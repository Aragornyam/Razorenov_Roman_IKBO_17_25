import os
import csv
import hashlib


class VirtualFileSystem:
    """Управляет загрузкой и хранением состояния виртуальной файловой системы."""

    def __init__(self, path: str) \
            -> None:
        self.path = path
        self.error = ""
        self.hash_sha256 = ""
        self.data: dict[str, dict[str, str]] = {}
        self._load()

    def _load(self) -> None:
        """Считывает VFS из CSV-файла и вычисляет SHA-256."""
        if not self.path:
            self.error = "VFS не задана."
            return

        if not os.path.exists(self.path):
            self.error = f"Ошибка: Файл VFS '{self.path}' не найден."
            return

        try:
            with open(self.path, 'rb') as f:
                self.hash_sha256 = hashlib.sha256(f.read()).hexdigest()

            with open(self.path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                req_cols = {"path", "type", "content"}

                if not reader.fieldnames or not req_cols.issubset(set(reader.fieldnames)):
                    self.error = (
                        "Ошибка: Неверный формат VFS. "
                        "Требуются колонки path, type, content."
                    )
                    return

                for row in reader:
                    self.data[row["path"]] = {
                        "type": row["type"],
                        "content": row["content"]
                    }

            if "/" not in self.data:
                self.data["/"] = {"type": "dir", "content": ""}

        except Exception as e:
            self.error = f"Ошибка при загрузке VFS: {str(e)}"