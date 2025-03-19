import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# +
# Случайные параметры
n_rays = random.randint(3, 7)  # Количество лучей (сторон) снежинки
order = random.randint(1, 4)  # Глубина снежинки
color = random.choice(['blue', 'cyan', 'purple', 'pink', 'silver'])  # Цвет
angle_offset = random.uniform(0, 360)  # Случайный угол наклона


# Функция для построения кривой Коха
def koch_curve(p1, p2, order):
    """
    Рекурсивно строит одну линию кривой Коха.
    p1, p2: начальные точки линии
    order: уровень рекурсии
    """
    if order == 0:
        return [p1, p2]
    else:
        # Разбиваем линию на 4 части
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = (x2 - x1) / 3, (y2 - y1) / 3

        # Точки деления
        pA = (x1 + dx, y1 + dy)
        pB = (x2 - dx, y2 - dy)

        # Вершина "треугольника"
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        peak_x = mid_x + (dy * (3 ** 0.5)) / 3
        peak_y = mid_y - (dx * (3 ** 0.5)) / 3
        pC = (peak_x, peak_y)

        # Рекурсивно строим сегменты
        return (koch_curve(p1, pA, order - 1) +
                koch_curve(pA, pC, order - 1) +
                koch_curve(pC, pB, order - 1) +
                koch_curve(pB, p2, order - 1))


# Функция для создания снежинки
def koch_snowflake(n_rays, order, angle_offset, scale=1):
    """
    Генерация снежинки Коха с несколькими лучами.
    n_rays: количество лучей (лучей/граней)
    order: уровень рекурсии
    angle_offset: угол наклона
    scale: размер снежинки
    """
    # Генерируем точки для многоугольника
    angles = np.linspace(0, 2 * np.pi, n_rays, endpoint=False) + np.radians(angle_offset)
    vertices = [(scale * np.cos(a), scale * np.sin(a)) for a in angles]
    vertices.append(vertices[0])  # Замыкаем фигуру

    # Создаем снежинку
    segments = []
    for i in range(len(vertices) - 1):
        segments += koch_curve(vertices[i], vertices[i + 1], order)

    return segments


# Генерация снежинки
snowflake_segments = koch_snowflake(n_rays, order, angle_offset)

# Анимация
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')
ax.axis('off')
ax.set_title("Снежинка Коха")

# Линии для анимации
lines = [ax.plot([], [], color=color, lw=1)[0] for _ in range(len(snowflake_segments) - 1)]

# Устанавливаем границы
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)


# Функция инициализации
def init():
    for line in lines:
        line.set_data([], [])
    return lines


# Функция обновления
def update(frame):
    for i in range(frame + 1):
        x1, y1 = snowflake_segments[i]
        x2, y2 = snowflake_segments[i + 1]
        lines[i].set_data([x1, x2], [y1, y2])
    return lines


# Анимация
ani = FuncAnimation(fig, update, frames=len(snowflake_segments) - 1, init_func=init, blit=True, interval=50)

plt.show()
