"""Dijkstra (búsqueda de costo uniforme) adaptado al espacio de Sudoku."""
from __future__ import annotations

from math import inf
from time import perf_counter

from utils_busqueda import ListaPrioritaria, Nodo, nodo_hijo, solucion as reconstruct_actions
from .common import SearchResult, SearchStats, build_solution_path, event_record, finish_metrics


def solve_dijkstra(
    problem,
    *,
    max_expansions: int = 20_000,
    time_limit_seconds: float = 8.0,
    max_frontier: int = 80_000,
    event_limit: int = 2500,
    capture_events: bool = True,
) -> SearchResult:
    """Ejecuta Dijkstra usando los nodos y la frontera del material de clase.

    Correcciones relevantes frente al notebook:
    - ListaPrioritaria(max_heap=False) extrae el menor costo.
    - Nodo usa el atributo costo_camino (no `costo`).
    - El control de repetidos se hace mediante códigos y best_cost; no se usa
      `hijo not in frontera`, operación no definida por la clase original.
    """
    started = perf_counter()
    stats = SearchStats()
    events: list[dict] = []
    truncated = False
    status = "unsolvable"
    message = "La frontera se agotó sin encontrar solución."

    node_counter = 0
    node_ids = {}
    node_parents = {}

    def emit(event_type, board, text, action=None, *, node_id=None, parent_id=None, depth=None):
        nonlocal truncated
        if not capture_events:
            return
        if len(events) < event_limit:
            events.append(event_record(event_type, board, message=text, action=action, stats=stats,
                                       node_id=node_id, parent_id=parent_id, depth=depth))
        else:
            truncated = True
            if event_type in ("solution", "finished") and events:
                events[-1] = event_record(event_type, board, message=text, action=action, stats=stats,
                                          node_id=node_id, parent_id=parent_id, depth=depth)

    initial_errors = problem.validar_estado_inicial()
    emit("initial", problem.estado_inicial, "Estado inicial del Sudoku.", node_id=0, depth=0)
    if initial_errors:
        status = "invalid"
        message = "Tablero inicial inválido: " + " ".join(initial_errors)
        metrics = finish_metrics(stats, started, status)
        return SearchResult("Dijkstra", status, None, [], [], events, metrics, message, truncated)

    if problem.test_objetivo(problem.estado_inicial):
        status = "solved"
        message = "El tablero inicial ya es una solución válida."
        stats.solution_depth = 0
        stats.solution_cost = 0
        solution = [list(row) for row in problem.estado_inicial]
        emit("solution", problem.estado_inicial, message)
        metrics = finish_metrics(stats, started, status)
        return SearchResult("Dijkstra", status, solution, [], [solution], events, metrics, message, truncated)

    start_code = problem.codigo(problem.estado_inicial)
    initial_node = Nodo(problem.estado_inicial, None, None, 0, start_code)
    node_ids[start_code] = 0
    node_parents[start_code] = None
    # La clase de clase usa max_heap=True como valor por defecto; para Dijkstra
    # debemos solicitar explícitamente el min-heap.
    frontier = ListaPrioritaria(max_heap=False)
    frontier.push(initial_node, 0)
    best_cost = {start_code: 0}
    explored: set[str] = set()
    goal_node: Nodo | None = None
    stop_reason: str | None = None
    stats.frontier_current = len(frontier)
    stats.frontier_max = len(frontier)

    while not frontier.is_empty():
        if stats.nodes_expanded >= max_expansions:
            stop_reason = "Se alcanzó el límite de nodos expandidos."
            break
        if perf_counter() - started >= time_limit_seconds:
            stop_reason = "Se alcanzó el límite de tiempo."
            break
        if len(frontier) > max_frontier:
            stop_reason = "Se alcanzó el límite de tamaño de frontera."
            break

        node, priority = frontier.pop()
        stats.frontier_current = len(frontier)

        # Descarta entradas obsoletas o un estado ya expandido.
        if node.codigo in explored or node.costo_camino != best_cost.get(node.codigo, inf):
            continue

        explored.add(node.codigo)
        stats.unique_codes.add(node.codigo)
        stats.nodes_visited = len(explored)
        emit("expand", node.estado, f"Se extrae de la frontera un estado con costo acumulado {node.costo_camino}.",
             node_id=node_ids[node.codigo], parent_id=node_parents[node.codigo],
             depth=int(node.costo_camino))

        if problem.test_objetivo(node.estado):
            goal_node = node
            break

        stats.nodes_expanded += 1
        actions = problem.acciones_aplicables(node.estado)
        if not actions:
            emit("dead_end", node.estado, "Estado sin sucesores válidos.",
                 node_id=node_ids[node.codigo], parent_id=node_parents[node.codigo],
                 depth=int(node.costo_camino))
            continue

        for action in actions:
            child = nodo_hijo(problem, node, action)
            stats.nodes_generated += 1
            old_cost = best_cost.get(child.codigo, inf)
            if child.codigo not in explored and child.costo_camino < old_cost:
                best_cost[child.codigo] = child.costo_camino
                node_counter += 1
                node_ids[child.codigo] = node_counter
                node_parents[child.codigo] = node_ids[node.codigo]
                frontier.push(child, child.costo_camino)
                stats.frontier_current = len(frontier)
                stats.frontier_max = max(stats.frontier_max, stats.frontier_current)
                row, col, value = action
                emit(
                    "enqueue", child.estado,
                    f"Se agrega a la frontera el valor {value} en ({row + 1}, {col + 1}); costo {child.costo_camino}.",
                    action, node_id=node_counter, parent_id=node_ids[node.codigo],
                    depth=int(child.costo_camino),
                )

    if goal_node is not None:
        status = "solved"
        actions = reconstruct_actions(goal_node)
        final_state = goal_node.estado
        solution = [list(row) for row in final_state]
        stats.solution_depth = len(actions)
        stats.solution_cost = float(goal_node.costo_camino)
        message = "Solución encontrada mediante Dijkstra (costo uniforme)."
        emit("solution", final_state, message, node_id=node_ids[goal_node.codigo],
             parent_id=node_parents[goal_node.codigo], depth=int(goal_node.costo_camino))
        path = build_solution_path(problem, actions)
        metrics = finish_metrics(stats, started, status)
        return SearchResult("Dijkstra", status, solution, actions, path, events, metrics, message, truncated)

    if stop_reason:
        status = "limit_reached"
        message = stop_reason + " La ausencia de solución no está demostrada."
    else:
        status = "unsolvable"
        message = "La frontera se agotó: no existe solución alcanzable desde el tablero inicial."
    emit("finished", problem.estado_inicial, message)
    metrics = finish_metrics(stats, started, status)
    return SearchResult("Dijkstra", status, None, [], [], events, metrics, message, truncated)
