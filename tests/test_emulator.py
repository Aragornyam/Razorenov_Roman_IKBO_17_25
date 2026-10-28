import unittest
import os
from core.emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.emulator = ShellEmulator(vfs_path="")

    def test_ls_stub(self):
        result = self.emulator.execute_command("ls /var")
        self.assertIn("ls (заглушка)", result)
        self.assertIn("/var", result)
        
    def test_cd_stub(self):
        result = self.emulator.execute_command("cd /home")
        self.assertIn("cd (заглушка)", result)
        self.assertIn("/home", result)
        
    def test_exit_command(self):
        self.assertTrue(self.emulator.is_running)
        result = self.emulator.execute_command("exit")
        self.assertFalse(self.emulator.is_running)
        self.assertIn("Завершение работы", result)
        
    def test_vfs_info_no_vfs(self):
        result = self.emulator.execute_command("vfs-info")
        self.assertIn("Ошибка: VFS не была успешно загружена", result)

    def test_unknown_command(self):
        result = self.emulator.execute_command("qweasdzxc")
        self.assertIn("Ошибка: неизвестная команда", result)

if __name__ == "__main__":
    unittest.main()
