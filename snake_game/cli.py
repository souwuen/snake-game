"""Отрисовка игры и управление из терминала."""

import argparse
import curses
import time

from snake_game.game import Game
from snake_game.snake import Point


def _write(stdscr: curses.window, row: int, text: str) -> None:
    """Безопасно выводит строку, не выходя за границы окна."""
    height, width = stdscr.getmaxyx()
    if 0 <= row < height and width > 1:
        stdscr.addstr(row, 0, text[: width - 1])


def _draw(
    stdscr: curses.window,
    game: Game,
    footer: tuple[str, ...] = (),
) -> bool:
    """Рисует поле; возвращает False, если окно слишком мало."""
    screen_height, screen_width = stdscr.getmaxyx()
    required_height = game.height + 4 + len(footer)
    required_width = game.width + 3

    stdscr.erase()
    if screen_height < required_height or screen_width < required_width:
        _write(
            stdscr,
            0,
            f"Увеличьте окно: нужно минимум {required_width}x{required_height}.",
        )
        stdscr.refresh()
        return False

    lines = ["+" + "-" * game.width + "+"]
    for y in range(game.height):
        row = [" "] * game.width

        for x, body_y in game.snake.body[1:]:
            if body_y == y and 0 <= x < game.width:
                row[x] = "o"

        head_x, head_y = game.snake.head()
        if head_y == y and 0 <= head_x < game.width:
            row[head_x] = "@"

        if game.food is not None and game.food[1] == y:
            row[game.food[0]] = "*"

        lines.append("|" + "".join(row) + "|")

    lines.append("+" + "-" * game.width + "+")
    for row_number, line in enumerate(lines):
        _write(stdscr, row_number, line)

    _write(stdscr, game.height + 2, f"Счёт: {game.score}  Уровень: {game.level}")
    _write(stdscr, game.height + 3, "Стрелки/WASD — ход, P — пауза, Q — выход")

    for index, line in enumerate(footer):
        _write(stdscr, game.height + 4 + index, line)

    stdscr.refresh()
    return True


def _pause(stdscr: curses.window, game: Game) -> bool:
    """Ожидает продолжения после паузы; False означает выход."""
    stdscr.timeout(100)
    while True:
        _draw(stdscr, game, ("Пауза: P — продолжить, Q — выйти",))
        key = stdscr.getch()

        if key in (ord("p"), ord("P")):
            return True
        if key in (ord("q"), ord("Q")):
            return False


def _game_over(stdscr: curses.window, game: Game) -> bool:
    """Показывает итог и возвращает выбор о повторной игре."""
    stdscr.timeout(100)
    footer = (
        f"Игра окончена! Счёт: {game.score}",
        "Y — сыграть ещё раз, Q — выйти",
    )
    while True:
        _draw(stdscr, game, footer)
        key = stdscr.getch()

        if key in (ord("y"), ord("Y")):
            return True
        if key in (ord("q"), ord("Q")):
            return False


def _play(stdscr: curses.window, width: int, height: int, speed: float) -> bool:
    """Запускает раунд с фиксированным интервалом движения."""
    game = Game(width, height, speed)
    directions: dict[int, Point] = {
        curses.KEY_UP: (0, -1),
        curses.KEY_DOWN: (0, 1),
        curses.KEY_LEFT: (-1, 0),
        curses.KEY_RIGHT: (1, 0),
        ord("w"): (0, -1),
        ord("s"): (0, 1),
        ord("a"): (-1, 0),
        ord("d"): (1, 0),
        ord("W"): (0, -1),
        ord("S"): (0, 1),
        ord("A"): (-1, 0),
        ord("D"): (1, 0),
    }

    direction = game.snake.direction
    next_move = time.monotonic() + game.tick

    while not game.is_over:
        if not _draw(stdscr, game):
            stdscr.timeout(100)
            if stdscr.getch() in (ord("q"), ord("Q")):
                return False
            continue

        remaining = max(0.0, next_move - time.monotonic())
        stdscr.timeout(max(1, int(remaining * 1000)))
        key = stdscr.getch()

        if key in (ord("q"), ord("Q")):
            return False

        if key in (ord("p"), ord("P")):
            remaining = max(0.0, next_move - time.monotonic())
            if not _pause(stdscr, game):
                return False
            next_move = time.monotonic() + remaining
            continue

        if key in directions:
            direction = directions[key]

        now = time.monotonic()
        if now >= next_move:
            game.step(direction)
            next_move = now + game.tick

    return _game_over(stdscr, game)


def main() -> None:
    """Разбирает аргументы и запускает игру."""
    parser = argparse.ArgumentParser(description="Змейка в терминале")
    parser.add_argument("--width", type=int, default=20, help="ширина поля")
    parser.add_argument("--height", type=int, default=15, help="высота поля")
    parser.add_argument("--speed", type=float, default=8, help="ходов в секунду")
    args = parser.parse_args()

    try:
        while curses.wrapper(_play, args.width, args.height, args.speed):
            pass
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
