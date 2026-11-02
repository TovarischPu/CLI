import urllib.error
import urllib.request

def download_text(url: str) -> str:
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ошибка скачивания {url}: {exc}")