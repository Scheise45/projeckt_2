import pygame
import engin as e
import MENU as m
import csv
# Инициализация Pygame
pygame.init()

# Настройки экрана
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
clock = pygame.time.Clock()

# Высота нижней панели
STATUS_BAR_HEIGHT = 100
lvls = ["test", "second"]
# Загрузка уровня


def rewrite_settings_volume():
    with open("levels/settings.csv", newline='', encoding='utf-8') as f:
        r = list(csv.reader(f))  # Читаем текущие настройки
        if len(r) > 1:
            r[1][0] = str(int(music_on))

    with open("levels/settings.csv", "w", newline='', encoding='utf-8') as f:
        writ = csv.writer(f)
        writ.writerows(r)  # Записываем обновлённые данные


def rewrite_settings(arg):
    with open("levels/settings.csv", newline='', encoding='utf-8') as f:
        r = list(csv.reader(f))  # Читаем текущие настройки

    if len(r) > 1:  # Проверяем, что есть данные
        r[1][2] = str(arg)  # Обновляем lastlvl

    with open("levels/settings.csv", "w", newline='', encoding='utf-8') as f:
        writ = csv.writer(f)
        writ.writerows(r)  # Записываем обновлённые данные


def load():
    with open("levels/settings.csv") as qq:
        reader = csv.DictReader(qq, delimiter=',', quotechar='"')
        settings = sorted(reader, reverse=True)
    for i in settings:
        lvl = int(i["lastlvl"])
    return lvls[lvl]


def reset_game(map="test"):
    e.load_level(f'levels/{map}.txt')  # Загрузка уровня


# Основные переменные
paused = False

# Шрифты
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Переменные для управления звуком
with open("levels/settings.csv") as qq:
    reader = csv.DictReader(qq, delimiter=',', quotechar='"')
    settings = sorted(reader, reverse=True)
    for i in settings:
        music_on = bool(int(i["music"]))
        sound_on = bool(i["interface"])


# Запуск фоновой музыки
pygame.mixer.music.load("volume/music2.mp3")  # Загружаем музыку
pygame.mixer.music.play(-1)  # Запускаем бесконечное воспроизведение
pygame.mixer.music.set_volume(0.15 if music_on else 0.0)  # Громкость


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


def draw_status_bar(flag=False):
    # Нижняя панель
    if flag:
        TOTAL = len(e.diamond_sprites)
        pygame.draw.rect(screen, (0, 90, 0), (0, SCREEN_HEIGHT -
                                              STATUS_BAR_HEIGHT, SCREEN_WIDTH, STATUS_BAR_HEIGHT))

        crystals_text = font.render(
            f'Недостаточно кристаллов для завершения, найдите ещё: {TOTAL}', True, (255, 255, 255))

        screen.blit(crystals_text, (SCREEN_WIDTH - crystals_text.get_width() -
                    10, SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 20))
    else:
        TOTAL = len(e.diamond_sprites)
        pygame.draw.rect(screen, (0, 90, 0), (0, SCREEN_HEIGHT -
                                              STATUS_BAR_HEIGHT, SCREEN_WIDTH, STATUS_BAR_HEIGHT))

        crystals_text = font.render(
            f'Кристаллов осталось: {TOTAL}', True, (255, 255, 255))

        screen.blit(crystals_text, (SCREEN_WIDTH - crystals_text.get_width() -
                    10, SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 20))


def draw_game_over():
    """Отображение экрана GAME OVER"""
    gamover = pygame.image.load("picture/gameover.jpg")
    gamover = pygame.transform.scale(gamover, (SCREEN_WIDTH, SCREEN_HEIGHT))

    instruction_text1 = button_font.render(
        "ЛКМ: Начать сначало", True, (255, 255, 255))
    instruction_text2 = button_font.render(
        "ПКМ: Вернуться в меню", True, (255, 255, 255))

    screen.blit(gamover, (0, 0))  # Отображаем картинку на весь экран
    screen.blit(instruction_text1, instruction_text1.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)))
    screen.blit(instruction_text2, instruction_text2.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)))

    pygame.display.flip()  # Обновляем экран


"""отрисовка конца уровня"""


def draw_end_level():
    endlevle = pygame.image.load("picture/quest.jpg")
    endlevle = pygame.transform.scale(endlevle, (SCREEN_WIDTH, SCREEN_HEIGHT))

    instruction_text1 = button_font.render(
        "ЛКМ: Слудующий уровень", True, (255, 255, 255))
    instruction_text2 = button_font.render(
        "ПКМ: Вернуться в меню", True, (255, 255, 255))

    screen.blit(endlevle, (0, 0))  # Отображаем картинку на весь экран
    screen.blit(instruction_text1, instruction_text1.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)))
    screen.blit(instruction_text2, instruction_text2.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)))

    pygame.display.flip()  # Обновляем экран


def draw_settings_menu():
    settings_width = SCREEN_WIDTH // 2
    settings_height = SCREEN_HEIGHT // 2
    settings_rect = pygame.Rect((SCREEN_WIDTH - settings_width) // 2,
                                (SCREEN_HEIGHT - settings_height) // 2, settings_width, settings_height)

    # Рисуем фон меню настроек
    pygame.draw.rect(screen, "orange", settings_rect)

    title_surface = button_font.render("Настройки", True, (255, 255, 255))
    screen.blit(title_surface, title_surface.get_rect(
        center=(SCREEN_WIDTH // 2, settings_rect.top + 30)))

    # Кнопка для включения/выключения музыки
    music_button_text = "Музыка: Включена" if music_on else "Музыка: Выключена"
    music_button_surface = button_font.render(
        music_button_text, True, (255, 255, 255))
    music_button_rect = music_button_surface.get_rect(
        center=(SCREEN_WIDTH // 2, settings_rect.top + 100))

    pygame.draw.rect(screen, (50, 50, 50), music_button_rect.inflate(20, 10))
    screen.blit(music_button_surface, music_button_rect)

    return music_button_rect


def run(map):
    reset_game(map)
    diamond_for_end = len(e.diamond_sprites) // 2
    camera = e.Camera(SCREEN_WIDTH, SCREEN_HEIGHT, 48 * 130, 20 * 130)
    in_settings_menu = False

    # Заставка
    quest_image = pygame.image.load("picture/quest.jpg")
    quest_image = pygame.transform.scale(
        quest_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.blit(quest_image, (0, 0))
        pygame.display.flip()

    running = True
    paused = False
    game_over = False
    end_levle = False

    while running:
        of_exit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                in_settings_menu = False
                paused = not paused

            if end_levle:
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        arg = (lvls.index(map)+1) % 2
                        map = lvls[arg]
                        reset_game(map)
                        rewrite_settings(arg)
                        camera = e.Camera(
                            SCREEN_WIDTH, SCREEN_HEIGHT, 48 * 130, 20 * 130)
                        end_levle = False

                    elif event.button == 3:
                        s = menu.main_menu()
                        if s:
                            reset_game(map)
                            run(map)
                        else:
                            rewrite_settings(0)
                            run(lvls[0])
                        running = False
                continue

            elif game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        reset_game(map)
                        camera = e.Camera(
                            SCREEN_WIDTH, SCREEN_HEIGHT, 48 * 130, 20 * 130)
                        game_over = False

                    elif event.button == 3:
                        s = menu.main_menu()
                        if s:
                            reset_game(map)
                            run(map)
                        else:
                            rewrite_settings(0)
                            run(lvls[0])
                        running = False
                continue

            elif in_settings_menu:
                music_button_rect = draw_settings_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if music_button_rect.collidepoint(mouse_pos):
                        global music_on
                        music_on = not music_on
                        pygame.mixer.music.set_volume(
                            0.15 if music_on else 0.0)
                        rewrite_settings_volume()

            else:
                if paused:
                    continue_button_rect, restart_button_rect, settings_button_rect, exit_button_rect = draw_pause_menu()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if continue_button_rect.collidepoint(mouse_pos):
                            paused = False
                        elif restart_button_rect.collidepoint(mouse_pos):
                            reset_game(map)
                            camera = e.Camera(
                                SCREEN_WIDTH, SCREEN_HEIGHT, 48 * 130, 20 * 130)
                            paused = False
                        elif settings_button_rect.collidepoint(mouse_pos):
                            in_settings_menu = True
                        elif exit_button_rect.collidepoint(mouse_pos):
                            running = False
                            reset_game(map)
                            s = menu.main_menu()
                            if not s:
                                arg = 0
                                map = lvls[arg]
                                reset_game(map)
                                rewrite_settings(arg)
                            run(map)
                    continue

        if not paused and not game_over and not end_levle:
            screen.fill(0)
            e.hero.handle_input()
            e.hero.update()

            for stone in e.stone_sprites:
                stone.update()
                if pygame.sprite.collide_rect(stone, e.hero):
                    if stone.velocity_y > 0:
                        game_over = True
                        draw_game_over()
                        break

            """Обработка конца уровня"""
            for exit in e.exit_sprites:
                if pygame.sprite.collide_rect(exit, e.hero):
                    if len(e.diamond_sprites) <= diamond_for_end:
                        end_levle = True
                        draw_end_level()
                        break
                    else:
                        of_exit = True

            if game_over:
                continue

            if end_levle:
                continue

            camera.update(e.hero)

            all_sp_group = [e.background_sprites, e.stone_sprites,
                            e.diamond_sprites, e.foreground_sprites, e.exit_sprites]

            for sprite_group in all_sp_group:
                for sprite in sprite_group:
                    camera.apply(sprite)

            e.background_sprites.draw(screen)
            e.exit_sprites.draw(screen)
            e.stone_sprites.draw(screen)
            e.foreground_sprites.draw(screen)
            e.diamond_sprites.draw(screen)

            draw_status_bar(of_exit)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


menu = m.GameMenu()

if __name__ == "__main__":
    s = menu.main_menu()
    if not s:
        rewrite_settings(0)
    lvl = load()

    run(lvl)

pygame.quit()
