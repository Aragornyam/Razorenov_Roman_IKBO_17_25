"""Тесты однострочных и многострочных комментариев."""
from confconv import ConfigSyntaxError
from tests.helpers import TranslatorTestCase


class LineCommentTests(TranslatorTestCase):
    """Комментарии, которые начинаются с % и длятся до конца строки."""

    def test_comment_before_value(self):
        self.assert_translates("% comment\n.5", 0.5)

    def test_comment_after_value_on_same_line(self):
        self.assert_translates(".5 % trailing comment", 0.5)

    def test_comment_without_final_newline(self):
        self.assert_translates(".5\n% last line", 0.5)

    def test_comment_may_contain_any_symbols(self):
        text = "% ![x] #( { } ' (* *) set\n.5"
        self.assert_translates(text, 0.5)

    def test_comment_inside_array(self):
        text = "#( .1 % first\n .2 % second\n)"
        self.assert_translates(text, [0.1, 0.2])

    def test_comment_inside_dictionary(self):
        text = "{ % start\n a = .1 % value\n b = % between\n .2 }"
        self.assert_translates(text, {"a": 0.1, "b": 0.2})

    def test_comment_between_declaration_parts(self):
        text = "set % keyword\n a % name\n = % sign\n .3\n![a]"
        self.assert_translates(text, 0.3)

    def test_percent_inside_string_is_not_a_comment(self):
        self.assert_translates("'100% sure'", "100% sure")


class BlockCommentTests(TranslatorTestCase):
    """Комментарии формата (* ... *),
    которые могут занимать много строк."""

    def test_single_line_block_comment(self):
        self.assert_translates("(* note *) .5", 0.5)

    def test_multi_line_block_comment(self):
        self.assert_translates("(*\n  many\n  lines\n*)\n.5", 0.5)

    def test_empty_block_comment(self):
        self.assert_translates("(**) .5", 0.5)

    def test_block_comment_hides_code(self):
        self.assert_translates("(* set a = .1 *) .5", 0.5)

    def test_comment_markers_do_not_nest(self):
        self.assert_translates("(* a (* b *) .5", 0.5)

    def test_block_comment_inside_array(self):
        self.assert_translates("#( .1 (* skip *) .2 )", [0.1, 0.2])

    def test_block_comment_inside_dictionary(self):
        text = "{ a = (* multi\nline *) .1 (* x *) b = .2 }"
        self.assert_translates(text, {"a": 0.1, "b": 0.2})

    def test_block_comment_at_end(self):
        self.assert_translates(".5 (* end *)", 0.5)

    def test_markers_inside_string_are_not_a_comment(self):
        self.assert_translates("'(* text *)'", "(* text *)")

    def test_line_comment_inside_block_comment(self):
        self.assert_translates("(* % not a line comment *) .5", 0.5)

    def test_block_comment_inside_line_comment(self):
        self.assert_translates("% (* open\n.5", 0.5)

    def test_unterminated_block_comment(self):
        error = self.assert_fails(
            ".5\n(* never closed", ConfigSyntaxError, "незакрытый комментарий")
        self.assertEqual((error.line, error.column), (2, 1))

    def test_comment_only_text_has_no_value(self):
        self.assert_fails("% nothing\n(* here *)", fragment="найдено 0")
