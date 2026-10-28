class ShellEmulator:
    """Класс ядра эмулятора, обрабатывающий логику REPL."""

    def __init__(self) -> None:
        self.is_running = True

    def execute_command(self, command_line: str) -> str:
        """
        Парсит и выполняет команду.
        Возвращает текстовый результат для вывода в консоль.
        """
        if not command_line:
            return ""

        parts = command_line.split()
        command = parts[0]
        args = parts[1:]

        if command == "ls":
            return self._stub_ls(args)
        elif command == "cd":
            return self._stub_cd(args)
        elif command == "exit":
            self.is_running = False
            return "Завершение работы эмулятора..."

        return f"Ошибка: неизвестная команда '{command}'"

    def _stub_ls(self, args: list[str]) -> str:
        if len(args) > 1:
            return "Ошибка: ls принимает не более 1 аргумента"

        args_str = " ".join(args) if args else "нет аргументов"
        return f"ls (заглушка). Аргументы: {args_str}"

    def _stub_cd(self, args: list[str]) -> str:
        if len(args) > 1:
            return "Ошибка: cd принимает не более 1 аргумента"

        args_str = " ".join(args) if args else "нет аргументов"
        return f"cd (заглушка). Аргументы: {args_str}"
