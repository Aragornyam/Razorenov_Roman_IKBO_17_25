import json
from core.cli import parse_args
from core.graph import build_dependency_graph


def main():
    args = parse_args()

    print("=== Этап 3: Построенный граф зависимостей ===")
    graph = build_dependency_graph(args)

    print(json.dumps(graph, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
