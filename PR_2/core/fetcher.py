import json
import urllib.request
import re


def clean_version(version_str: str) -> str:
    """Очистка версии от спецсимволов npm (^, ~, >, <)."""
    match = re.search(r'\d+\.\d+\.\d+', version_str)
    return match.group(0) if match else "latest"


def get_npm_dependencies(package: str, version: str, url: str) -> dict:
    """Получение прямых зависимостей из npm registry."""
    target_version = version if version and version != "latest" else "latest"
    req_url = f"{url}/{package}/{target_version}"

    try:
        req = urllib.request.Request(
            req_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("dependencies", {})
    except Exception as e:
        print(f"Ошибка получения зависимостей {package}@{version}: {e}")
        return {}


def get_test_dependencies(package: str, file_path: str) -> dict:
    """Получение зависимостей из локального тестового графа."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get(package, {})
    except Exception as e:
        print(f"Ошибка чтения тестового файла: {e}")
        return {}
