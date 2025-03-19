import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random


# +
# Звезда


def generate_star(n_rays, inner_radius, outer_radius):
    """
    Генерирует координаты звезды.
    n_rays: количество лучей
    inner_radius: радиус внутренних точек
    outer_radius: радиус внешних точек
    """
    angles = np.linspace(0, 2 * np.pi, 2 * n_rays, endpoint=False)  # Углы
    radii = np.array([outer_radius if i % 2 == 0 else inner_radius for i in range(2 * n_rays)])
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    return x, y


n_rays = random.randint(5, 15)  # Случайное количество лучей
inner_radius = random.uniform(0.2, 0.5)  # Случайный радиус внутренних точек
outer_radius = random.uniform(0.6, 1.0)  # Случайный радиус внешних точек

colors = [random.choice(['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink']) for _ in range(n_rays)]

# Генерация
x, y = generate_star(n_rays, inner_radius, outer_radius)

# Настройка графика
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal', 'box')
ax.set_title("Анимация звезды")
ax.axis('off')

patches = []

# секторы звезды
for i in range(2 * n_rays - 1):
    patch, = ax.fill([0], [0], color=colors[i // 2], alpha=0.8)
    patches.append(patch)


def init():
    for patch in patches:
        patch.set_xy([[0, 0], [0, 0], [0, 0]])
    return patches


# обновление кадров
def update(frame):
    for i, patch in enumerate(patches[:frame + 1]):
        if i < len(x) - 1:
            patch.set_xy([[0, 0], [x[i], y[i]], [x[i + 1], y[i + 1]]])
    return patches


# анимация
frames = len(x) - 1
ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=100)

plt.show()
