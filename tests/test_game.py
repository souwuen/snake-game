"""Тесты правил и состояния игры."""

import pytest

from snake_game.game import Game


def test_eating_food_grows_snake_and_increases_score() -> None:
    """Еда увеличивает длину змейки и счёт."""
    game = Game(10, 10, 8)
    game.food = (6, 5)

    game.step((1, 0))

    assert game.score == 1
    assert len(game.snake.body) == 2


def test_hitting_wall_ends_game() -> None:
    """Выход за край поля завершает раунд."""
    game = Game(5, 5, 1)
    game.food = (0, 0)

    game.step((1, 0))
    game.step((1, 0))
    game.step((1, 0))

    assert game.is_over


def test_reverse_direction_is_ignored_for_long_snake() -> None:
    """Змейка длиной больше одного не разворачивается на 180 градусов."""
    game = Game(10, 10, 2)
    game.food = (0, 0)
    game.snake.grow()
    game.step((1, 0))

    game.step((-1, 0))

    assert game.snake.head() == (7, 5)
    assert game.snake.direction == (1, 0)


def test_level_up_reduces_tick_interval() -> None:
    """С ростом уровня интервал между ходами уменьшается."""
    game = Game(10, 10, 8)
    first_level_tick = game.tick
    game.score = 5

    assert game.level == 2
    assert game.tick < first_level_tick


def test_food_uses_the_only_free_cell() -> None:
    """Еда появляется в единственной свободной клетке."""
    game = Game(3, 3, 4)
    game.snake.body = [
        (0, 0),
        (1, 0),
        (2, 0),
        (0, 1),
        (1, 1),
        (2, 1),
        (0, 2),
        (1, 2),
    ]

    for _ in range(20):
        assert game.spawn_food() == (2, 2)


def test_invalid_direction_raises_value_error() -> None:
    """Некорректное направление вызывает понятную ошибку."""
    game = Game(10, 10, 4)

    with pytest.raises(ValueError):
        game.step((1, 1))
