import os
from core.vfs import VirtualFileSystem


class ShellEmulator:
    """Класс ядра эмулятора, обрабатывающий логику REPL и команды."""

    def __init__(self, vfs_path: str = "") -> None:
        self.is_running = True
        self.vfs = VirtualFileSystem(vfs_path)

    def execute_command(self, command_line: str) -> str:
        """Парсит и выполняет команду."""
        if not command_line:
            return ""

        parts = command_line.split()
        command = parts[0]
        args = parts[1:]

        if command == "ls":
            return self._stub_ls(args)
        elif command == "cd":
            return self._stub_cd(args)
        elif command == "vfs-info":
            return self._cmd_vfs_info(args)
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

    def _cmd_vfs_info(self, args: list[str]) -> str:
        if args:
            return "Ошибка: команда vfs-info не принимает аргументов"
        if self.vfs.error or not self.vfs.path:
            return "Ошибка: VFS не была успешно загружена."
        vfs_name = os.path.basename(self.vfs.path)
        return f"Имя VFS: {vfs_name}\nSHA-256: {self.vfs.hash_sha256}"