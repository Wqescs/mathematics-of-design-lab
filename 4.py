import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# +
# Случайные параметры снежинки
n_rays = random.randint(6, 10)  # Количество основных лучей
depth = random.randint(2, 4)  # Глубина разветвлений
color = random.choice(['blue', 'cyan', 'purple', 'pink', 'silver'])  # Цвет снежинки
angle_offset = random.uniform(0, 120)  # Случайный угол наклона


# луч с разветвлениями
def generate_branch(x, y, angle, depth, length):
    """
    Рекурсивное создание луча снежинки с подветвями.
    x, y: координаты начала
    angle: угол направления
    depth: текущая глубина рекурсии
    length: длина текущего луча
    """
    if depth == 0:
        return []

    # Конец текущего сегмента
    x_end = x + length * np.cos(angle)
    y_end = y + length * np.sin(angle)

    # Список сегментов (x1, y1, x2, y2)
    segments = [(x, y, x_end, y_end)]

    # Углы подветвей
    branch_angles = [angle - np.pi / 6, angle + np.pi / 6]
    branch_length = length * 0.6  # Укорочение подветвей

    for branch_angle in branch_angles:
        segments += generate_branch(x_end, y_end, branch_angle, depth - 1, branch_length)

    return segments


# Вся снежинка
def generate_snowflake(n_rays, depth, angle_offset, length=1):
    """
    Генерация снежинки с заданным количеством лучей и глубиной разветвлений.
    """
    segments = []
    angles = np.linspace(0, 2 * np.pi, n_rays, endpoint=False) + np.radians(angle_offset)
    for angle in angles:
        segments += generate_branch(0, 0, angle, depth, length)
    return segments


# Генерация снежинки
snowflake_segments = generate_snowflake(n_rays, depth, angle_offset)

# Анимация
fig, ax = plt.subplots()
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect('equal', 'box')
ax.axis('off')
ax.set_title("Снежинка с разветвлениями")
lines = [ax.plot([], [], color=color, lw=2)[0] for _ in snowflake_segments]


def init():
    for line in lines:
        line.set_data([], [])
    return lines


def update(frame):
    for i in range(frame + 1):
        x1, y1, x2, y2 = snowflake_segments[i]
        lines[i].set_data([x1, x2], [y1, y2])
    return lines


# Анимация
ani = FuncAnimation(fig, update, frames=len(snowflake_segments), init_func=init, blit=True, interval=50)

plt.show()
