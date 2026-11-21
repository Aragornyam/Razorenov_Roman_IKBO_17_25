"""Тесты словарей { имя = значение ... }."""
from confconv import ConfigSemanticError, ConfigSyntaxError, translate
from tests.helpers import TranslatorTestCase


class MappingTests(TranslatorTestCase):
    """Словари со всеми типами значений, включая вложенные."""

    def test_empty_dictionary(self):
        self.assert_translates("{}", {})

    def test_empty_dictionary_with_spaces(self):
        self.assert_translates("{ \n }", {})

    def test_single_entry(self):
        self.assert_translates("{ a = .5 }", {"a": 0.5})

    def test_entries_of_all_value_kinds(self):
        text = "{ n = .5 s = 'x' a = #( .1 ) d = { k = 'v' } }"
        expected = {"n": 0.5, "s": "x", "a": [0.1], "d": {"k": "v"}}
        self.assert_translates(text, expected)

    def test_entries_on_separate_lines(self):
        text = "{\n  a = .1\n  b = .2\n  c = .3\n}"
        self.assert_translates(text, {"a": 0.1, "b": 0.2, "c": 0.3})

    def test_entries_on_one_line(self):
        self.assert_translates("{a=.1 b=.2}", {"a": 0.1, "b": 0.2})

    def test_key_order_is_preserved(self):
        result = translate("{ z = .1 a = .2 m = .3 }")
        self.assertEqual(list(result), ["z", "a", "m"])

    def test_nested_dictionaries(self):
        text = "{ a = { b = { c = 'deep' } } }"
        self.assert_translates(text, {"a": {"b": {"c": "deep"}}})

    def test_dictionary_with_nested_arrays(self):
        text = "{ matrix = #( #( .1 .2 ) #( .3 .4 ) ) }"
        self.assert_translates(text, {"matrix": [[0.1, 0.2], [0.3, 0.4]]})

    def test_duplicate_key(self):
        error = self.assert_fails(
            "{ a = .1\n  a = .2 }", ConfigSemanticError, "дубликат ключа 'a'")
        self.assertEqual((error.line, error.column), (2, 3))

    def test_same_key_in_different_dictionaries(self):
        text = "{ a = { x = .1 } b = { x = .2 } }"
        self.assert_translates(text, {"a": {"x": 0.1}, "b": {"x": 0.2}})

    def test_missing_equal_sign(self):
        error = self.assert_fails(
            "{ a .5 }", ConfigSyntaxError, "ожидалось '='")
        self.assertEqual((error.line, error.column), (1, 5))

    def test_missing_value(self):
        self.assert_fails("{ a = }", ConfigSyntaxError, "ожидалось значение")

    def test_missing_closing_brace(self):
        self.assert_fails("{ a = .5", ConfigSyntaxError, "конец ввода")

    def test_value_without_name(self):
        self.assert_fails("{ .5 }", ConfigSyntaxError, "имя или '}'")

    def test_string_cannot_be_a_key(self):
        self.assert_fails("{ 'a' = .5 }", ConfigSyntaxError)
