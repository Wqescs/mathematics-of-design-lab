import pygame
import random
import math

# Шарики
# Константы
WIDTH, HEIGHT = 800, 600
SPEED_MIN = 0.2
SPEED_MAX = 0.4
ANGLE_DEVIATION = 15  # max отклонение

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Ball:
    def __init__(self, radius):
        self.radius = radius
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.dx = random.uniform(-SPEED_MAX, SPEED_MAX)  # скорость по X
        self.dy = random.uniform(-SPEED_MAX, SPEED_MAX)  # скорость по Y
        # RGB
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # проверка на столкновение
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.dx *= -1  # отталкивание от левой или правой границы
            self.random_deviation()  # случайное отклонение

        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.dy *= -1  # отталкивание от верхней или нижней границы
            self.random_deviation()  # случайное отклонение

    def random_deviation(self):
        angle = random.uniform(-ANGLE_DEVIATION, ANGLE_DEVIATION) * (math.pi / 180)  # Переводим градусы в радианы
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)  # скорость
        new_dx = speed * math.cos(angle)  # Новая скорость по X с учетом отклонения
        new_dy = speed * math.sin(angle)  # Новая скорость по Y с учетом отклонения

        # с учетом отклонения
        if self.dx < 0:
            new_dx *= -1
        if self.dy < 0:
            new_dy *= -1

        self.dx += new_dx * random.choice([-1, 1]) * (random.random() * 0.5)  # Случайное изменение скорости по X
        self.dy += new_dy * random.choice([-1, 1]) * (random.random() * 0.5)  # Случайное изменение скорости по Y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


def check_collision(ball1, ball2):
    distance = math.sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)
    return distance < (ball1.radius + ball2.radius)


def resolve_collision(ball1, ball2):
    # Вектор между центрами шариков
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance == 0:
        return

    # Нормализуем вектор
    nx = dx / distance
    ny = dy / distance

    # Отталкивание
    overlap = (ball1.radius + ball2.radius) - distance
    ball1.x -= nx * overlap / 2
    ball1.y -= ny * overlap / 2
    ball2.x += nx * overlap / 2
    ball2.y += ny * overlap / 2

    # Обмен скоростями
    ball1.dx, ball2.dx = ball2.dx, ball1.dx
    ball1.dy, ball2.dy = ball2.dy, ball1.dy

    # случайное отклонение после столкновения.
    ball1.random_deviation()
    ball2.random_deviation()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Броуновское движение шариков")

    balls = []

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # "R" для случайной генерации шариков
                    num_balls = random.randint(5, 30)  # Случайное количество шариков от 5 до 30
                    radius_list = [random.randint(5, 20) for _ in range(num_balls)]  # Случайные радиусы от 5 до 20
                    balls = [Ball(radius) for radius in radius_list]
                    print(f"Случайно сгенерировано {num_balls} шариков с радиусами {radius_list}.")

                elif event.key == pygame.K_e:  # "E" для задания количества шариков вручную
                    num_balls_input = input("Введите количество шариков (от 5 до 30): ")
                    try:
                        num_balls_input = int(num_balls_input)
                        if num_balls_input < 5 or num_balls_input > 30:
                            print("Пожалуйста, введите число от 5 до 30.")
                        else:
                            radius_list = []
                            for i in range(num_balls_input):
                                radius_input = input(f"Введите радиус для шарика {i + 1} (от 5 до 20): ")
                                radius_list.append(int(radius_input))
                            balls = [Ball(radius) for radius in radius_list]
                            print(f"Сгенерировано {num_balls_input} шариков с радиусами {radius_list}.")
                    except ValueError:
                        print("Пожалуйста, введите корректное целое число.")

        screen.fill(WHITE)

        for i in range(len(balls)):
            balls[i].move()
            balls[i].draw(screen)

            for j in range(i + 1, len(balls)):
                if check_collision(balls[i], balls[j]):
                    resolve_collision(balls[i], balls[j])

        # Отображение количества шариков
        text_surface = font.render(f"Количество шариков: {len(balls)}", True, BLACK)
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
