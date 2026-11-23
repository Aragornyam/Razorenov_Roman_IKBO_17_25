"""Синтаксический разбор текста
конфигурации в синтаксическое дерево."""
import re

import pyparsing as pp

from .errors import ConfigSyntaxError
from .grammar import SET_PATTERN, build_grammar
from .nodes import Program

BLOCK_COMMENT_START = "(*"
QUOTE = "'"
DIGITS = "0123456789"
MAX_FOUND_LENGTH = 20
WORD_PATTERN = re.compile(r"\S+")
RESERVED_PATTERN = re.compile(SET_PATTERN)


def _describe_found(text, loc):
    """Возврат короткой цитаты текста, найденного на позиции loc."""
    if loc >= len(text):
        return "конец ввода"
    match = WORD_PATTERN.match(text, loc)
    word = match.group(0) if match else text[loc]
    if len(word) > MAX_FOUND_LENGTH:
        word = word[:MAX_FOUND_LENGTH] + "..."
    return repr(word)


def _hint(text, loc):
    """Возврат конкретного объяснения для типичных ошибок или None."""
    if loc >= len(text):
        return None
    if text.startswith(BLOCK_COMMENT_START, loc):
        return "незакрытый комментарий: отсутствует закрывающий '*)'"
    if text[loc] == QUOTE:
        return "незакрытая строка: отсутствует закрывающая кавычка"
    if text[loc] in DIGITS:
        return ("некорректное число: число должно содержать "
                "десятичную точку, например 1.0 или .5")
    if RESERVED_PATTERN.match(text, loc):
        return ("неожиданный 'set': это зарезервированное слово, оно не "
                "может быть именем, и объявления разрешены только "
                "на верхнем уровне")
    return None


def _to_syntax_error(exc, text):
    """Конвертация исключения pyparsing в ConfigSyntaxError."""
    message = _hint(text, exc.loc)
    if message is None:
        expected = exc.msg
        if expected.startswith("Expected "):
            expected = expected[9:]
        else:
            expected = expected[:1].lower() + expected[1:]
        message = (f"ожидалось {expected}, "
                   f"найдено {_describe_found(text, exc.loc)}")
    return ConfigSyntaxError(message, exc.lineno, exc.column)


def parse(text):
    """Разбор text и возврат синтаксического дерева Program.

    Вызывает ConfigSyntaxError, если текст не соответствует грамматике.
    """
    try:
        results = build_grammar().parse_string(text)
    except pp.ParseBaseException as exc:
        raise _to_syntax_error(exc, text) from None
    return Program(tuple(results))
