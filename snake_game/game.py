"""Правила игры, игровое поле, еда и счёт."""

import random

from snake_game.snake import Point, Snake


class Game:
    """Управляет состоянием одного раунда."""

    def __init__(self, w: int, h: int, speed: float) -> None:
        """Создаёт поле и размещает змейку с едой."""
        if w < 3 or h < 3:
            raise ValueError("Ширина и высота поля должны быть не меньше 3.")
        if speed <= 0:
            raise ValueError("Скорость должна быть больше нуля.")

        self.width = w
        self.height = h
        self.speed = speed
        self.snake = Snake((w // 2, h // 2), (1, 0))
        self.score = 0
        self._is_over = False
        self.food = self.spawn_food()

    @property
    def is_over(self) -> bool:
        """Возвращает True, если раунд завершён."""
        return self._is_over

    @property
    def level(self) -> int:
        """Повышает уровень за каждые пять очков."""
        return self.score // 5 + 1

    @property
    def tick(self) -> float:
        """Возвращает интервал между ходами с учётом уровня."""
        return max(0.05, 1 / self.speed * 0.9 ** (self.level - 1))

    def spawn_food(self) -> Point | None:
        """Выбирает случайную свободную клетку для еды."""
        free_cells = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in self.snake.body
        ]
        return random.choice(free_cells) if free_cells else None

    def step(self, direction: Point) -> None:
        """Делает один игровой ход и проверяет столкновения."""
        if self.is_over:
            return

        if direction not in {(0, -1), (0, 1), (-1, 0), (1, 0)}:
            raise ValueError("Направление должно указывать на соседнюю клетку.")

        current_dx, current_dy = self.snake.direction
        if len(self.snake.body) > 1 and direction == (-current_dx, -current_dy):
            direction = self.snake.direction

        dx, dy = direction
        head_x, head_y = self.snake.head()
        next_head = (head_x + dx, head_y + dy)
        eating = next_head == self.food

        if eating:
            self.snake.grow()
        self.snake.move(dx, dy)

        x, y = self.snake.head()
        hit_wall = x < 0 or x >= self.width or y < 0 or y >= self.height
        if hit_wall or self.snake.collides_self():
            self._is_over = True
            return

        if eating:
            self.score += 1
            self.food = self.spawn_food()
            if self.food is None:
                self._is_over = True
