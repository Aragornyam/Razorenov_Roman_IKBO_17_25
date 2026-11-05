from core.fetcher import get_test_dependencies, get_npm_dependencies
from core.fetcher import clean_version


def build_dependency_graph(args) -> dict:
    """Построение графа зависимостей алгоритмом DFS без рекурсии."""
    stack = [(args.package, args.pkg_version, 0)]
    visited = set()
    graph = {}

    while stack:
        curr_pkg, curr_ver, depth = stack.pop()
        node_id = f"{curr_pkg}@{curr_ver}"

        if node_id in visited or depth > args.max_depth:
            continue

        visited.add(node_id)
        graph[node_id] = []

        if args.test_mode:
            deps = get_test_dependencies(curr_pkg, args.url)
        else:
            deps = get_npm_dependencies(curr_pkg, curr_ver, args.url)

        for dep_name, dep_ver_raw in deps.items():
            dep_ver = clean_version(dep_ver_raw)
            dep_id = f"{dep_name}@{dep_ver}"
            graph[node_id].append(dep_id)

            stack.append((dep_name, dep_ver, depth + 1))

    return graph
