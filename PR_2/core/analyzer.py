def _compute_in_degrees(graph: dict) -> dict:
    """Вычисляет входящие степени вершин графа."""
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1
    return in_degree


def _process_queue(graph: dict, in_degree: dict, queue: list) -> list:
    """Обрабатывает очередь для топологической сортировки."""
    order = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in graph.get(u, []):
            if v in in_degree:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
    return order


def get_download_order(graph: dict) -> list:
    """
    Получение порядка загрузки на основе графа 
    (Топологическая сортировка).
    """
    in_degree = _compute_in_degrees(graph)
    queue = [u for u, deg in in_degree.items() if deg == 0]

    order = _process_queue(graph, in_degree, queue)

    cycles = [u for u, deg in in_degree.items() if deg > 0]
    if cycles:
        order.extend(cycles)

    return order[::-1]