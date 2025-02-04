import pygame
import sys


class GameMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Меню")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)

        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 30)

        self.buttons = ["Продолжить", "Играть",  "Выход"]
        self.button_rects = []

        self.button_width = 350
        self.button_height = 80
        self.spacing = 20
        self.total_height = len(
            self.buttons) * self.button_height + (len(self.buttons) - 1) * self.spacing

        start_y = (self.screen_height - self.total_height) // 2
        for i, text in enumerate(self.buttons):
            x = (self.screen_width - self.button_width) // 2
            y = start_y + i * (self.button_height + self.spacing)
            rect = pygame.Rect(x, y, self.button_width, self.button_height)
            self.button_rects.append(rect)

    def draw_text_centered(self, surface, text, font, rect, color):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

    def confirm_exit(self):
        confirm_rect = pygame.Rect(
            self.screen_width // 2 - 200, self.screen_height // 2 - 100, 400, 200)
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

            pygame.draw.rect(self.screen, self.GRAY, confirm_rect)
            pygame.draw.rect(self.screen, self.BLACK, confirm_rect, 3)

            s = "Вы действительно хотите выйти?"
            self.draw_text_centered(
                self.screen, s, self.small_font, confirm_rect, self.BLACK)

            pygame.draw.rect(self.screen, self.WHITE, yes_button)
            pygame.draw.rect(self.screen, self.WHITE, no_button)
            pygame.draw.rect(self.screen, self.BLACK, yes_button, 2)
            pygame.draw.rect(self.screen, self.BLACK, no_button, 2)

            self.draw_text_centered(
                self.screen, "Да", self.small_font, yes_button, self.BLACK)
            self.draw_text_centered(
                self.screen, "Нет", self.small_font, no_button, self.BLACK)

            pygame.display.flip()

    def main_menu(self):
        running = True

        # Загружаем изображение фона
        background_image = pygame.image.load("picture/formenu.jpg")
        # Масштабируем изображение на весь экран
        background_image = pygame.transform.scale(
            background_image, (self.screen_width, self.screen_height))

        while running:
            # Отображаем фон
            self.screen.blit(background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(event.pos):
                            if i == 0:
                                return True
                            if i == 1:  # Играть
                                return False
                            elif i == 2:  # Настройки
                                self.confirm_exit()
                            elif i == 3:  # Выход
                                self.confirm_exit()

            # Рисуем кнопки
            for i, rect in enumerate(self.button_rects):
                pygame.draw.rect(self.screen, self.GRAY, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 3)
                self.draw_text_centered(
                    self.screen, self.buttons[i], self.font, rect, self.BLACK)

            pygame.display.flip()

    pygame.quit()
