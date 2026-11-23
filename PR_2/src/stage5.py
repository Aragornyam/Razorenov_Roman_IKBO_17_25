from core.cli import parse_args
from core.graph import build_dependency_graph
from core.renderer import generate_d2_and_svg


def main():
    args = parse_args()

    print("=== Этап 5: Визуализация графа ===")
    graph = build_dependency_graph(args)
    generate_d2_and_svg(graph, args.output)


if __name__ == "__main__":
    main()
