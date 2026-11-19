"""Исключения, вызываемые транслятором конфигурационного языка."""


class ConfigError(Exception):
    """Базовый класс для всех ошибок в тексте конфигурации.

    Необязательные line и column (начиная с 1) указывают на
    место в тексте, вызвавшее ошибку.
    """

    def __init__(self, message, line=None, column=None):
        """Сохранение сообщения и необязательной позиции ошибки."""
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        """Возврат сообщения с префиксом позиции, если она известна."""
        if self.line is None:
            return self.message
        return f"строка {self.line}, колонка {self.column}: {self.message}"


class ConfigSyntaxError(ConfigError):
    """Текст не соответствует грамматике языка."""


class ConfigSemanticError(ConfigError):
    """Текст синтаксически корректен, но содержит семантическую ошибку.

    Примеры. Использование неопределенной константы, дублирование
    ключа в словаре.
    """