"""Тесты интерфейса командной строки."""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from confconv import __version__
from tests.helpers import ROOT
from confconv.cli import EXIT_CONFIG_ERROR, EXIT_IO_ERROR, EXIT_OK, main

ARGPARSE_ERROR = 2


def run_cli(*args):
    """Запуск main и возврат кортежа (код возврата, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main(list(args))
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


@contextlib.contextmanager
def config_file(text, name="config.conf", encoding="utf-8"):
    """Создание временного файла
     с текстом text и возврат пути к нему."""
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / name
        path.write_bytes(text.encode(encoding))
        yield str(path)


class SuccessTests(unittest.TestCase):
    """Корректный ввод преобразуется
    в JSON в стандартном потоке вывода."""

    def test_json_goes_to_standard_output(self):
        with config_file("{ a = .5 b = #( 'x' ) }") as path:
            code, out, err = run_cli("--input", path)
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(json.loads(out), {"a": 0.5, "b": ["x"]})
        self.assertEqual(err, "")

    def test_short_option(self):
        with config_file("'text'") as path:
            code, out, _ = run_cli("-i", path)
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(json.loads(out), "text")

    def test_constants_and_comments(self):
        text = "% c\nset a = .5\n{ x = ![a] }"
        with config_file(text) as path:
            _, out, _ = run_cli("-i", path)
        self.assertEqual(json.loads(out), {"x": 0.5})

    def test_default_indent_is_two_spaces(self):
        with config_file("{ a = .5 }") as path:
            _, out, _ = run_cli("-i", path)
        self.assertEqual(out, '{\n  "a": 0.5\n}\n')

    def test_custom_indent(self):
        with config_file("{ a = .5 }") as path:
            _, out, _ = run_cli("-i", path, "--indent", "4")
        self.assertEqual(out, '{\n    "a": 0.5\n}\n')

    def test_non_ascii_text_is_not_escaped(self):
        with config_file("'Привет'") as path:
            _, out, _ = run_cli("-i", path)
        self.assertIn("Привет", out)

    def test_utf8_bom_is_accepted(self):
        with config_file("'ok'", encoding="utf-8-sig") as path:
            code, out, _ = run_cli("-i", path)
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(json.loads(out), "ok")

    def test_version(self):
        code, out, _ = run_cli("--version")
        self.assertEqual(code, EXIT_OK)
        self.assertIn(__version__, out)


class FailureTests(unittest.TestCase):
    """Ошибки ввода выводятся в стандартный поток ошибок."""

    def test_syntax_error_message(self):
        with config_file("{\n  a = 5\n}") as path:
            code, out, err = run_cli("-i", path)
        self.assertEqual(code, EXIT_CONFIG_ERROR)
        self.assertEqual(out, "")
        self.assertIn(path, err)
        self.assertIn("строка 2, колонка 7", err)

    def test_semantic_error_message(self):
        with config_file("![x]") as path:
            code, out, err = run_cli("-i", path)
        self.assertEqual(code, EXIT_CONFIG_ERROR)
        self.assertEqual(out, "")
        self.assertIn("неопределенная константа 'x'", err)

    def test_missing_file(self):
        code, out, err = run_cli("-i", "no/such/file.conf")
        self.assertEqual(code, EXIT_IO_ERROR)
        self.assertEqual(out, "")
        self.assertIn("невозможно прочитать файл", err)

    def test_file_with_wrong_encoding(self):
        with config_file("'ж'", encoding="cp1251") as path:
            code, _, err = run_cli("-i", path)
        self.assertEqual(code, EXIT_IO_ERROR)
        self.assertIn("невозможно прочитать файл", err)

    def test_input_option_is_required(self):
        code, _, err = run_cli()
        self.assertEqual(code, ARGPARSE_ERROR)
        self.assertIn("--input", err)

    def test_negative_indent_is_rejected(self):
        with config_file(".5") as path:
            code, _, err = run_cli("-i", path, "--indent", "-1")
        self.assertEqual(code, ARGPARSE_ERROR)
        self.assertIn("не должно быть отрицательным", err)

    def test_indent_must_be_integer(self):
        with config_file(".5") as path:
            code, _, err = run_cli("-i", path, "--indent", "many")
        self.assertEqual(code, ARGPARSE_ERROR)
        self.assertIn("не целое число", err)


class EntryPointTests(unittest.TestCase):
    """Пакет можно запустить с помощью python -m confconv."""

    def run_module(self, *args):
        """Запуск пакета в отдельном процессе."""
        env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [sys.executable, "-m", "confconv", *args], env=env,
            capture_output=True, encoding="utf-8", check=False)

    def test_module_prints_json(self):
        with config_file("{ a = .5 }") as path:
            result = self.run_module("-i", path)
        self.assertEqual(result.returncode, EXIT_OK)
        self.assertEqual(json.loads(result.stdout), {"a": 0.5})

    def test_module_reports_errors_with_exit_code(self):
        with config_file("{ a = }") as path:
            result = self.run_module("-i", path)
        self.assertEqual(result.returncode, EXIT_CONFIG_ERROR)
        self.assertEqual(result.stdout, "")
        self.assertIn("ошибка", result.stderr)