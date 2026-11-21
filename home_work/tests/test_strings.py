"""Тесты строковых литералов в одинарных кавычках."""
from confconv import ConfigSyntaxError
from tests.helpers import TranslatorTestCase


class StringTests(TranslatorTestCase):
    """Корректные и некорректные строки."""

    def test_simple_string(self):
        self.assert_translates("'hello'", "hello")

    def test_empty_string(self):
        self.assert_translates("''", "")

    def test_string_with_spaces(self):
        self.assert_translates("'  two  spaces  '", "  two  spaces  ")

    def test_string_with_language_symbols(self):
        text = "'#( { } = ![x] set % (* *)'"
        self.assert_translates(text, "#( { } = ![x] set % (* *)")

    def test_unicode_string(self):
        self.assert_translates("'Привет, мир!'", "Привет, мир!")

    def test_multi_line_string(self):
        self.assert_translates("'first\nsecond'", "first\nsecond")

    def test_double_quotes_are_not_supported(self):
        self.assert_fails('"text"', ConfigSyntaxError)

    def test_two_adjacent_strings_in_array(self):
        self.assert_translates("#( 'a''b' )", ["a", "b"])

    def test_unterminated_string(self):
        error = self.assert_fails(
            "{ a = 'oops }", ConfigSyntaxError, "незакрытая строка")
        self.assertEqual((error.line, error.column), (1, 7))
