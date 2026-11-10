# Змейка в терминале

Консольная игра «Змейка» на Python. Змейка растёт, когда ест, игра завершается столкновением со стеной или своим телом.

## Требования

Python 3.11 или новее, uv.

## Установка

```bash
uv sync --group dev
```

## Запуск

```bash
uv run --group dev python snake.py --width 20 --height 15 --speed 8
```

Для более спокойной игры можно уменьшить скорость, например до 4:

```bash
uv run --group dev python snake.py --width 20 --height 15 --speed 4
```

Стрелки или WASD — движение, `P` — пауза, `Q` — выход. На экране Game Over нажмите `Y`, чтобы сыграть ещё раз.

## Тесты и проверки

```bash
uv run --group dev pytest
uv run --group dev ruff check .
uv run --group dev ruff format --check .
uv run --group dev mypy --strict snake_game tests snake.py
```