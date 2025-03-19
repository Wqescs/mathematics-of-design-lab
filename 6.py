import pygame
import math
import random

pygame.init()

# Окно
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0),  # Красный
    (0, 255, 0),  # Зеленый
    (0, 0, 255),  # Синий
    (255, 255, 0),  # Желтый
]

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Замощение")

# Генерация случайного цвета
def random_color():
    return random.choice(COLORS)

# Треугольник (равносторонний)
def draw_triangle(x, y, size, color, inverted=False):
    points = [
        (x, y),
        (x + size, y),
        (x + size // 2, y - int(size * math.sqrt(3) / 2))
    ]
    if inverted:
        points = [
            (x, y + int(size * math.sqrt(3) / 2)),
            (x + size, y + int(size * math.sqrt(3) / 2)),
            (x + size // 2, y + int(size * math.sqrt(3) / 2) - int(size * math.sqrt(3) / 2))
        ]
    pygame.draw.polygon(screen, color, points)

# Квадрат
def draw_square(x, y, size, color):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, size, size))

# Замощение треугольниками
def tile_with_triangles(x, y, step, size, colors):
    count = 0
    inverted = False  # Переключение между нормальными и перевернутыми треугольниками
    for row in range(y, y + step * int(size * math.sqrt(3) / 2), int(size * math.sqrt(3) / 2)):
        for col in range(x, x + step * size, size):
            if count >= step:
                return count
            draw_triangle(col, row, size, colors[count % len(colors)], inverted)
            count += 1
            inverted = not inverted  # Переключаем ориентацию треугольников
    return count

# Замощение квадратами
def tile_with_squares(x, y, step, size, colors):
    count = 0
    for row in range(y, y + step * size, size):
        for col in range(x, x + step * size, size):
            if count >= step:
                return count
            draw_square(col, row, size, colors[count % len(colors)])
            count += 1
    return count

running = True
clock = pygame.time.Clock()

# Случайный выбор замощения
tiling_type = random.choice(["triangle", "square"])

# Случайное определение области для замощения
x_pos = random.randint(0, WIDTH // 2)
y_pos = random.randint(0, HEIGHT // 2)
step = random.randint(5, 10)  # Сколько фигур замостить в строке
size = 50  # Размер фигуры

# Цвета
colors = [random_color() for _ in range(1000)]  # Предварительно сгенерированные цвета

# Анимация
count = 0  # Сколько фигур уже нарисовано

while running:
    screen.fill(WHITE)

    # Замощение в случайной области
    if tiling_type == "triangle":
        count = tile_with_triangles(x_pos, y_pos, step, size, colors)
    elif tiling_type == "square":
        count = tile_with_squares(x_pos, y_pos, step, size, colors)

    # Увеличение количества фигур в анимации
    count += 1

    # Обновление экрана
    pygame.display.flip()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)

pygame.quit()
