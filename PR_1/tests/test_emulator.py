import unittest
from core.emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    """Тесты для эмулятора командной оболочки."""

    def test_ls_stub(self) -> None:
        """Тест заглушки команды ls."""
        emulator = ShellEmulator(vfs_path="")
        result = emulator.execute_command("ls /var")
        self.assertIn("ls (заглушка)", result)
        self.assertIn("/var", result)
        
    def test_cd_stub(self) -> None:
        """Тест заглушки команды cd."""
        emulator = ShellEmulator(vfs_path="")
        result = emulator.execute_command("cd /home")
        self.assertIn("cd (заглушка)", result)
        self.assertIn("/home", result)
        
    def test_exit_command(self) -> None:
        """Тест команды exit."""
        emulator = ShellEmulator(vfs_path="")
        self.assertTrue(emulator.is_running)
        result = emulator.execute_command("exit")
        self.assertFalse(emulator.is_running)
        self.assertIn("Завершение работы", result)
        
    def test_vfs_info_no_vfs(self) -> None:
        """Тест вывода информации о VFS при ее отсутствии."""
        emulator = ShellEmulator(vfs_path="")
        result = emulator.execute_command("vfs-info")
        self.assertIn("Ошибка: VFS не была успешно загружена", result)

    def test_unknown_command(self) -> None:
        """Тест обработки неизвестной команды."""
        emulator = ShellEmulator(vfs_path="")
        result = emulator.execute_command("qweasdzxc")
        self.assertIn("Ошибка: неизвестная команда", result)


if __name__ == "__main__":
    unittest.main()