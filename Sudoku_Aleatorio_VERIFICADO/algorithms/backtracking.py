"""Búsqueda en profundidad con retroceso para Sudoku."""
from __future__ import annotations

from time import perf_counter

from .common import SearchResult, SearchStats, build_solution_path, event_record, finish_metrics


def solve_backtracking(
    problem,
    *,
    max_expansions: int = 250_000,
    time_limit_seconds: float = 10.0,
    event_limit: int = 2500,
    capture_events: bool = True,
) -> SearchResult:
    """Resuelve un Sudoku mediante DFS y backtracking.

    La selección de la siguiente celda usa MRV (menos candidatos), compartida
    con el entorno. Esto reduce callejones sin salida sin introducir un tercer
    algoritmo de búsqueda.
    """
    started = perf_counter()
    stats = SearchStats()
    events: list[dict] = []
    truncated = False
    status = "unsolvable"
    message = "No se encontró una solución."
    found_actions: list[tuple[int, int, int]] | None = None
    initial_errors = problem.validar_estado_inicial()

    node_counter = 0

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
                # Conserva siempre el desenlace aunque se haya limitado el historial.
                events[-1] = event_record(event_type, board, message=text, action=action, stats=stats,
                                          node_id=node_id, parent_id=parent_id, depth=depth)

    emit("initial", problem.estado_inicial, "Estado inicial del Sudoku.", node_id=0, depth=0)

    if initial_errors:
        status = "invalid"
        message = "Tablero inicial inválido: " + " ".join(initial_errors)
        metrics = finish_metrics(stats, started, status)
        return SearchResult("Backtracking", status, None, [], [], events, metrics, message, truncated)

    if problem.test_objetivo(problem.estado_inicial):
        status = "solved"
        message = "El tablero inicial ya es una solución válida."
        stats.solution_depth = 0
        stats.solution_cost = 0
        solution = [list(row) for row in problem.estado_inicial]
        emit("solution", problem.estado_inicial, message)
        metrics = finish_metrics(stats, started, status)
        return SearchResult("Backtracking", status, solution, [], [solution], events, metrics, message, truncated)

    stop_reason: str | None = None

    def search(state, actions, depth, node_id, parent_id):
        nonlocal stop_reason, node_counter
        elapsed = perf_counter() - started
        if stats.nodes_expanded >= max_expansions:
            stop_reason = "Se alcanzó el límite de nodos expandidos."
            return None
        if elapsed >= time_limit_seconds:
            stop_reason = "Se alcanzó el límite de tiempo."
            return None

        code = problem.codigo(state)
        stats.unique_codes.add(code)
        stats.nodes_visited = len(stats.unique_codes)
        stats.frontier_current = depth + 1
        stats.frontier_max = max(stats.frontier_max, stats.frontier_current)

        if problem.test_objetivo(state):
            return actions

        stats.nodes_expanded += 1
        applicable = problem.acciones_aplicables(state)
        emit("expand", state, f"Expandiendo estado a profundidad {depth}.",
             node_id=node_id, parent_id=parent_id, depth=depth)

        if not applicable:
            emit("dead_end", state, "Callejón sin salida: no hay asignaciones válidas.",
                 node_id=node_id, parent_id=parent_id, depth=depth)
            return None

        for action in applicable:
            if stop_reason is not None:
                return None
            child = problem.transicion(state, action)
            stats.nodes_generated += 1
            node_counter += 1
            child_id = node_counter
            row, col, value = action
            emit(
                "try", child,
                f"Se prueba {value} en fila {row + 1}, columna {col + 1}.",
                action, node_id=child_id, parent_id=node_id, depth=depth + 1,
            )
            result = search(child, actions + [action], depth + 1, child_id, node_id)
            if result is not None:
                return result
            if stop_reason is not None:
                stats.frontier_current = depth + 1
                return None
            stats.frontier_current = depth + 1
            stats.backtracks += 1
            emit("backtrack", state, f"Se deshace la asignación {value} de ({row + 1}, {col + 1}).", action,
                 node_id=child_id, parent_id=node_id, depth=depth + 1)

        stats.frontier_current = depth
        return None

    found_actions = search(problem.estado_inicial, [], 0, 0, None)
    stats.frontier_current = 0

    if found_actions is not None:
        status = "solved"
        message = "Solución encontrada mediante búsqueda en profundidad con retroceso."
        final_state = problem.estado_inicial
        for action in found_actions:
            final_state = problem.transicion(final_state, action)
        solution = [list(row) for row in final_state]
        stats.solution_depth = len(found_actions)
        stats.solution_cost = float(sum(problem.costo(None, action) for action in found_actions))
        emit("solution", final_state, message, node_id=node_counter, depth=len(found_actions))
        path = build_solution_path(problem, found_actions)
        metrics = finish_metrics(stats, started, status)
        return SearchResult("Backtracking", status, solution, found_actions, path, events, metrics, message, truncated)

    if stop_reason:
        status = "limit_reached"
        message = stop_reason + " La ausencia de solución no está demostrada."
    else:
        status = "unsolvable"
        message = "La búsqueda agotó las alternativas: el tablero no tiene solución."
    emit("finished", problem.estado_inicial, message)
    metrics = finish_metrics(stats, started, status)
    return SearchResult("Backtracking", status, None, [], [], events, metrics, message, truncated)
