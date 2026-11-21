"""Тесты комбинации всех конструкций."""
from confconv import ConfigSemanticError, translate
from tests.helpers import TranslatorTestCase

COMBINED = """
% every construct of the language in one text
set unit = 'kg'
set weights = #( .5 1.25 (* inline *) 2.0 )
set meta = { unit = ![unit] source = 'scale' }
{
  items = #(
    { name = 'apple' weight = ![weights] meta = ![meta] }
    { name = 'pear' tags = #( 'fruit' #( 'sweet' ) ) }
  )
  nested = { a = { b = #( { c = ![unit] } ) } }
}
"""


class NestingTests(TranslatorTestCase):
    """Вложенные друг в друга конструкции."""

    def test_all_constructs_together(self):
        expected = {
            "items": [
                {
                    "name": "apple",
                    "weight": [0.5, 1.25, 2.0],
                    "meta": {"unit": "kg", "source": "scale"},
                },
                {"name": "pear", "tags": ["fruit", ["sweet"]]},
            ],
            "nested": {"a": {"b": [{"c": "kg"}]}},
        }
        self.assert_translates(COMBINED, expected)

    def test_moderately_deep_arrays(self):
        depth = 30
        text = "#(" * depth + " .5 " + ")" * depth
        value = translate(text)
        for _ in range(depth - 1):
            value = value[0]
        self.assertEqual(value, [0.5])

    def test_moderately_deep_dictionaries(self):
        depth = 25
        text = "{ a = " * depth + "'x'" + " }" * depth
        value = translate(text)
        for _ in range(depth):
            value = value["a"]
        self.assertEqual(value, "x")

    def test_too_deep_structure_is_reported(self):
        depth = 5000
        text = "#(" * depth + ")" * depth
        self.assert_fails(text, ConfigSemanticError, "вложена слишком глубоко")
