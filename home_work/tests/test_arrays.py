"""Тесты массивов #( значение значение ... )."""
from confconv import ConfigSyntaxError
from tests.helpers import TranslatorTestCase


class ArrayTests(TranslatorTestCase):
    """Массивы со всеми типами значений, включая вложенные."""

    def test_empty_array(self):
        self.assert_translates("#()", [])

    def test_empty_array_with_spaces(self):
        self.assert_translates("#(   \n  )", [])

    def test_array_of_numbers(self):
        self.assert_translates("#( .1 2.5 3.75 )", [0.1, 2.5, 3.75])

    def test_array_of_strings(self):
        self.assert_translates("#( 'a' 'b' 'c' )", ["a", "b", "c"])

    def test_array_with_mixed_values(self):
        text = "#( .5 'x' #( .1 ) { k = 'v' } )"
        self.assert_translates(text, [0.5, "x", [0.1], {"k": "v"}])

    def test_values_without_separators(self):
        self.assert_translates("#(.1 .2 'a''b')", [0.1, 0.2, "a", "b"])

    def test_array_of_arrays(self):
        text = "#( #( .1 .2 ) #() #( 'a' ) )"
        self.assert_translates(text, [[0.1, 0.2], [], ["a"]])

    def test_array_of_dictionaries(self):
        text = "#( { a = .1 } {} { b = .2 } )"
        self.assert_translates(text, [{"a": 0.1}, {}, {"b": 0.2}])

    def test_array_may_span_lines(self):
        self.assert_translates("#(\n  .1\n  .2\n)", [0.1, 0.2])

    def test_missing_closing_bracket(self):
        error = self.assert_fails(
            "#( .1 .2", ConfigSyntaxError, "конец ввода")
        self.assertEqual((error.line, error.column), (1, 9))

    def test_wrong_closing_bracket(self):
        self.assert_fails(
            "#( .1 ]", ConfigSyntaxError, "значение или ')'")

    def test_array_needs_hash_sign(self):
        self.assert_fails("( .1 .2 )", ConfigSyntaxError)

    def test_commas_are_not_separators(self):
        self.assert_fails("#( .1, .2 )", ConfigSyntaxError)

    def test_unexpected_element_in_array(self):
        error = self.assert_fails("#( .1 x )", ConfigSyntaxError, "найдено 'x'")
        self.assertEqual((error.line, error.column), (1, 7))
