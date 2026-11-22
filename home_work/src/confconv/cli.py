"""Интерфейс командной строки транслятора."""
import argparse
import sys
from pathlib import Path

from . import __version__
from .errors import ConfigError
from .translator import DEFAULT_INDENT, to_json

EXIT_OK = 0
EXIT_CONFIG_ERROR = 1
EXIT_IO_ERROR = 2
MIN_INDENT = 0


def indent_type(raw):
    """Разбор опции --indent: неотрицательное целое число."""
    try:
        value = int(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"не целое число: {raw!r}") from None
    if value < MIN_INDENT:
        raise argparse.ArgumentTypeError("не должно быть отрицательным")
    return value


def build_arg_parser():
    """Создание парсера аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="confconv",
        description="Трансляция конфигурации на учебном языке "
                    "в JSON (вывод в стандартный поток).")
    parser.add_argument(
        "-i", "--input", required=True, metavar="ФАЙЛ",
        help="путь к файлу с текстом конфигурации")
    parser.add_argument(
        "--indent", type=indent_type, default=DEFAULT_INDENT, metavar="N",
        help="количество пробелов на уровень JSON (по умолчанию: %(default)s)")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def read_source(path):
    """Чтение текста конфигурации из path."""
    return Path(path).read_text(encoding="utf-8-sig")


def main(argv=None):
    """Запуск транслятора и возврат кода завершения процесса."""
    args = build_arg_parser().parse_args(argv)
    try:
        text = read_source(args.input)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"{args.input}: невозможно прочитать файл: {exc}",
              file=sys.stderr)
        return EXIT_IO_ERROR
    try:
        output = to_json(text, args.indent)
    except ConfigError as exc:
        print(f"{args.input}: ошибка: {exc}", file=sys.stderr)
        return EXIT_CONFIG_ERROR
    print(output)
    return EXIT_OK
