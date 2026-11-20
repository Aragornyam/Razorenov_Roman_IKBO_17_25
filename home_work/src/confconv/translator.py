"""Высокоуровневый API:
текст конфигурационного языка -> данные или JSON."""
import json

from .errors import ConfigSemanticError
from .evaluator import evaluate
from .parser import parse

DEFAULT_INDENT = 2


def translate(text):
    """Трансляция конфигурационного текста text в данные Python.

    Числа становятся float, строки str, массивы list,
    а словари dict. Выбрасывает подклассы ConfigError при ошибках.
    """
    try:
        return evaluate(parse(text))
    except RecursionError:
        raise ConfigSemanticError(
            "структура вложена слишком глубоко") from None


def to_json(text, indent=DEFAULT_INDENT):
    """Трансляция текста конфигурации
    и сериализация результата в JSON."""
    return json.dumps(translate(text), ensure_ascii=False, indent=indent)
