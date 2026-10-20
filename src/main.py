"""Точка входа CLI-приложения."""

import sys
from typing import Sequence

from .cli import safe_parse_args
from .validation import ValidationError


def run(argv: Sequence[str]) -> int:
    """Запустить приложение и вернуть код возврата."""
    try:
        config = safe_parse_args(argv)
    except ValidationError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    print("=== Конфигурация приложения ===")
    print(config.as_key_value())
    print("=== Конец конфигурации ===")
    return 0


def main() -> None:
    """Обёртка для запуска из командной строки."""
    sys.exit(run(sys.argv[1:]))


if __name__ == "__main__":
    main()