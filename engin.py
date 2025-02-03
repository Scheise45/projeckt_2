import pygame
from pygame.sprite import Sprite
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
clock = pygame.time.Clock()

# Глобальные переменные
MOVE_SPEED = 7


def load_image(image_path, size):
    image = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(image, (size, size))


class BaseSprite(Sprite):
    def __init__(self, x, y, size, image_path):
        super().__init__()
        self.image = load_image(image_path, size)
        self.rect = self.image.get_rect(topleft=(x, y))


class Hero(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x, y - int(size * 0.2), size * 0.9, 'picture/hero.png')
        self.size = size
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = True
        self.is_jumping = False
        self.jump_height = 0
        self.max_jump_height = size * 1.4
        self.facing_right = True
        self.collected_diamonds = 0
        self.TOTAL_DIAMONDS = len(diamond_sprites)

        # Загрузка звука шагов
        self.step_sound = pygame.mixer.Sound('volume/step.mp3')
        self.step_sound.set_volume(1)  # Громкость (0.0 - 1.0)

        # Флаг движения
        self.is_moving = False

        # Анимации
        self.standing_image = pygame.transform.scale(
            pygame.image.load('picture/hero.png'), (size*0.9, size*0.9)
        )
        self.walking_images = [
            pygame.transform.scale(
                pygame.image.load(f'picture/hero{i}.png'), (size*0.9, size*0.9)
            ) for i in range(1, 5)
        ]
        self.image = self.standing_image
        self.image_index = 0
        self.animation_timer = 0
        self.animation_speed = 5

    def update(self):
        """Обновление позиции героя с учетом движения"""
        # Движение по горизонтали
        self.rect.x += self.velocity_x
        self.handle_collisions('horizontal')

        # Проверка столкновения с алмазами
        self.collect_diamonds()

        # Если герой в прыжке, проверяем, достиг ли он максимальной высоты
        if self.is_jumping:
            if self.jump_height < self.max_jump_height:
                self.velocity_y = -MOVE_SPEED  # Поднимаем героя вверх
                # Увеличиваем высоту прыжка
                self.jump_height += abs(self.velocity_y)
            else:
                self.velocity_y = MOVE_SPEED  # Начинаем падать после достижения максимальной высоты
                if self.is_on_solid_ground():
                    self.is_jumping = False

        # Если герой не в прыжке, проверяем падение
        if not self.is_jumping and not self.is_on_solid_ground():
            self.velocity_y = MOVE_SPEED  # Включаем гравитацию

        if self.is_on_solid_ground() and not self.is_jumping:
            self.velocity_y = 0  # Если на земле, сбрасываем вертикальную скорость
            self.on_ground = True  # Герой на земле
            # Сбрасываем флаг прыжка только если герой на земле
            self.is_jumping = False

        # Движение по вертикали (прыжок или падение)
        self.rect.y += self.velocity_y
        self.handle_collisions('vertical')

        # Ограничение выхода за границы экрана
        self.clamp_to_screen()

        # Обновление анимации
        self.update_animation()

    def collect_diamonds(self):
        """Сбор кристаллов"""
        diamond_collisions = pygame.sprite.spritecollide(
            self, diamond_sprites, True)
        self.collected_diamonds += len(diamond_collisions)
        self.display_diamond_count()

    def display_diamond_count(self):
        """Вывод количества собранных и оставшихся кристаллов"""
        remaining_diamonds = self.TOTAL_DIAMONDS - self.collected_diamonds

    def handle_input(self):
        """Управление героем"""
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        self.is_moving = False  # Сбрасываем флаг перед проверкой

        if keys[pygame.K_LEFT]:
            self.velocity_x = -MOVE_SPEED
            self.is_moving = True  # Герой движется влево
            if self.facing_right:
                self.flip_images()
        if keys[pygame.K_RIGHT]:
            self.velocity_x = MOVE_SPEED
            self.is_moving = True  # Герой движется вправо
            if not self.facing_right:
                self.flip_images()

        # Начинаем прыжок, если не в прыжке и если на земле
        if keys[pygame.K_UP] and not self.is_jumping and self.on_ground:
            self.is_jumping = True
            self.jump_height = 0  # Сбрасываем высоту прыжка
            self.velocity_y = -MOVE_SPEED  # Начинаем подниматься вверх

    def handle_collisions(self, direction):
        """Обновлённая логика столкновений"""
        stone_collisions = pygame.sprite.spritecollide(
            self, stone_sprites, False)

        # Если герой сталкивается с камнем, пытаемся его сдвинуть
        for stone in stone_collisions:
            if direction == 'horizontal':
                stone.push('right' if self.velocity_x > 0 else 'left')

        # Проверка столкновений с твёрдыми объектами и камнями
        collisions = pygame.sprite.spritecollide(self, solid_sprites, False) + \
            pygame.sprite.spritecollide(self, stone_sprites, False)

        for sprite in collisions:
            if sprite != self:
                if direction == 'vertical':
                    if self.velocity_y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                        self.is_jumping = False
                    elif self.velocity_y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.velocity_y = 0
                elif direction == 'horizontal':
                    if self.velocity_x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.velocity_x < 0:
                        self.rect.left = sprite.rect.right

    def clamp_to_screen(self):
        """Ограничение выхода за границы экрана"""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def is_on_solid_ground(self):
        """Проверка, находится ли герой на твердой поверхности под ногами"""
        self.rect.y += 1  # Временное смещение вниз для проверки
        collisions = pygame.sprite.spritecollide(self, solid_sprites, False)
        self.rect.y -= 1
        return bool(collisions)

    def flip_images(self):
        """Переворот изображений героя при смене направления"""
        self.facing_right = not self.facing_right
        self.standing_image = pygame.transform.flip(
            self.standing_image, True, False)
        self.walking_images = [
            pygame.transform.flip(image, True, False)
            for image in self.walking_images
        ]

    def update_animation(self):
        """Обновление текущего кадра анимации и звука шагов"""
        if self.is_moving:  # Если герой двигается
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.image_index = (self.image_index +
                                    1) % len(self.walking_images)
                self.image = self.walking_images[self.image_index]

                # Воспроизводим звук, если он ещё не играет
                if not self.step_sound.get_num_channels():
                    self.step_sound.play()
        else:
            self.image = self.standing_image
            self.step_sound.stop()  # Останавливаем звук, если герой перестал двигаться


class Background(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, 'picture/background.png')


class Wall(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, 'picture/wall.png')


class Stone(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x, y, size*0.85, 'picture/stone.png')
        self.velocity_y = 0  # Вертикальная скорость для падения
        self.size = size
        self.is_moving = False  # Флаг, который будет указывать, пытается ли игрок двигать камень
        self.time_on_stone = 0  # Время, проведённое на другом камне
        self.shaking = False
        self.onefall = True

    def update(self):
        """Обновление состояния камня с учётом падения и движения"""

        # Если камень на камне, запускаем таймер
        if self.is_on_stone() and self.onefall:
            self.shaking = True
            self.time_on_stone += 1
            if self.time_on_stone >= 90:  # 1.25 секунды при 60 FPS
                self.shaking = False
                self.onefall = False
                self.try_fall_sideways()
                self.time_on_stone = 0
            else:
                self.shake()
            return

        # Падение, если нет твёрдой поверхности под камнем
        if not self.is_on_falling_surface():
            self.velocity_y = MOVE_SPEED  # Камень падает

        # Падение вниз, если не на поверхности
        self.rect.y += self.velocity_y

        # Проверка столкновений вниз (с камнями и стенами)
        collisions = pygame.sprite.spritecollide(self, solid_sprites, False) + \
            pygame.sprite.spritecollide(self, stone_sprites, False)
        for sprite in collisions:
            if sprite != self and self.velocity_y > 0:
                self.rect.bottom = sprite.rect.top
                self.velocity_y = 0

    def shake(self):
        """Эффект дрожания камня перед падением."""
        if self.shaking:
            self.rect.x += 2 if self.time_on_stone % 10 < 5 else -2
        else:
            self.shaking = True

    def try_fall_sideways(self):
        """Попытка упасть в сторону, если под камнем нет твердой поверхности."""
        left_free = self.check_free_space(-self.size)
        right_free = self.check_free_space(self.size)

        if left_free and right_free:
            self.rect.x += self.size if random.choice(
                [True, False]) else -self.size
        elif left_free:
            self.rect.x += -self.size * 0.95
        elif right_free:
            self.rect.x += self.size * 0.95
        else:
            self.rect.x += self.size * 0.03

    def check_free_space(self, offset_x):
        """Проверяет, свободно ли пространство сбоку и снизу.
        Под проверку попадают только объекты Wall и Stone."""
        # Смещаемся по оси X для проверки
        self.rect.x += offset_x*0.9
        # Исключаем текущий камень из проверки
        collisions_x = [sprite for sprite in (
            pygame.sprite.spritecollide(self, solid_sprites, False) +
            pygame.sprite.spritecollide(self, stone_sprites, False))
            if sprite != self]
        self.rect.x -= offset_x

        # Если на пути есть препятствия по X, пространство не свободно
        if collisions_x:
            return False

        # Теперь проверяем, что под камнем (вниз по Y)
        self.rect.y += self.size*0.9
        collisions_y = [sprite for sprite in (
            pygame.sprite.spritecollide(self, solid_sprites, False) +
            pygame.sprite.spritecollide(self, stone_sprites, False))
            if sprite != self]
        self.rect.y -= self.size

        # Пространство считается свободным только если по X свободно и снизу нет препятствий
        return collisions_y

    def push(self, direction):
        """Двигает камень только если это возможно (игрок может толкать)."""
        original_position = self.rect.x
        if direction == 'right':
            self.rect.x += MOVE_SPEED
        elif direction == 'left':
            self.rect.x -= MOVE_SPEED

        # Проверка столкновений с другими объектами
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or \
                pygame.sprite.spritecollide(self, solid_sprites, False):
            self.rect.x = original_position
        collisions = pygame.sprite.spritecollide(self, solid_sprites, False) + \
            pygame.sprite.spritecollide(self, stone_sprites, False)
        for sprite in collisions:
            if sprite != self:
                self.rect.x = original_position
                break

    def is_on_solid_ground(self):
        """Проверка, стоит ли камень на твердой поверхности (Stone, Wall)."""
        self.rect.y += 1
        collisions = pygame.sprite.spritecollide(
            self, solid_sprites, False)  # + \
        # pygame.sprite.spritecollide(self, stone_sprites, False)
        self.rect.y -= 1
        return any(isinstance(sprite, Wall) for sprite in collisions)

    def is_on_stone(self):
        """Проверка, стоит ли камень на другом камне из той же группы."""
        self.rect.y += 1  # Временное смещение вниз для проверки
        collisions = pygame.sprite.spritecollide(self, stone_sprites, False)
        self.rect.y -= 1

        # Исключаем сам камень из проверки
        for sprite in collisions:
            if sprite != self:
                return True
        return False

    def is_on_falling_surface(self):
        """Проверка, может ли камень падать (если под ним Liana или Background)."""
        self.rect.y += 1
        collisions = pygame.sprite.spritecollide(self, solid_sprites, False)
        self.rect.y -= 1
        return any(isinstance(sprite, (Wall, Stone)) for sprite in collisions)


class Lianas(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, 'picture/lianas.png')


class Diamond(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x + size * 0.25, y + size *
                         0.25, size * 0.5, "picture/diamond.png")


class Exit(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "picture/exit.png")


class Camera:
    def __init__(self, screen_width, screen_height, map_w, map_h):
        self.offset_x = 0  # Смещение по оси X
        self.offset_y = 0  # Смещение по оси Y
        self.map_w = map_w
        self.map_h = map_h
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.last_offset_x = 0  # последнее смещение
        self.summ_offset_x = 0  # координаты
        self.summ_offset_y = 0
        self.last_offset_y = 0

    def update(self, target):
        """Обновляет положение камеры, удерживая target в центре экрана."""
        self.way_x = 902
        self.way_y = -571
        self.offset_x = target.rect.centerx - self.screen_width // 2
        self.offset_y = target.rect.centery - self.screen_height // 2
        if self.summ_offset_x < self.way_x:
            self.summ_offset_x = self.offset_x + self.way_x
            self.offset_x = 0
        elif self.summ_offset_x > self.map_w - 1020:
            self.summ_offset_x += (self.offset_x - self.last_offset_x)
            self.last_offset_x = self.offset_x
            self.offset_x = 0
        else:
            self.summ_offset_x += self.offset_x

        if self.summ_offset_y < self.way_y:
            self.summ_offset_y = self.offset_y + self.way_y
            self.offset_y = 0
        elif self.summ_offset_y > self.map_h - 560:
            self.summ_offset_y += (self.offset_y - self.last_offset_y)
            self.last_offset_y = self.offset_y
            self.offset_y = 0
        else:
            self.summ_offset_y += self.offset_y

    def apply(self, sprite):
        """Смещение позиции спрайта в зависимости от положения камеры."""
        sprite.rect.x -= self.offset_x
        sprite.rect.y -= self.offset_y


# Группы спрайтов
background_sprites = pygame.sprite.Group()
foreground_sprites = pygame.sprite.Group()
solid_sprites = pygame.sprite.Group()
stone_sprites = pygame.sprite.Group()
diamond_sprites = pygame.sprite.Group()
exit_sprites = pygame.sprite.Group()


# volume_on = m.sound_on


def clear_sprites():
    background_sprites.empty()  # Очищаем группу фона
    stone_sprites.empty()       # Очищаем группу камней
    foreground_sprites.empty()  # Очищаем группу переднего плана


hero = None

sprite_classes = {
    "h": Hero,
    "b": Background,
    "w": Wall,
    "s": Stone,
    "l": Lianas,
    'd': Diamond,
    "e": Exit
}


def clear_group():
    background_sprites.empty()
    foreground_sprites.empty()
    solid_sprites.empty()
    stone_sprites.empty()
    diamond_sprites.empty()  # Очищаем алмазы перед загрузкой
    exit_sprites.empty()


def load_level(filename):
    global hero
    with open(filename, 'r') as file:
        lines = [line.strip().split(', ') for line in file]

    rows, cols = len(lines), len(lines[0])
    tile_size = 130

    # Очищаем группы перед загрузкой уровня
    background_sprites.empty()
    foreground_sprites.empty()
    solid_sprites.empty()
    stone_sprites.empty()
    diamond_sprites.empty()  # Очищаем алмазы перед загрузкой
    exit_sprites.empty()

    for row_index, line in enumerate(lines):
        for col_index, tile in enumerate(line):
            x, y = col_index * tile_size, row_index * tile_size
            for symbol in tile:
                if symbol in sprite_classes:
                    sprite = sprite_classes[symbol](x, y, tile_size)
                    if isinstance(sprite, (Background, Lianas)):
                        background_sprites.add(sprite)
                    elif isinstance(sprite, Exit):
                        exit_sprites.add(sprite)
                    elif isinstance(sprite, Hero):
                        hero = sprite
                        foreground_sprites.add(sprite)
                    elif isinstance(sprite, Wall):
                        solid_sprites.add(sprite)
                        foreground_sprites.add(sprite)
                    elif isinstance(sprite, Stone):
                        stone_sprites.add(sprite)
                    elif isinstance(sprite, Diamond):  # Добавляем алмазы
                        diamond_sprites.add(sprite)
