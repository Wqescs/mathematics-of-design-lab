import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# +
# Cпираль
def generate_spiral(theta_max, angle):
    """координаты"""
    theta = np.linspace(0, theta_max, 1000)  # Углы
    r = theta / (2 * np.pi)  # Радиус
    x = r * np.cos(angle * theta)
    y = r * np.sin(angle * theta)
    return x, y


angles = [1, 1.5, 2]  # Углы наклона
theta_max = 10 * np.pi  # Максимальный угол

print("Выберите угол для спирали:")
for i, angle in enumerate(angles, 1):
    print(f"{i}: {angle} π")
choice = int(input("Введите номер угла (1-3): "))
angle = angles[choice - 1]

# Генерация
x, y = generate_spiral(theta_max, angle)

# Настройка графика
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal', 'box')
ax.set_title("Анимация спирали")
ax.set_xlabel("X")
ax.set_ylabel("Y")

line, = ax.plot([], [], lw=2)


# Функция инициализации
def init():
    line.set_data([], [])
    return line,


def update(frame):
    line.set_data(x[:frame], y[:frame])
    return line,


frames = len(x)
ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=20)

plt.show()
