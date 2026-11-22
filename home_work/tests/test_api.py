"""Тесты публичного API на Python и сообщений об ошибках."""
import json

from confconv import (ConfigError, ConfigSemanticError, ConfigSyntaxError,
                      to_json, translate)
from tests.helpers import TranslatorTestCase

LONG_WORD_LENGTH = 50


class ApiTests(TranslatorTestCase):
    """Функции translate и to_json."""

    def test_result_consists_of_plain_python_types(self):
        data = translate("{ a = #( .5 'x' { b = .1 } ) }")
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["a"], list)
        self.assertIsInstance(data["a"][0], float)
        self.assertIsInstance(data["a"][1], str)
        self.assertIsInstance(data["a"][2], dict)

    def test_to_json_is_valid_json(self):
        text = "set a = .5\n{ x = ![a] y = #( 'q' ) }"
        self.assertEqual(json.loads(to_json(text)), {"x": 0.5, "y": ["q"]})

    def test_to_json_compact_form(self):
        self.assertEqual(to_json("{ a = .5 }", indent=None), '{"a": 0.5}')

    def test_to_json_keeps_non_ascii_text(self):
        self.assertEqual(to_json("'ёж'"), '"ёж"')

    def test_error_classes_share_one_base(self):
        self.assertTrue(issubclass(ConfigSyntaxError, ConfigError))
        self.assertTrue(issubclass(ConfigSemanticError, ConfigError))


class MessageTests(TranslatorTestCase):
    """Тексты диагностики ошибок."""

    def test_message_contains_position(self):
        error = self.assert_fails("\n\n  x", ConfigSyntaxError)
        self.assertEqual(str(error).split(":")[0], "строка 3, колонка 3")

    def test_message_without_position(self):
        error = self.assert_fails("", ConfigSemanticError)
        self.assertIsNone(error.line)
        self.assertNotIn("строка", str(error))

    def test_long_found_text_is_shortened(self):
        text = "{ a = " + "x" * LONG_WORD_LENGTH + " }"
        error = self.assert_fails(text, ConfigSyntaxError, "...")
        self.assertNotIn("x" * LONG_WORD_LENGTH, str(error))
