"""Тесты структуры всего текста."""
from confconv import ConfigSemanticError, ConfigSyntaxError
from tests.helpers import TranslatorTestCase


class ProgramTests(TranslatorTestCase):
    """Текст состоит из объявлений
    и одного значения верхнего уровня."""

    def test_top_level_number(self):
        self.assert_translates(".5", 0.5)

    def test_top_level_string(self):
        self.assert_translates("'text'", "text")

    def test_top_level_array(self):
        self.assert_translates("#( .1 )", [0.1])

    def test_top_level_dictionary(self):
        self.assert_translates("{ a = .1 }", {"a": 0.1})

    def test_declarations_before_value(self):
        self.assert_translates("set a = .1 set b = .2 ![b]", 0.2)

    def test_declaration_after_value(self):
        self.assert_translates("{ a = .1 } set unused = .2", {"a": 0.1})

    def test_empty_text(self):
        self.assert_fails("", ConfigSemanticError, "найдено 0")

    def test_only_declarations(self):
        self.assert_fails("set a = .1", ConfigSemanticError, "найдено 0")

    def test_two_top_level_values(self):
        self.assert_fails(".1 .2", ConfigSemanticError, "найдено 2")

    def test_garbage_after_value(self):
        error = self.assert_fails(
            "{ a = .1 }\n\n  }", ConfigSyntaxError, "найдено '}'")
        self.assertEqual((error.line, error.column), (3, 3))

    def test_windows_line_endings(self):
        self.assert_translates("{\r\n a = .1 % c\r\n b = .2\r\n}\r\n",
                               {"a": 0.1, "b": 0.2})

    def test_tabs_keep_columns_of_errors(self):
        error = self.assert_fails("\t\t{ a = x }", ConfigSyntaxError, "'x'")
        self.assertEqual((error.line, error.column), (1, 9))

    def test_error_in_late_line_reports_the_line(self):
        text = "set a = .1\n\n% c\n(* c\nc *)\n{ b = ![zzz] }"
        error = self.assert_fails(text, ConfigSemanticError, "zzz")
        self.assertEqual(error.line, 6)
