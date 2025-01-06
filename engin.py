import pygame
from pygame.sprite import Sprite
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Глобальные переменные
GRAVITY = 3
MOVE_SPEED = 3


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
        super().__init__(x, y, size*0.9, 'picture/hero.png')
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = True
        self.is_jumping = False
        self.jump_height = 0
        self.max_jump_height = size * 1.4

    def update(self):
        """Обновление позиции героя с учетом движения"""
        # Движение по горизонтали
        self.rect.x += self.velocity_x
        self.handle_collisions('horizontal')

        # Если герой в прыжке, проверяем, достиг ли он максимальной высоты
        if self.is_jumping:
            if self.jump_height < self.max_jump_height:
                self.velocity_y = -MOVE_SPEED  # Поднимаем героя вверх
                # Увеличиваем высоту прыжка
                self.jump_height += abs(self.velocity_y)
            else:
                self.velocity_y = GRAVITY  # Начинаем падать после достижения максимальной высоты
                if self.is_on_solid_ground():
                    self.is_jumping = False

        # Если герой не в прыжке, проверяем падение
        if not self.is_jumping and not self.is_on_solid_ground():
            self.velocity_y += GRAVITY  # Включаем гравитацию

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

    def handle_input(self):
        """Управление героем"""
        keys = pygame.key.get_pressed()
        self.velocity_x = 0

        if keys[pygame.K_LEFT]:
            self.velocity_x = -MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.velocity_x = MOVE_SPEED

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


class Background(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, 'picture/background.png')


class Wall(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, 'picture/wall.png')


class Stone(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x, y, size*0.95, 'picture/stone.png')
        self.velocity_y = 0  # Вертикальная скорость для падения
        self.size = size
        self.is_moving = False  # Флаг, который будет указывать, пытается ли игрок двигать камень
        self.time_on_stone = 0  # Время, проведённое на другом камне
        self.shaking = False

    def update(self):
        """Обновление состояния камня с учётом падения и движения"""
        if self.is_moving:
            return  # Если камень двигается, пропускаем его падение

        # Проверка, стоит ли камень на другом камне
        if self.is_on_solid_ground() and not self.is_on_falling_surface():
            self.time_on_stone = 0
            self.velocity_y = 0
            return

        # Если камень на камне, запускаем таймер
        if self.is_on_solid_ground():
            self.time_on_stone += 1
            if self.time_on_stone >= 90:  # 1.5 секунды при 60 FPS
                self.shaking = False
                self.try_fall_sideways()
            else:
                self.shake()
            return

        # Падение, если нет твёрдой поверхности под камнем
        if self.is_on_falling_surface():
            self.velocity_y = GRAVITY  # Камень падает

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
        left_free = self.check_free_space(-self.size, self.size)
        right_free = self.check_free_space(self.size, self.size)

        if left_free and right_free:
            self.rect.x += self.size if random.choice([True, False]) else -self.size
        elif left_free:
            self.rect.x -= self.size
        elif right_free:
            self.rect.x += self.size

    def check_free_space(self, offset_x, offset_y):
        """Проверяет, свободно ли пространство в указанном направлении."""
        self.rect.x += offset_x
        self.rect.y += offset_y
        collisions = pygame.sprite.spritecollide(self, solid_sprites, False)
        self.rect.x -= offset_x
        self.rect.y -= offset_y
        return not collisions

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
        collisions = pygame.sprite.spritecollide(self, solid_sprites, False) + \
            pygame.sprite.spritecollide(self, stone_sprites, False)
        self.rect.y -= 1
        return any(isinstance(sprite, Wall) for sprite in collisions)

    def is_on_falling_surface(self):
        """Проверка, может ли камень падать (если под ним Liana или Background)."""
        self.rect.y += 1
        collisions = pygame.sprite.spritecollide(self, solid_sprites, False)
        self.rect.y -= 1
        return not any(isinstance(sprite, (Wall, Stone)) for sprite in collisions)

    def set_moving(self, moving):
        """Устанавливает флаг движения (для того, чтобы игрок мог двигать камень)."""
        self.is_moving = moving


class Lianas(BaseSprite):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, 'picture/lianas.png')


# Группы спрайтов
background_sprites = pygame.sprite.Group()
foreground_sprites = pygame.sprite.Group()
solid_sprites = pygame.sprite.Group()
stone_sprites = pygame.sprite.Group()
hero = None

sprite_classes = {
    "h": Hero,
    "b": Background,
    "w": Wall,
    "s": Stone,
    "l": Lianas
}


def load_level(filename):
    global hero
    with open(filename, 'r') as file:
        lines = [line.strip().split(', ') for line in file]

    rows, cols = len(lines), len(lines[0])
    tile_size = min(SCREEN_WIDTH // cols, SCREEN_HEIGHT // rows)

    for row_index, line in enumerate(lines):
        for col_index, tile in enumerate(line):
            x, y = col_index * tile_size, row_index * tile_size
            for symbol in tile:
                if symbol in sprite_classes:
                    sprite = sprite_classes[symbol](x, y, tile_size)
                    if isinstance(sprite, (Background, Lianas)):
                        background_sprites.add(sprite)
                    elif isinstance(sprite, Hero):
                        hero = sprite
                        foreground_sprites.add(sprite)
                    elif isinstance(sprite, Wall):
                        solid_sprites.add(sprite)
                        foreground_sprites.add(sprite)
                    elif isinstance(sprite, Stone):
                        stone_sprites.add(sprite)
