import pygame as pg
import sys

# 1. Ініціалізація
pg.init()
WIDTH, HEIGHT = 600, 400
screen = pg.display.set_caption("PACMAN vs GHOST")
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# 2. Кольори та Налаштування
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TILE_SIZE = 40

# 3. Карта (1-стіна, 0-точка)
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

# Створюємо список точок
dots = []
for r in range(len(MAP)):
    for c in range(len(MAP[r])):
        if MAP[r][c] == 0:
            dots.append(pg.Vector2(c * TILE_SIZE + 20, r * TILE_SIZE + 20))

# Позиції гравців
p_pos = pg.Vector2(60, 60)
g_pos = pg.Vector2(540, 300)

# 4. Головний цикл
while True:
    screen.fill(BLACK) # Очищення екрана в кожному кадрі
    
    # Малюємо стіни
    for r in range(len(MAP)):
        for c in range(len(MAP[r])):
            if MAP[r][c] == 1:
                pg.draw.rect(screen, BLUE, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
    
    # Малюємо точки
    for dot in dots:
        pg.draw.circle(screen, WHITE, (int(dot.x), int(dot.y)), 4)

    # Обробка виходу
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Керування
    k = pg.key.get_pressed()
    
    # Рух Пакмена (Стрілочки)
    new_p = p_pos + pg.Vector2(0,0)
    if k[pg.K_UP]:    new_p.y -= 3
    if k[pg.K_DOWN]:  new_p.y += 3
    if k[pg.K_LEFT]:  new_p.x -= 3
    if k[pg.K_RIGHT]: new_p.x += 3
    
    # Перевірка стін для Пакмена
    if MAP[int(new_p.y//TILE_SIZE)][int(new_p.x//TILE_SIZE)] == 0:
        p_pos = new_p

    # Рух Привида (WASD)
    new_g = g_pos + pg.Vector2(0,0)
    if k[pg.K_w]: new_g.y -= 3
    if k[pg.K_s]: new_g.y += 3
    if k[pg.K_a]: new_g.x -= 3
    if k[pg.K_d]: new_g.x += 3
    
    # Перевірка стін для Привида
    if MAP[int(new_g.y//TILE_SIZE)][int(new_g.x//TILE_SIZE)] == 0:
        g_pos = new_g

    # Малюємо персонажів
    pg.draw.circle(screen, YELLOW, (int(p_pos.x), int(p_pos.y)), 14) # Пакмен
    pg.draw.rect(screen, RED, (int(g_pos.x)-14, int(g_pos.y)-14, 28, 28)) # Привид

    # Логіка збирання точок
    for d in dots[:]:
        if p_pos.distance_to(d) < 15:
            dots.remove(d)

    # Умова перемоги (всі з'їв)
    if not dots:
        print("WIN!")
        pg.quit()
        sys.exit()

    # Умова смерті (зловив)
    if p_pos.distance_to(g_pos) < 25:
        print("GAME OVER!")
        pg.quit()
        sys.exit()

    pg.display.update() # ВАЖЛИВО: Оновлюємо вікно
    clock.tick(60)