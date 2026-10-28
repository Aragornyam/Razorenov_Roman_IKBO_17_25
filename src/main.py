import sys
import argparse

from PyQt6.QtWidgets import QApplication

from gui import MainWindow


def main() -> None:
    """Точка входа в приложение."""
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument(
        "--vfs",
        type=str,
        default="",
        help="Путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        type=str,
        default="",
        help="Путь к стартовому скрипту",
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = MainWindow(vfs_path=args.vfs, script_path=args.script)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
