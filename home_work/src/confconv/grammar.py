"""Грамматика учебного конфигурационного языка (pyparsing).

Грамматика строит только синтаксическое дерево (см. nodes);
константы разрешаются позже в evaluator. Действия при разборе
(parse actions) не имеют побочных эффектов, что важно при
возвратах (backtracking) в pyparsing.
"""
from functools import lru_cache

import pyparsing as pp

from .nodes import (Array, ConstRef, Entry, Mapping, Name, Number, SetStmt,
                    String)

NAME_PATTERN = r"[a-zA-Z][_a-zA-Z0-9]*"
NAME_TAIL = r"(?![_a-zA-Z0-9])"
SET_PATTERN = r"set" + NAME_TAIL
NUMBER_PATTERN = r"[0-9]*\.[0-9]+"
STRING_PATTERN = r"'[^']*'"
LINE_COMMENT_PATTERN = r"%[^\n]*"
BLOCK_COMMENT_PATTERN = r"\(\*[\s\S]*?\*\)"


def _make_name(source, loc, tokens):
    """Создание Name с сохранением строки и колонки."""
    return Name(tokens[0], pp.lineno(loc, source), pp.col(loc, source))


def _make_number(tokens):
    """Создание Number из совпавшего текста."""
    return Number(float(tokens[0]))


def _make_string(tokens):
    """Создание String без окружающих кавычек."""
    return String(tokens[0][1:-1])


def _make_array(tokens):
    """Создание Array из уже разобранных элементов."""
    return Array(tuple(tokens))


def _make_entry(tokens):
    """Создание Entry словаря из имени и значения."""
    name, value = tokens
    return Entry(name, value)


def _make_mapping(tokens):
    """Создание Mapping из уже разобранных записей."""
    return Mapping(tuple(tokens))


def _make_const_ref(tokens):
    """Создание ConstRef из ссылаемого имени."""
    return ConstRef(tokens[0])


def _make_set(tokens):
    """Создание SetStmt из имени и значения."""
    name, value = tokens
    return SetStmt(name, value)


def _symbol(text, label=None):
    """Возврат подавленного литерала;
    label для сообщений об ошибках."""
    literal = pp.Literal(text).set_name(label or f"'{text}'")
    return pp.Suppress(literal)


def _name_term():
    """Возврат терминала для имен; слово set зарезервировано."""
    pattern = f"(?!{SET_PATTERN})" + NAME_PATTERN
    term = pp.Regex(pattern).set_name("имя")
    return term.set_parse_action(_make_name)


def _value_term(value):
    """Определение правила value грамматики в forward-объекте ``value``."""
    number = pp.Regex(NUMBER_PATTERN).set_parse_action(_make_number)
    string = pp.Regex(STRING_PATTERN).set_parse_action(_make_string)
    name = _name_term()
    array = (_symbol("#(") - pp.ZeroOrMore(value)
             - _symbol(")", "значение или ')'")).set_parse_action(_make_array)
    entry = (name - _symbol("=") - value).set_parse_action(_make_entry)
    mapping = (_symbol("{") - pp.ZeroOrMore(entry)
               - _symbol("}", "имя или '}'")).set_parse_action(_make_mapping)
    const = (_symbol("![") - name
             - _symbol("]")).set_parse_action(_make_const_ref)
    alternatives = number | string | array | mapping | const
    value <<= alternatives.set_name("значение")
    return value


def _statements(value):
    """Возврат правила для оператора верхнего уровня:
     set или значение."""
    keyword = pp.Regex(SET_PATTERN).set_name("'set'")
    declaration = (pp.Suppress(keyword) - _name_term() - _symbol("=")
                   - value).set_parse_action(_make_set)
    return declaration | value


@lru_cache(maxsize=None)
def build_grammar():
    """Возврат элемента pyparsing, который разбирает весь текст.

    Элемент создается один раз и затем переиспользуется.
    """
    value = _value_term(pp.Forward())
    end = pp.StringEnd().set_name("set, значение или конец ввода")
    program = pp.ZeroOrMore(_statements(value)) + end
    program.ignore(pp.Regex(LINE_COMMENT_PATTERN))
    program.ignore(pp.Regex(BLOCK_COMMENT_PATTERN))
    program.parse_with_tabs()
    return program
