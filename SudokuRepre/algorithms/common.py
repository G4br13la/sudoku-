"""Tipos y utilidades comunes de los algoritmos de búsqueda."""
from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any


def board_to_list(board):
    return [list(row) for row in board]


@dataclass
class SearchStats:
    nodes_generated: int = 0
    nodes_expanded: int = 0
    nodes_visited: int = 0
    frontier_current: int = 0
    frontier_max: int = 0
    backtracks: int = 0
    solution_depth: int | None = None
    solution_cost: float | None = None
    elapsed_seconds: float = 0.0
    estimated_memory_bytes: int = 0
    unique_codes: set[str] = field(default_factory=set, repr=False)

    def snapshot(self) -> dict[str, Any]:
        return {
            "nodes_generated": self.nodes_generated,
            "nodes_expanded": self.nodes_expanded,
            "nodes_visited": self.nodes_visited,
            "frontier_current": self.frontier_current,
            "frontier_max": self.frontier_max,
            "backtracks": self.backtracks,
        }


@dataclass
class SearchResult:
    algorithm: str
    status: str
    solution: list[list[int]] | None
    actions: list[tuple[int, int, int]]
    solution_path: list[list[list[int]]]
    events: list[dict[str, Any]]
    metrics: dict[str, Any]
    message: str = ""
    events_truncated: bool = False

    def to_state(self) -> dict[str, Any]:
        """Representación serializable para guardar en gr.State de Gradio."""
        return {
            "algorithm": self.algorithm,
            "status": self.status,
            "solution": self.solution,
            "actions": [list(a) for a in self.actions],
            "solution_path": self.solution_path,
            "events": self.events,
            "metrics": self.metrics,
            "message": self.message,
            "events_truncated": self.events_truncated,
        }


def event_record(
    event_type: str,
    board,
    *,
    message: str,
    action=None,
    stats: SearchStats | None = None,
    node_id: int | None = None,
    parent_id: int | None = None,
    depth: int | None = None,
) -> dict[str, Any]:
    event = {
        "type": event_type,
        "board": board_to_list(board),
        "message": message,
        "action": list(action) if action is not None else None,
        "node_id": node_id,
        "parent_id": parent_id,
        "depth": depth,
    }
    if stats is not None:
        event["stats"] = stats.snapshot()
    return event


def finish_metrics(stats: SearchStats, started: float, status: str) -> dict[str, Any]:
    stats.elapsed_seconds = perf_counter() - started
    # Estimación conservadora, no medición exacta del consumo del proceso.
    # Un tablero en tuplas contiene 81 referencias y 81 enteros/objetos.
    state_bytes = 9 * (sys_tuple_size() + 9 * 28)
    if status == "solved" and stats.solution_depth is not None:
        pass
    # En Dijkstra la frontera contiene estados completos; en Backtracking el
    # máximo corresponde a la profundidad/pila recursiva.
    estimated = stats.frontier_max * state_bytes + len(stats.unique_codes) * 140
    stats.estimated_memory_bytes = int(estimated)
    return {
        "status": status,
        "elapsed_seconds": stats.elapsed_seconds,
        "nodes_generated": stats.nodes_generated,
        "nodes_expanded": stats.nodes_expanded,
        "nodes_visited": stats.nodes_visited,
        "frontier_current": stats.frontier_current,
        "frontier_max": stats.frontier_max,
        "backtracks": stats.backtracks,
        "solution_depth": stats.solution_depth,
        "solution_cost": stats.solution_cost,
        "estimated_memory_bytes": stats.estimated_memory_bytes,
        "estimated_memory_mb": stats.estimated_memory_bytes / (1024 * 1024),
    }


def sys_tuple_size() -> int:
    # Evita depender de una implementación específica del tamaño exacto de tupla.
    return 112


def build_solution_path(problem, actions):
    current = problem.estado_inicial
    path = [board_to_list(current)]
    for action in actions:
        current = problem.transicion(current, tuple(action))
        path.append(board_to_list(current))
    return path
