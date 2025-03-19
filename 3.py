import pygame
import numpy as np
import math

pygame.init()
# Фракталы

# окно
WIDTH, HEIGHT = 800, 600

# параметры для Мандельброта и Жюлиа
ZOOM = 200
OFFSET_X, OFFSET_Y = -WIDTH // 2, -HEIGHT // 2
MAX_ITER = 100
GROWTH_RADIUS = 1
MAX_RADIUS = 2
JULIA_C = complex(-0.7, 0.27015)  # Параметр для множества Жюлиа

# параметры для Дракона Хартера-Хейтуэя
LEVI_MAX_DEPTH = 16
LEVI_POINTS = [(WIDTH // 2, HEIGHT // 2 - 200), (WIDTH // 2 + 200, HEIGHT // 2)]

# Параметры для Треугольника Серпинского
SIERPINSKI_MAX_DEPTH = 8
SIERPINSKI_POINTS = [(WIDTH // 2, 50), (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50)]

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Фракталы")


# Цвета
def get_color(iteration, max_iter):
    if iteration == max_iter:
        return (0, 0, 0)
    color = int(255 * iteration / max_iter)
    return (color, 0, 255 - color)


# множество Мандельброта
def fractal(z, c, max_iter, max_radius):
    for n in range(max_iter):
        if abs(z) > max_radius:
            return n
        z = z * z + c
    return max_iter


# рисование множества Мандельброта
def draw_mandelbrot(current_radius):
    coords = np.array([[complex((x + OFFSET_X) / ZOOM, (y + OFFSET_Y) / ZOOM)
                        for x in range(WIDTH)] for y in range(HEIGHT)])
    for y in range(HEIGHT):
        for x in range(WIDTH):
            c = coords[y][x]
            iter_count = fractal(0, c, MAX_ITER, current_radius)
            color = get_color(iter_count, MAX_ITER)
            screen.set_at((x, y), color)


# рисование множества Жюлиа
def draw_julia(current_radius):
    coords = np.array([[complex((x + OFFSET_X) / ZOOM, (y + OFFSET_Y) / ZOOM)
                        for x in range(WIDTH)] for y in range(HEIGHT)])
    for y in range(HEIGHT):
        for x in range(WIDTH):
            z = coords[y][x]
            iter_count = fractal(z, JULIA_C, MAX_ITER, current_radius)
            color = get_color(iter_count, MAX_ITER)
            screen.set_at((x, y), color)


# генерация Леви
def levi_curve(points, depth):
    if depth == 0:
        return points
    new_points = []
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        dx = x2 - x1
        dy = y2 - y1
        new_x = mid_x - dy / 2
        new_y = mid_y + dx / 2
        new_points.extend([(x1, y1), (new_x, new_y)])
    new_points.append(points[-1])
    return levi_curve(new_points, depth - 1)


# рисование Леви
def draw_levi(depth):
    points = levi_curve(LEVI_POINTS, depth)
    for i in range(len(points) - 1):
        pygame.draw.line(screen, (255, 255, 255), points[i], points[i + 1], 1)


# генерация Треугольника Серпинского
def sierpinski(points, depth):
    if depth == 0:
        pygame.draw.polygon(screen, (255, 255, 255), points, 0)
    else:
        mid1 = ((points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2)
        mid2 = ((points[1][0] + points[2][0]) / 2, (points[1][1] + points[2][1]) / 2)
        mid3 = ((points[2][0] + points[0][0]) / 2, (points[2][1] + points[0][1]) / 2)
        sierpinski([points[0], mid1, mid3], depth - 1)
        sierpinski([points[1], mid1, mid2], depth - 1)
        sierpinski([points[2], mid2, mid3], depth - 1)


# Главный игровой цикл
running = True
clock = pygame.time.Clock()

# Выбор фрактала: 1 - Мандельброт, 2 - Жюлиа, 3 - Леви, 4 - Серпинский
current_fractal = 4
current_radius = GROWTH_RADIUS
current_levi_depth = 1
current_sierpinski_depth = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_fractal = 1
                current_radius = GROWTH_RADIUS
            elif event.key == pygame.K_2:
                current_fractal = 2
                current_radius = GROWTH_RADIUS
            elif event.key == pygame.K_3:
                current_fractal = 3
                current_levi_depth = 1
            elif event.key == pygame.K_4:
                current_fractal = 4
                current_sierpinski_depth = 1


    screen.fill((0, 0, 0))

    if current_fractal == 1:  # Мандельброт
        if current_radius < MAX_RADIUS:
            draw_mandelbrot(current_radius)
            current_radius += 0.25
        else:
            draw_mandelbrot(current_radius)
    elif current_fractal == 2:  # Жюлиа
        if current_radius < MAX_RADIUS:
            draw_julia(current_radius)
            current_radius += 0.25
        else:
            draw_julia(current_radius)
    elif current_fractal == 3:  # Леви
        if current_levi_depth <= LEVI_MAX_DEPTH:
            draw_levi(current_levi_depth)
            current_levi_depth += 1
        else:
            draw_levi(current_levi_depth)
    elif current_fractal == 4:  # Серпинский
        if current_sierpinski_depth <= SIERPINSKI_MAX_DEPTH:
            sierpinski(SIERPINSKI_POINTS, current_sierpinski_depth)
            current_sierpinski_depth += 1
        else:
            sierpinski(SIERPINSKI_POINTS, current_sierpinski_depth)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
