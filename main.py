import pygame
import engin as e
import MENU as m
# Инициализация Pygame
pygame.init()

# Настройки экрана
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
clock = pygame.time.Clock()

# Высота нижней панели
STATUS_BAR_HEIGHT = 100

# Загрузка уровня


def reset_game():
    e.clear_sprites()  # Очистка всех спрайтов (если такая функция есть)
    e.load_level('levels/test.txt')  # Загрузка уровня


reset_game()

# Основные переменные
paused = False

# Шрифты
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Функция для отрисовки кнопок


def draw_pause_menu():
    button_color = (50, 50, 50)  # Цвет фона кнопок
    button_hover_color = (100, 100, 100)  # Цвет фона кнопок при наведении
    text_color = (255, 255, 255)  # Цвет текста

    # Кнопки
    buttons = [
        ("Продолжить", SCREEN_HEIGHT // 4 + 50),
        ("Заново", SCREEN_HEIGHT // 4 + 150),
        ("Настройки", SCREEN_HEIGHT // 4 + 250),
        ("Выйти", SCREEN_HEIGHT // 4 + 350)
    ]

    button_rects = []

    for text, y in buttons:
        button_surface = button_font.render(text, True, text_color)
        button_rect = button_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
        button_rects.append(button_rect)

        # Отрисовка фона кнопки
        if paused and button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, button_rect.inflate(
                20, 10))  # Увеличиваем размер кнопки для эффекта наведения
        else:
            pygame.draw.rect(screen, button_color, button_rect.inflate(20, 10))

        # Отрисовка текста на кнопке
        screen.blit(button_surface, button_rect)

    return button_rects

# Функция для отрисовки статической нижней панели


def draw_status_bar(lives, crystals):
    # Нижняя панель
    pygame.draw.rect(screen, (0, 128, 0), (0, SCREEN_HEIGHT -
                     STATUS_BAR_HEIGHT, SCREEN_WIDTH, STATUS_BAR_HEIGHT))

    # Отображение жизней и кристаллов
    lives_text = font.render(f'Жизни: {lives}', True, (255, 255, 255))
    crystals_text = font.render(
        f'Кристаллы: {crystals}', True, (255, 255, 255))

    screen.blit(lives_text, (10, SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 20))
    screen.blit(crystals_text, (SCREEN_WIDTH - crystals_text.get_width() -
                10, SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 20))


camera = e.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)


def run():
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # Переключаем состояние паузы

            if paused:
                continue_button_rect, restart_button_rect, settings_button_rect, exit_button_rect = draw_pause_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if continue_button_rect.collidepoint(mouse_pos):
                        paused = False  # Продолжить игру
                    elif restart_button_rect.collidepoint(mouse_pos):
                        reset_game()  # Сбросить состояние и заново загрузить уровень
                        paused = False  # Выход из паузы
                    elif settings_button_rect.collidepoint(mouse_pos):
                        print("Настройки (пока не реализовано)")
                    elif exit_button_rect.collidepoint(mouse_pos):
                        running = False  # Выйти из игры
                        s = menu.main_menu()
                        if s:
                            run()
                continue

        if not paused:
            screen.fill(0)
            e.hero.handle_input()
            e.hero.update()
            for stone in e.stone_sprites:
                stone.update()

            camera.update(e.hero)

            for sprite_group in [e.background_sprites, e.stone_sprites, e.foreground_sprites]:
                for sprite in sprite_group:
                    camera.apply(sprite)

            e.background_sprites.draw(screen)
            e.stone_sprites.draw(screen)
            e.foreground_sprites.draw(screen)
            # Предполагается наличие атрибутов lives и crystals у героя
            # draw_status_bar(e.hero.lives, e.hero.crystals)
        else:
            draw_pause_menu()

        pygame.display.flip()
        clock.tick(60)


menu = m.GameMenu()

if __name__ == "__main__":
    s = menu.main_menu()
    if s:
        run()
pygame.quit()
