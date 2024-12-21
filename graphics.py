import pygame

s = [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1],
    [2, 3, 2, 3, 2, 2],
    [2, 1, 2, 1, 2, 2],
    [4, 1, 2, 1, 2, 2],
    [1, 1, 1, 1, 1, 1],
]
pygame.init()
screen = pygame.display.set_mode((600, 600))
screen.fill("white")
hero = pygame.image.load("hero.jpg")
sky = pygame.image.load("sky.jpg")
wall = pygame.image.load("wall.jpg")
lianas = pygame.image.load("lianas.jpg")
stone = pygame.image.load("stone.jpg")
fils = [sky, wall, lianas, stone, hero]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for n1, i in enumerate(s):
        for n2, j in enumerate(i):
            screen.blit(fils[j], (n2 * 100, n1 * 100))
    pygame.display.flip()
pygame.quit()
