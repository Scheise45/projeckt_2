import pygame
import engin as e

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
clock = pygame.time.Clock()

# Загрузка уровня


def reset_game():
    e.clear_sprites()  # Очистка всех спрайтов (если такая функция есть)
    e.load_level('levels/test.txt')  # Загрузка уровня


reset_game()

# Основные переменные
running = True
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


# Основной игровой цикл
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
                    # Здесь можно добавить функционал настроек
                    print("Настройки (пока не реализовано)")
                elif exit_button_rect.collidepoint(mouse_pos):
                    running = False  # Выйти из игры

            continue

    if not paused:
        e.hero.handle_input()
        e.hero.update()
        for stone in e.stone_sprites:
            stone.update()

        # Сначала фон, потом камни, потом передний план
        e.background_sprites.draw(screen)
        e.stone_sprites.draw(screen)
        e.foreground_sprites.draw(screen)

    else:
        # Отрисовка меню паузы без фона
        draw_pause_menu()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
