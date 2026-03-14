import pygame as pg
import sys
import random

# 1. Ініціалізація
pg.init()
WIDTH, HEIGHT = 600, 400
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("PACMAN vs GHOSTS")
clock = pg.time.Clock()

# Шрифти
font_big = pg.font.SysFont("Arial", 48, bold=True)
font_small = pg.font.SysFont("Arial", 24)

# 2. Кольори
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Колір для бота
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TILE_SIZE = 40

MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,0,1,1,0,1,0,1,1,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

def reset_game():
    dots = []
    for r in range(len(MAP)):
        for c in range(len(MAP[r])):
            if MAP[r][c] == 0:
                dots.append(pg.Vector2(c * TILE_SIZE + 20, r * TILE_SIZE + 20))
    
    p_pos = pg.Vector2(60, 60)
    g_pos = pg.Vector2(540, 300)
    # Позиція бота та його початковий напрямок
    bot_pos = pg.Vector2(300, 220)
    bot_dir = random.choice([pg.Vector2(0, 2), pg.Vector2(0, -2), pg.Vector2(2, 0), pg.Vector2(-2, 0)])
    
    return dots, p_pos, g_pos, bot_pos, bot_dir

def draw_text(text, font, color, y_offset=0):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)

dots, p_pos, g_pos, bot_pos, bot_dir = reset_game()
game_state = "PLAY"

while True:
    screen.fill(BLACK)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if game_state != "PLAY" and event.key == pg.K_SPACE:
                dots, p_pos, g_pos, bot_pos, bot_dir = reset_game()
                game_state = "PLAY"

    if game_state == "PLAY":
        k = pg.key.get_pressed()
        
        # --- ЛОГІКА ПАКМЕНА ---
        new_p = p_pos + pg.Vector2(0,0)
        if k[pg.K_UP]:    new_p.y -= 3
        if k[pg.K_DOWN]:  new_p.y += 3
        if k[pg.K_LEFT]:  new_p.x -= 3
        if k[pg.K_RIGHT]: new_p.x += 3
        if MAP[int(new_p.y//TILE_SIZE)][int(new_p.x//TILE_SIZE)] == 0:
            p_pos = new_p

        # --- ЛОГІКА ПРИВИДА (ГРАВЕЦЬ) ---
        new_g = g_pos + pg.Vector2(0,0)
        if k[pg.K_w]: new_g.y -= 3
        if k[pg.K_s]: new_g.y += 3
        if k[pg.K_a]: new_g.x -= 3
        if k[pg.K_d]: new_g.x += 3
        if MAP[int(new_g.y//TILE_SIZE)][int(new_g.x//TILE_SIZE)] == 0:
            g_pos = new_g

        # --- ЛОГІКА БОТА-ПРИВИДА (РАНДОМ) ---
        new_bot_pos = bot_pos + bot_dir
        # Перевірка на стіну: якщо попереду стіна, змінити напрямок
        if MAP[int(new_bot_pos.y//TILE_SIZE)][int(new_bot_pos.x//TILE_SIZE)] == 1:
            bot_dir = random.choice([pg.Vector2(0, 2), pg.Vector2(0, -2), pg.Vector2(2, 0), pg.Vector2(-2, 0)])
        else:
            bot_pos = new_bot_pos
            # Невеликий шанс змінити напрямок на перехресті (щоб бот не ходив по колу)
            if random.random() < 0.02: 
                bot_dir = random.choice([pg.Vector2(0, 2), pg.Vector2(0, -2), pg.Vector2(2, 0), pg.Vector2(-2, 0)])

        # Збирання точок
        for d in dots[:]:
            if p_pos.distance_to(d) < 15:
                dots.remove(d)

        # Перевірка умов завершення
        if not dots:
            game_state = "WIN"
        if p_pos.distance_to(g_pos) < 25 or p_pos.distance_to(bot_pos) < 25:
            game_state = "GAMEOVER"

        # --- МАЛЮВАННЯ ---
        for r in range(len(MAP)):
            for c in range(len(MAP[r])):
                if MAP[r][c] == 1:
                    pg.draw.rect(screen, BLUE, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
        
        for dot in dots:
            pg.draw.circle(screen, WHITE, (int(dot.x), int(dot.y)), 4)

        pg.draw.circle(screen, YELLOW, (int(p_pos.x), int(p_pos.y)), 14) # Пакмен
        pg.draw.rect(screen, RED, (int(g_pos.x)-14, int(g_pos.y)-14, 28, 28)) # Привид-гравець
        pg.draw.rect(screen, GREEN, (int(bot_pos.x)-14, int(bot_pos.y)-14, 28, 28)) # БОТ

    elif game_state == "WIN":
        draw_text("ПЕРЕМОГА!", font_big, YELLOW)
        draw_text("Натисніть ПРОБІЛ, щоб почати знову", font_small, WHITE, 60)

    elif game_state == "GAMEOVER":
        draw_text("ГРА ЗАКІНЧЕНА!", font_big, RED)
        draw_text("Вас спіймали! Натисніть ПРОБІЛ", font_small, WHITE, 60)

    pg.display.update()
    clock.tick(60)