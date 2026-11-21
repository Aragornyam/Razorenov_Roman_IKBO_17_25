"""Тесты имен [a-zA-Z][_a-zA-Z0-9]*, используемых как ключи словаря."""
from confconv import ConfigSyntaxError
from tests.helpers import TranslatorTestCase


class NameTests(TranslatorTestCase):
    """Корректные и некорректные имена."""

    def test_single_letter(self):
        self.assert_translates("{ a = .1 }", {"a": 0.1})

    def test_upper_case_letters(self):
        self.assert_translates("{ ABC = .1 }", {"ABC": 0.1})

    def test_underscores_and_digits(self):
        self.assert_translates("{ a_1_B2 = .1 }", {"a_1_B2": 0.1})

    def test_names_are_case_sensitive(self):
        self.assert_translates(
            "{ key = .1 Key = .2 }", {"key": 0.1, "Key": 0.2})

    def test_name_may_start_with_reserved_word(self):
        self.assert_translates("{ setting = .1 set_2 = .2 }",
                               {"setting": 0.1, "set_2": 0.2})

    def test_name_cannot_start_with_underscore(self):
        self.assert_fails("{ _a = .1 }", ConfigSyntaxError)

    def test_name_cannot_start_with_digit(self):
        self.assert_fails("{ 1a = .1 }", ConfigSyntaxError)

    def test_name_cannot_contain_dash(self):
        self.assert_fails("{ a-b = .1 }", ConfigSyntaxError)

    def test_reserved_word_set_is_not_a_name(self):
        error = self.assert_fails(
            "{ set = .1 }", ConfigSyntaxError, "зарезервированное")
        self.assertEqual((error.line, error.column), (1, 3))

    def test_names_of_constants_follow_same_rules(self):
        self.assert_fails("set _x = .1 .2", ConfigSyntaxError)
