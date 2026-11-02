#!/bin/bash

# 1. Создаем минимальный VFS
echo "path,type,content" > vfs_min.csv
echo "/,dir," >> vfs_min.csv

# 2. Создаем VFS с несколькими файлами
echo "path,type,content" > vfs_multi.csv
echo "/,dir," >> vfs_multi.csv
echo "/file1.txt,file,dGVzdA==" >> vfs_multi.csv
echo "/file2.txt,file,MTIz" >> vfs_multi.csv

# 3. Создаем глубокий VFS (3+ уровня вложенности)
echo "path,type,content" > vfs_deep.csv
echo "/,dir," >> vfs_deep.csv
echo "/usr,dir," >> vfs_deep.csv
echo "/usr/bin,dir," >> vfs_deep.csv
echo "/usr/bin/python,file,cHl0aG9u" >> vfs_deep.csv
echo "/var,dir," >> vfs_deep.csv
echo "/var/log,dir," >> vfs_deep.csv
echo "/var/log/syslog,file,bG9n" >> vfs_deep.csv

# 4. Создаем скрипт тестирования команд
echo "vfs-info" > test_stage3.txt
echo "ls" >> test_stage3.txt
echo "exit" >> test_stage3.txt

echo "=== Тест 1: Ошибка VFS (файл не найден) ==="
python3 src/main.py --vfs "not_found.csv"

echo "=== Тест 2: Ошибка VFS (неверный формат) ==="
python3 src/main.py --vfs "test_stage3.txt"

echo "=== Тест 3: Успешный запуск с вложенной VFS и скриптом ==="
python3 src/main.py --vfs "vfs_deep.csv" --script "test_stage3.txt"

rm vfs_min.csv vfs_multi.csv vfs_deep.csv test_stage3.txt