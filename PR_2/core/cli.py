import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Анализатор графа зависимостей")
    parser.add_argument("--package", required=True,
                        help="Имя анализируемого пакета")
    parser.add_argument("--url", required=True,
                        help="URL-адрес репозитория или путь к файлу")
    parser.add_argument("--test-mode", action="store_true",
                        help="Режим работы с тестовым репозиторием")
    parser.add_argument("--pkg-version", required=True,
                        help="Версия пакета")
    parser.add_argument("--output", required=True,
                        help="Имя сгенерированного файла с изображением")
    parser.add_argument("--max-depth", type=int, required=True,
                        help="Максимальная глубина анализа")

    try:
        args = parser.parse_args()
    except SystemExit:
        print("Ошибка: Неверно заданы аргументы или пропущены параметры.")
        sys.exit(1)

    if (args.max_depth
            < 0):
        print("Ошибка: Максимальная глубина не может быть отрицательной.")
        sys.exit(1)

    return args
