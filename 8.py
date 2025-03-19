import pygame
import random
import sys

# +
# Лабиринт
# Параметры
CELL_SIZE = 20  # Размер клетки в пикселях

# Цвета
COLOR_WALL = (0, 0, 0)
COLOR_PATH = (255, 255, 255)
COLOR_VISITED = (200, 200, 200)  # Цвет для посещенных клеток


def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        maze[y][x] = 0  # Отметить текущую клетку как проход
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0  # Удалить стену
                carve(nx, ny)

    maze[1][1] = 0
    carve(1, 1)
    return maze


def set_entry_exit(maze):
    entry = (0, random.randint(1, len(maze[0]) - 2))
    exit = (len(maze) - 1, random.randint(1, len(maze[0]) - 2))
    maze[entry[0]][entry[1]] = 0
    maze[exit[0]][exit[1]] = 0
    return entry, exit


def draw_maze(screen, maze):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 1:
                color = COLOR_WALL
            elif maze[row][col] == -1:  # Если клетка посещена во время генерации
                color = COLOR_VISITED
            else:
                color = COLOR_PATH

            pygame.draw.rect(screen,
                             color,
                             (col * CELL_SIZE, row * CELL_SIZE,
                              CELL_SIZE - 1, CELL_SIZE - 1))  # -1 для разделения клеток


def animate_maze_generation(screen, width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        maze[y][x] = -1  # Отметить текущую клетку как посещенную для анимации
        draw_maze(screen, maze)  # Отрисовка текущего состояния лабиринта
        pygame.display.flip()  # Обновление экрана
        pygame.time.delay(50)  # Задержка для анимации

        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = -1  # Удалить стену и отметить как посещенную
                carve(nx, ny)

    carve(1, 1)  # Начинаем с координат (1,1)
    return maze


def main():
    # Запрос размеров лабиринта у пользователя
    while True:
        try:
            width = int(input("Введите ширину лабиринта (нечетное число): "))
            height = int(input("Введите высоту лабиринта (нечетное число): "))

            if width % 2 == 0 or height % 2 == 0 or width < 5 or height < 5:
                print("Ширина и высота должны быть нечетными числами и больше или равны 5.")
                continue

            break

        except ValueError:
            print("Пожалуйста, введите корректные целые числа.")

    pygame.init()
    screen = pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE))
    pygame.display.set_caption("Случайный Лабиринт")

    # Генерация лабиринта с анимацией
    maze = animate_maze_generation(screen, width, height)

    entry, exit = set_entry_exit(maze)

    print(f"Вход: {entry}, Выход: {exit}")

    # Основной цикл программы после генерации лабиринта
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Фон белый

        draw_maze(screen, maze)  # Отрисовка финального лабиринта

        pygame.display.flip()  # Обновление экрана

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

