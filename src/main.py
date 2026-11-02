import sys
from typing import Sequence

from .cli import safe_parse_args
from .downloader import download_text
from .parser import build_pom_url, parse_direct_dependencies
from .validation import ValidationError


def run(argv: Sequence[str]) -> int:
    try:
        config = safe_parse_args(argv)
    except ValidationError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    print("=== Конфигурация приложения ===")
    print(config.as_key_value())
    print("=== Конец конфигурации ===")

    if config.test_mode:
        print("\n[INFO] Тестовый режим: скачивание пропущено.")
        return 0

    url = build_pom_url(config.source, config.package)
    print(f"\n[INFO] Загрузка pom.xml: {url}")
    
    try:
        xml_content = download_text(url)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    deps = parse_direct_dependencies(xml_content)
    print(f"\nПрямые зависимости для {config.package}:")
    if not deps:
        print(" - зависимости не найдены")
    for dep in deps:
        print(f" - {dep['groupId']}:{dep['artifactId']}")
        
    return 0


def main() -> None:
    sys.exit(run(sys.argv[1:]))

if __name__ == "__main__":
    main()