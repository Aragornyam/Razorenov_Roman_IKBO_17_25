#!/bin/bash

# ошибка на третьей строке
echo -e "ls\ncd my_folder\nfake_command\nls" > test_script.txt

echo "=== Запуск 1: Без аргументов ==="
python3 src/main.py

echo "=== Запуск 2: Только параметр VFS ==="
python3 src/main.py --vfs "system.csv"

echo "=== Запуск 3: Передача VFS и скрипта (должен прерваться на fake_command) ==="
python3 src/main.py --vfs "system.csv" --script "test_script.txt"

rm test_script.txt