"""Тесты базового поведения змейки."""

from snake_game.snake import Snake


def test_move_changes_head_and_direction() -> None:
    """Ход перемещает голову и обновляет направление."""
    snake = Snake((2, 2), (1, 0))

    snake.move(0, -1)

    assert snake.head() == (2, 1)
    assert snake.direction == (0, -1)


def test_growth_keeps_tail_on_next_move() -> None:
    """После роста длина змейки увеличивается на один сегмент."""
    snake = Snake((1, 1), (1, 0))
    snake.grow()

    snake.move(1, 0)

    assert len(snake.body) == 2
    assert snake.body == [(2, 1), (1, 1)]


def test_self_collision_after_moving_in_a_loop() -> None:
    """Движение по замкнутому пути приводит к самопересечению."""
    snake = Snake((1, 1), (1, 0))
    for _ in range(4):
        snake.grow()

    snake.move(1, 0)
    snake.move(0, 1)
    snake.move(-1, 0)
    snake.move(0, -1)

    assert snake.collides_self()
