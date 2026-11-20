"""Вычисление синтаксического
дерева на этапе трансляции в базовые типы."""
from .errors import ConfigSemanticError
from .nodes import Array, ConstRef, Mapping, Number, SetStmt, String

EXPECTED_TOP_LEVEL_VALUES = 1


class Evaluator:
    """Вычисляет значение программы.

    Константы объявляются через set и подставляются через ![имя].
    Константа должна быть объявлена
    до использования и не может быть
    переопределена.
    """

    def __init__(self):
        """Создание вычислителя без объявленных констант."""
        self._constants = {}
        self._handlers = {
            Number: self._number,
            String: self._string,
            Array: self._array,
            Mapping: self._mapping,
            ConstRef: self._const_ref,
        }

    def run(self, program):
        """Вычисление ``program`` и возврат значения верхнего уровня."""
        values = []
        for statement in program.statements:
            if isinstance(statement, SetStmt):
                self._declare(statement)
            else:
                values.append(self.evaluate(statement))
        return self._single(values)

    def evaluate(self, node):
        """Возврат значения Python для узла."""
        return self._handlers[type(node)](node)

    def _single(self, values):
        """Проверка наличия ровно одного значения верхнего уровня."""
        if len(values) != EXPECTED_TOP_LEVEL_VALUES:
            raise ConfigSemanticError(
                "ожидалось ровно одно значение верхнего уровня, "
                f"найдено {len(values)}")
        return values[0]

    def _declare(self, statement):
        """Вычисление значения set и сохранение его как константы."""
        name = statement.name
        if name.text in self._constants:
            raise ConfigSemanticError(
                f"константа '{name.text}' уже объявлена",
                name.line, name.column)
        self._constants[name.text] = self.evaluate(statement.value)

    def _number(self, node):
        """Возврат числа с плавающей точкой из числового литерала."""
        return node.value

    def _string(self, node):
        """Возврат текста из строкового литерала."""
        return node.value

    def _array(self, node):
        """Вычисление каждого элемента массива."""
        return [self.evaluate(item) for item in node.items]

    def _mapping(self, node):
        """Вычисление словаря с проверкой на дублирование ключей."""
        result = {}
        for entry in node.entries:
            key = entry.name
            if key.text in result:
                raise ConfigSemanticError(
                    f"дубликат ключа '{key.text}'", key.line, key.column)
            result[key.text] = self.evaluate(entry.value)
        return result

    def _const_ref(self, node):
        """Возврат значения ранее объявленной константы."""
        name = node.name
        if name.text not in self._constants:
            raise ConfigSemanticError(
                f"неопределенная константа '{name.text}'",
                name.line, name.column)
        return self._constants[name.text]


def evaluate(program):
    """Вычисление Program и возврат базовых данных Python."""
    return Evaluator().run(program)
