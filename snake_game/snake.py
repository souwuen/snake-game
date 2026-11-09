"""Тело змейки и базовая логика движения."""

from typing import TypeAlias

Point: TypeAlias = tuple[int, int]


class Snake:
    """Хранит сегменты змейки и перемещает её по клеткам."""

    def __init__(self, start_pos: Point, direction: Point) -> None:
        """Создаёт змейку из одного сегмента."""
        self.body: list[Point] = [start_pos]
        self.direction = direction
        self._growth_pending = 0

    def head(self) -> Point:
        """Возвращает координаты головы."""
        return self.body[0]

    def move(self, dx: int, dy: int) -> None:
        """Перемещает голову и при необходимости сохраняет хвост."""
        self.direction = (dx, dy)
        head_x, head_y = self.head()
        self.body.insert(0, (head_x + dx, head_y + dy))

        if self._growth_pending:
            self._growth_pending -= 1
        else:
            self.body.pop()

    def grow(self) -> None:
        """Откладывает рост на один сегмент до следующего движения."""
        self._growth_pending += 1

    def collides_self(self) -> bool:
        """Проверяет, занимает ли голова клетку другого сегмента."""
        return self.head() in self.body[1:]
