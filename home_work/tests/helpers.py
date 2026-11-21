"""Общие вспомогательные функции набора тестов."""
import unittest
from pathlib import Path

from confconv import ConfigError, translate

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


class TranslatorTestCase(unittest.TestCase):
    """Базовый класс с проверками результатов трансляции."""

    def assert_translates(self, text, expected):
        """Текст должен транслироваться в ожидаемые данные expected."""
        self.assertEqual(translate(text), expected)

    def assert_fails(self, text, error_type=ConfigError, fragment=""):
        """Текст должен вызывать error_type, содержащее фрагмент fragment.

        Возвращает вызванное исключение для дальнейших проверок.
        """
        with self.assertRaises(error_type) as context:
            translate(text)
        self.assertIn(fragment, str(context.exception))
        return context.exception
