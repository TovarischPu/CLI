import re
from urllib.parse import urlparse


class ValidationError(Exception):
    """Исключение для ошибок валидации конфигурации."""


_URL_PATTERN = re.compile(r"^https?://", re.IGNORECASE)
_MIN_DEPTH = 1
_MAX_DEPTH = 100


def validate_package(package: str) -> str:
    if not package or not package.strip():
        raise ValidationError("Имя пакета не может быть пустым")
    return package.strip()

def validate_source(source: str, test_mode: bool) -> str:
    if not source or not source.strip():
        raise ValidationError("Источник данных не указан")
    source = source.strip()
    if test_mode:
        return source
    if not _URL_PATTERN.match(source):
        raise ValidationError(
            f"Источник должен быть URL (http/https): {source}"
        )
    return source

def validate_max_depth(depth: int) -> int:
    if depth < _MIN_DEPTH or depth > _MAX_DEPTH:
        raise ValidationError(
            f"Глубина должна быть в диапазоне "
            f"[{_MIN_DEPTH}, {_MAX_DEPTH}]"
        )
    return depth

def validate_filter(value: str) -> str:
    return "" if value is None else value