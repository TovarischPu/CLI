"""Модуль с моделью конфигурации приложения."""

from dataclasses import dataclass


@dataclass
class AppConfig:
    """Конфигурация, собираемая из аргументов командной строки."""

    package: str
    source: str
    test_mode: bool
    ascii_tree: bool
    max_depth: int
    filter_substring: str

    def as_key_value(self) -> str:
        lines = [
            f"package          = {self.package}",
            f"source           = {self.source}",
            f"test_mode        = {self.test_mode}",
            f"ascii_tree       = {self.ascii_tree}",
            f"max_depth        = {self.max_depth}",
            f"filter_substring = {self.filter_substring!r}",
        ]
        return "\n".join(lines)