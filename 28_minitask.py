from collections import defaultdict


def parse_input(data: str):
    graph = defaultdict(list)
    for line in data.strip().splitlines():
        if ':' not in line:
            continue
        func, callees_str = line.split(':', 1)
        func = func.strip()
        callees = [c.strip() for c in callees_str.split(',') if c.strip()]
        graph[func].extend(callees)
    return graph


def find_all_functions(graph):
    """Отдельная простая функция для сбора всех имен функций."""
    all_nodes = set(graph.keys())
    for callees in graph.values():
        all_nodes.update(callees)
    return all_nodes


def kosaraju_scc(graph):
    """Классический алгоритм Косарайю, разделенный на понятные шаги."""

    order = []
    visited = set()
    all_nodes = find_all_functions(graph)

    def dfs1(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs1(neighbor)
        order.append(node)

    for node in all_nodes:
        if node not in visited:
            dfs1(node)

    transposed_graph = defaultdict(list)
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            transposed_graph[neighbor].append(node)

    sccs = []
    visited.clear()

    def dfs2(node, current_scc):
        visited.add(node)
        current_scc.append(node)
        for neighbor in transposed_graph.get(node, []):
            if neighbor not in visited:
                dfs2(neighbor, current_scc)

    for node in reversed(order):
        if node not in visited:
            current_scc = []
            dfs2(node, current_scc)
            sccs.append(sorted(current_scc))

    return sccs


def analyze(data: str):
    """
    Главная функция, анализирующая граф. Логика разделена на простые шаги.
    """
    graph = parse_input(data)
    sccs = kosaraju_scc(graph)
    all_nodes = find_all_functions(graph)
    output = []

    scc_to_recursion_type = {}
    for component in sccs:
        component_tuple = tuple(component)
        rec_type = "no recursion"
        if len(component) > 1:
            rec_type = "indirect recursion"
        elif len(component) == 1:
            func = component[0]
            if func in graph.get(func, []):
                rec_type = "direct recursion"

        scc_to_recursion_type[component_tuple] = rec_type

    recursive_components = [
        list(comp) for comp, rec_type in scc_to_recursion_type.items() if rec_type != "no recursion"
    ]

    if recursive_components:
        largest_scc = max(recursive_components, key=lambda comp: (len(comp), sorted(comp)))
        output.append(
            f"Largest recursive component ({len(largest_scc)} functions): {', '.join(sorted(largest_scc))}")
    else:
        output.append("No recursive components found")

    func_to_scc_tuple = {func: tuple(comp) for comp in sccs for func in comp}

    for func in sorted(all_nodes):
        component_tuple = func_to_scc_tuple.get(func)
        rec_type = scc_to_recursion_type.get(component_tuple, "no recursion")
        output.append(f"{func}: {rec_type}")

    return "\n".join(output)

result = analyze("""
foo: bar, baz, qux
bar: baz, foo, bar
qux: qux
""")
assert "Largest recursive component (2 functions): bar, foo" in result
assert "foo: indirect recursion" in result
assert "bar: indirect recursion" in result
assert "baz: no recursion" in result
assert "qux: direct recursion" in result

result = analyze("""
a: b
b: c
c: a
d:
""")
assert "Largest recursive component (3 functions): a, b, c" in result
assert "a: indirect recursion" in result
assert "b: indirect recursion" in result
assert "c: indirect recursion" in result
assert "d: no recursion" in result

result = analyze("""
selfcall: selfcall
lonely:
""")
assert "Largest recursive component (1 functions): selfcall" in result
assert "selfcall: direct recursion" in result
assert "lonely: no recursion" in result

result = analyze("""
x: y
y: z
z:
""")
assert "No recursive components found" in result
assert "x: no recursion" in result
assert "y: no recursion" in result
assert "z: no recursion" in result

print("All tests passed!")
