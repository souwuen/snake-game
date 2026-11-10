"""Тесты командного интерфейса."""

import sys
from io import StringIO

import pytest

from snake_game.cli import main


def test_main_reports_missing_terminal(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Без интерактивного терминала CLI выводит понятную ошибку."""
    monkeypatch.setattr(sys, "stdin", StringIO())
    monkeypatch.setattr(sys, "argv", ["snake.py"])

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
    assert "Запустите игру в терминале." in capsys.readouterr().err
