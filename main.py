import pygame
import engin as e

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Загрузка уровня
e.load_level('levels/test.txt')

# Основной игровой цикл
running = True
while running:
    screen.fill((100, 100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    e.hero.handle_input()
    e.hero.update()
    for stone in e.stone_sprites:
        stone.update()

    # Сначала фон, потом камни, потом передний план
    e.background_sprites.draw(screen)
    e.stone_sprites.draw(screen)
    e.foreground_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
