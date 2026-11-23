from core.cli import parse_args


def main():
    args = parse_args()

    print("=== Этап 1: Настраиваемые параметры ===")
    for key, value in vars(args).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
