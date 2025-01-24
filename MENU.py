import math as m
import pygame
import sys
import subprocess
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Меню")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 30)

buttons = ["Продолжить", "Играть", "Настройки", "Выход"]
button_rects = []

button_width = 350
button_height = 80
spacing = 20
total_height = len(buttons) * button_height + (len(buttons) - 1) * spacing

start_y = (screen_height - total_height) // 2
for i, text in enumerate(buttons):
    x = (screen_width - button_width) // 2
    y = start_y + i * (button_height + spacing)
    rect = pygame.Rect(x, y, button_width, button_height)
    button_rects.append(rect)


def draw_text_centered(surface, text, font, rect, color):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def confirm_exit():
    confirm_rect = pygame.Rect(
        screen_width // 2 - 200, screen_height // 2 - 100, 400, 200)
    yes_button = pygame.Rect(
        confirm_rect.x + 50, confirm_rect.y + 120, 120, 50)
    no_button = pygame.Rect(confirm_rect.x + 230,
                            confirm_rect.y + 120, 120, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if yes_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif no_button.collidepoint(event.pos):
                    return

        pygame.draw.rect(screen, GRAY, confirm_rect)
        pygame.draw.rect(screen, BLACK, confirm_rect, 3)

        s = "Вы действительно хотите выйти?"
        draw_text_centered(
            screen, s, small_font, confirm_rect, BLACK)

        pygame.draw.rect(screen, WHITE, yes_button)
        pygame.draw.rect(screen, WHITE, no_button)
        pygame.draw.rect(screen, BLACK, yes_button, 2)
        pygame.draw.rect(screen, BLACK, no_button, 2)

        draw_text_centered(screen, "Да", small_font, yes_button, BLACK)
        draw_text_centered(screen, "Нет", small_font, no_button, BLACK)

        pygame.display.flip()


def main_menu():
    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        if i == 0:
                            # Запуск main.py
                            subprocess.Popen(['python', 'main.py'])
                            running = False
                        if i == 1:  # Играть
                            # Запуск main.py
                            subprocess.Popen(['python', 'main.py'])
                            running = False  # Закрываем текущее окно
                        elif i == 2:  # Настройки
                            print("Открываем настройки!")
                        elif i == 3:  # Выход
                            confirm_exit()

        # Рисуем кнопки
        for i, rect in enumerate(button_rects):
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)
            draw_text_centered(screen, buttons[i], font, rect, BLACK)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main_menu()
