from core.cli import parse_args
from core.graph import build_dependency_graph
from core.analyzer import get_download_order


def main():
    args = parse_args()

    print("=== Этап 4: Порядок загрузки зависимостей ===")
    graph = build_dependency_graph(args)
    order = get_download_order(graph)

    for i, pkg in enumerate(order, 1):
        print(f"{i}. {pkg}")


if __name__ == "__main__":
    main()
