"""Тесты объявлений set имя = значение и вычислений ![имя]."""
from confconv import ConfigSemanticError, ConfigSyntaxError
from tests.helpers import TranslatorTestCase


class ConstantTests(TranslatorTestCase):
    """Объявление и вычисление констант на этапе трансляции."""

    def test_number_constant(self):
        self.assert_translates("set a = .5\n![a]", 0.5)

    def test_string_constant(self):
        self.assert_translates("set a = 'text'\n![a]", "text")

    def test_array_constant(self):
        self.assert_translates("set a = #( .1 'x' )\n![a]", [0.1, "x"])

    def test_dictionary_constant(self):
        self.assert_translates("set a = { k = .1 }\n![a]", {"k": 0.1})

    def test_constant_inside_array(self):
        text = "set a = .5\n#( ![a] ![a] .1 )"
        self.assert_translates(text, [0.5, 0.5, 0.1])

    def test_constant_inside_dictionary(self):
        text = "set a = 'v'\n{ x = ![a] y = ![a] }"
        self.assert_translates(text, {"x": "v", "y": "v"})

    def test_constant_in_deeply_nested_place(self):
        text = "set a = .5\n{ l1 = #( { l2 = #( ![a] ) } ) }"
        self.assert_translates(text, {"l1": [{"l2": [0.5]}]})

    def test_constant_defined_with_other_constant(self):
        text = "set a = .5\nset b = #( ![a] ![a] )\nset c = { k = ![b] }\n![c]"
        self.assert_translates(text, {"k": [0.5, 0.5]})

    def test_whitespace_inside_evaluation(self):
        self.assert_translates("set a = .5\n![  a  ]", 0.5)

    def test_whitespace_between_bang_and_bracket_is_not_allowed(self):
        self.assert_fails("set a = .5\n! [a]", ConfigSyntaxError)

    def test_comments_around_declarations(self):
        text = "% c\nset a = .5 (* c *)\n% c\n![a]"
        self.assert_translates(text, 0.5)

    def test_many_declarations(self):
        text = "set a = .1 set b = .2 set c = .3 #( ![c] ![b] ![a] )"
        self.assert_translates(text, [0.3, 0.2, 0.1])

    def test_constants_do_not_depend_on_case(self):
        text = "set a = .1 set A = .2 #( ![a] ![A] )"
        self.assert_translates(text, [0.1, 0.2])

    def test_undefined_constant_in_declaration_reports_position(self):
        error = self.assert_fails(
            "set a = ![missing]\n.5", ConfigSemanticError, "неопределенная")
        self.assertEqual((error.line, error.column), (1, 11))

    def test_undefined_constant(self):
        error = self.assert_fails(
            "{ a = ![nope] }", ConfigSemanticError,
            "неопределенная константа 'nope'")
        self.assertEqual((error.line, error.column), (1, 9))

    def test_constant_must_be_declared_before_use(self):
        self.assert_fails(
            "![a]\nset a = .5", ConfigSemanticError,
            "неопределенная константа 'a'")

    def test_constant_cannot_refer_to_itself(self):
        self.assert_fails("set a = ![a]\n.5", ConfigSemanticError, "'a'")

    def test_constant_cannot_be_redeclared(self):
        error = self.assert_fails(
            "set a = .1\nset a = .2\n.5", ConfigSemanticError, "уже объявлена")
        self.assertEqual((error.line, error.column), (2, 5))

    def test_declaration_is_not_allowed_inside_dictionary(self):
        self.assert_fails(
            "{ set a = .1 }", ConfigSyntaxError, "объявления разрешены")

    def test_declaration_is_not_allowed_inside_array(self):
        self.assert_fails("#( set a = .1 )", ConfigSyntaxError, "зарезервированное")

    def test_declaration_without_value(self):
        self.assert_fails("set a =", ConfigSyntaxError, "ожидалось значение")

    def test_declaration_without_equal_sign(self):
        self.assert_fails("set a .5", ConfigSyntaxError, "ожидалось '='")

    def test_declaration_without_name(self):
        self.assert_fails("set = .5", ConfigSyntaxError, "ожидалось имя")

    def test_evaluation_without_name(self):
        self.assert_fails("![]", ConfigSyntaxError, "ожидалось имя")

    def test_evaluation_without_closing_bracket(self):
        self.assert_fails("set a = .1 ![a", ConfigSyntaxError, "ожидалось ']'")

    def test_keyword_set_cannot_be_constant_name(self):
        self.assert_fails("set set = .5 .1", ConfigSyntaxError, "зарезервированное")
