from core.cli import parse_args
from core.fetcher import get_npm_dependencies, get_test_dependencies


def main():
    args = parse_args()

    print("=== Этап 2: Прямые зависимости ===")
    if args.test_mode:
        deps = get_test_dependencies(args.package, args.url)
    else:
        deps = get_npm_dependencies(args.package, args.pkg_version, args.url)

    if not deps:
        print("Зависимости не найдены или список пуст.")
    else:
        for k, v in deps.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
