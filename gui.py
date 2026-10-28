import getpass
import socket

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QLabel,
)

from emulator import ShellEmulator


class MainWindow(QMainWindow):
    """Главное окно графического интерфейса эмулятора."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.emulator = ShellEmulator()
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle(f"Эмулятор [{self.username}@{self.hostname}]")
        self.resize(750, 500)
        self.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(10, 10, 10, 10)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Consolas", 11))
        self.output_area.setStyleSheet("border: none;")
        layout.addWidget(self.output_area)

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)

        self.prompt_label = QLabel(f"{self.username}@{self.hostname}:~$ ", self)
        self.prompt_label.setFont(QFont("Consolas", 11))
        self.prompt_label.setStyleSheet("color: #4af626;")
        input_layout.addWidget(self.prompt_label)

        self.input_line = QLineEdit(self)
        self.input_line.setFont(QFont("Consolas", 11))
        self.input_line.setStyleSheet("border: none; background-color: #1e1e1e; color: #d4d4d4;")
        self.input_line.returnPressed.connect(self._process_command)  # type: ignore
        input_layout.addWidget(self.input_line)

        layout.addLayout(input_layout)

        self.output_area.append("REPL инициализирован. Ожидание ввода...\n")
        self.input_line.setFocus()

    def _process_command(self) -> None:
        command_text = self.input_line.text().strip()
        if not command_text:
            return

        self.input_line.clear()

        prompt = f"<font color='#4af626'>{self.username}@{self.hostname}:~$</font>"
        self.output_area.append(f"{prompt} {command_text}")

        result = self.emulator.execute_command(command_text)
        if result:
            self.output_area.append(result)

        if not self.emulator.is_running:
            self.close()
