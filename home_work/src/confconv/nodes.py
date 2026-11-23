"""Узлы синтаксического дерева, построенного парсером."""
from dataclasses import dataclass
from typing import Tuple, Union


@dataclass(frozen=True)
class Name:
    """Идентификатор вместе с местом, где он был написан."""

    text: str
    line: int
    column: int


@dataclass(frozen=True)
class Number:
    """Числовой литерал, например .5 или 3.14."""

    value: float


@dataclass(frozen=True)
class String:
    """Строковый литерал. кавычки уже удалены."""

    value: str


@dataclass(frozen=True)
class Array:
    """Массив #( значение ... )."""

    items: Tuple["node_value", ...]


@dataclass(frozen=True)
class Entry:
    """Одна пара имя = значение в словаре."""

    name: Name
    value: "node_value"


@dataclass(frozen=True)
class Mapping:
    """Словарь { имя = значение ... }."""

    entries: Tuple[Entry, ...]


@dataclass(frozen=True)
class ConstRef:
    """Подстановка константы на этапе трансляции ![имя]."""

    name: Name


@dataclass(frozen=True)
class SetStmt:
    """Объявление константы на
    этапе трансляции set имя = значение."""

    name: Name
    value: "node_value"


@dataclass(frozen=True)
class Program:
    """Весь текст: объявления и значения
    в порядке их написания."""

    statements: Tuple[Union[SetStmt, "node_value"], ...]


node_value = Union[Number, String, Array, Mapping, ConstRef]
