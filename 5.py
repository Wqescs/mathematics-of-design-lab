import pygame
import numpy as np
import random
import math

pygame.init()
# Кораблик
# Окно
WIDTH, HEIGHT = 1000, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (34, 177, 76)
BLACK = (0, 0, 0)

# Параметры корабля
ship_width = 100
ship_height = 30
mast_height = 50  # Высота мачты
sail_width = 40  # Ширина паруса
trapezoid_bottom_width = 60  # Нижняя ширина трапеции

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Корабль")


# генерация волны
def generate_wave(amplitude, frequency, phase_shift, wave_type='sin'):
    x_vals = np.linspace(0, WIDTH, WIDTH)
    if wave_type == 'sin':
        y_vals = amplitude * np.sin(frequency * x_vals + phase_shift)
    elif wave_type == 'cos':
        y_vals = amplitude * np.cos(frequency * x_vals + phase_shift)
    return x_vals, y_vals


# рисование корабля
def draw_ship(x, y, width, height, angle):
    # Создаем поверхность для корабля
    ship_surface = pygame.Surface((width, height + mast_height), pygame.SRCALPHA)

    # Рисуем корпус корабля (перевернутая трапеция)
    bottom_offset = (width - trapezoid_bottom_width) // 2
    pygame.draw.polygon(
        ship_surface,
        BLUE,
        [
            (0, mast_height),  # Верхний левый угол
            (width, mast_height),  # Верхний правый угол
            (width - bottom_offset, mast_height + height),  # Нижний правый угол
            (bottom_offset, mast_height + height)  # Нижний левый угол
        ]
    )

    # мачта
    mast_x = width // 2
    pygame.draw.line(ship_surface, BLACK, (mast_x, mast_height), (mast_x, 0), 3)

    #парус
    pygame.draw.polygon(
        ship_surface, GREEN,
        [(mast_x, 0), (mast_x - sail_width, mast_height // 2), (mast_x, mast_height // 2)]
    )

    #Наклон
    ship_surface = pygame.transform.rotate(ship_surface, angle+5)
    rotated_rect = ship_surface.get_rect(center=(x, y))
    screen.blit(ship_surface, rotated_rect.topleft)


running = True
clock = pygame.time.Clock()

# Параметры волны
amplitude = random.randint(10, 20)  # Уменьшенная амплитуда волны (меньше высота)
frequency = random.uniform(0.005, 0.02)  # Уменьшенная частота волны (длиннее волны)
phase_shift = random.uniform(0, 2 * math.pi)  # Сдвиг фазы
wave_type = random.choice(['sin', 'cos'])  # Тип волны

# Скорость корабля
ship_position = [0, HEIGHT // 2]  # Начальная позиция корабля
ship_speed = 3

while running:
    screen.fill(WHITE)

    # Генерация координат волны
    x_vals, y_vals = generate_wave(amplitude, frequency, phase_shift, wave_type)

    # Рисование волны
    for i in range(WIDTH - 1):
        pygame.draw.line(screen, BLUE, (x_vals[i], HEIGHT // 2 - int(y_vals[i])),
                         (x_vals[i + 1], HEIGHT // 2 - int(y_vals[i + 1])), 2)

    # Движение корабля
    ship_position[0] += ship_speed
    if ship_position[0] > WIDTH + ship_width:  # Если корабль выходит за экран
        ship_position[0] = -ship_width

    # Высота волны в текущей позиции корабля
    wave_height = y_vals[int(ship_position[0] % WIDTH)]
    ship_angle = -wave_height / 5  # Угол наклона в зависимости от высоты волны

    # Позиция корабля
    ship_y = HEIGHT // 2 - wave_height - ship_height // 2  # Учитываем высоту корпуса
    draw_ship(ship_position[0], ship_y, ship_width, ship_height, ship_angle)

    # Обновление экрана
    pygame.display.flip()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)

pygame.quit()
