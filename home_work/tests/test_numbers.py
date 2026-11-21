"""Тесты числовых литералов \\d*\\.\\d+."""
from confconv import ConfigSyntaxError, translate
from tests.helpers import TranslatorTestCase


class NumberTests(TranslatorTestCase):
    """Корректные и некорректные числа."""

    def test_fraction_without_integer_part(self):
        self.assert_translates(".5", 0.5)

    def test_integer_and_fraction_parts(self):
        self.assert_translates("3.14", 3.14)

    def test_zero_with_point(self):
        self.assert_translates(".0", 0.0)

    def test_leading_zeros(self):
        self.assert_translates("007.50", 7.5)

    def test_long_number(self):
        self.assert_translates("12345.678901", 12345.678901)

    def test_number_is_float(self):
        self.assertIsInstance(translate("2.0"), float)

    def test_numbers_separated_by_spaces(self):
        self.assert_translates("#( .1 .2\n.3\t.4 )", [0.1, 0.2, 0.3, 0.4])

    def test_integer_is_not_a_number(self):
        error = self.assert_fails("5", ConfigSyntaxError, "десятичную точку")
        self.assertEqual((error.line, error.column), (1, 1))

    def test_trailing_point_is_not_a_number(self):
        self.assert_fails("5.", ConfigSyntaxError, "десятичную точку")

    def test_integer_inside_array(self):
        self.assert_fails("#( .5 7 )", ConfigSyntaxError, "десятичную точку")

    def test_negative_number_is_not_supported(self):
        self.assert_fails("-.5", ConfigSyntaxError)

    def test_exponent_is_not_supported(self):
        self.assert_fails("1.5e3", ConfigSyntaxError)
