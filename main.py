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


def reset_game():
    e.clear_sprites()
    e.load_level('levels/test.txt')


reset_game()

# Основные переменные
paused = False
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)


def draw_game_over():
    """Отображение экрана GAME OVER"""
    screen.fill((0, 0, 0))
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    instruction_text1 = button_font.render(
        "ЛКМ: Продолжить", True, (255, 255, 255))
    instruction_text2 = button_font.render(
        "ПКМ: Вернуться в меню", True, (255, 255, 255))

    screen.blit(game_over_text, game_over_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))
    screen.blit(instruction_text1, instruction_text1.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    screen.blit(instruction_text2, instruction_text2.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
    pygame.display.flip()


camera = e.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)


def run():
    running = True
    paused = False
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # ЛКМ
                        reset_game()
                        game_over = False
                    elif event.button == 3:  # ПКМ
                        s = menu.main_menu()
                        if s:
                            reset_game()
                            run()
                        running = False
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused

            if paused:
                continue_button_rect, restart_button_rect, settings_button_rect, exit_button_rect = draw_pause_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if continue_button_rect.collidepoint(mouse_pos):
                        paused = False
                    elif restart_button_rect.collidepoint(mouse_pos):
                        reset_game()
                        paused = False
                    elif settings_button_rect.collidepoint(mouse_pos):
                        print("Настройки (пока не реализовано)")
                    elif exit_button_rect.collidepoint(mouse_pos):
                        running = False
                        s = menu.main_menu()
                        if s:
                            run()
                continue

        if not paused and not game_over:
            screen.fill(0)
            e.hero.handle_input()
            e.hero.update()

            for stone in e.stone_sprites:
                stone.update()
                # Проверка на падение камня на героя
                if pygame.sprite.collide_rect(stone, e.hero):
                    if stone.velocity_y > 0:  # Камень падает вниз
                        game_over = True
                        draw_game_over()
                        break

            if game_over:
                continue

            camera.update(e.hero)

            for sprite_group in [e.background_sprites, e.stone_sprites, e.foreground_sprites]:
                for sprite in sprite_group:
                    camera.apply(sprite)

            e.background_sprites.draw(screen)
            e.stone_sprites.draw(screen)
            e.foreground_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)


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
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color,
                             button_rect.inflate(20, 10))  # Эффект наведения
        else:
            pygame.draw.rect(screen, button_color, button_rect.inflate(20, 10))

        # Отрисовка текста на кнопке
        screen.blit(button_surface, button_rect)

    return button_rects


menu = m.GameMenu()

if __name__ == "__main__":
    s = menu.main_menu()
    if s:
        run()

pygame.quit()
