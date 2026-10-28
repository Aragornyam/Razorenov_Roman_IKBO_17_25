@echo off
chcp 65001 >nul

echo ls> test_script.txt
echo cd my_folder>> test_script.txt
echo fake_command>> test_script.txt
echo ls>> test_script.txt

echo === Запуск 1: Без аргументов ===
python src\main.py

echo === Запуск 2: Только параметр VFS ===
python src\main.py --vfs "system.csv"

echo === Запуск 3: Передача VFS и скрипта (должен прерваться на fake_command) ===
python src\main.py --vfs "system.csv" --script "test_script.txt"

del test_script.txt
pause