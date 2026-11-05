def get_download_order(graph: dict) -> list:
    """Получение порядка загрузки на основе графа (Топологическая сортировка)."""
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            if v in in_degree:
                in_degree[v] += 1
            else:
                in_degree[v] = 1

    queue = [u for u in graph if in_degree[u] == 0]
    order = []

    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in graph.get(u, []):
            if v in in_degree:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

    cycles = [u for u in in_degree if in_degree[u] > 0]
    if cycles:
        order.extend(cycles)

    return order[::-1]
