"""Estructuras de búsqueda basadas en el material de clase.

Se conserva la interfaz ListaPrioritaria/Nodo/nodo_hijo del notebook. Para
Dijkstra se debe instanciar ListaPrioritaria(max_heap=False), porque la frontera
necesita extraer la prioridad mínima.
"""
from __future__ import annotations

import heapq
import itertools
from typing import Any


class ListaPrioritaria:
    """Cola prioritaria estable respaldada por heapq."""

    def __init__(self, *, max_heap: bool = False) -> None:
        self._heap: list[tuple[float, int, Any]] = []
        self._counter = itertools.count()
        self._sign = -1 if max_heap else 1

    def push(self, item: Any, priority: float) -> None:
        heapq.heappush(
            self._heap,
            (self._sign * float(priority), next(self._counter), item),
        )

    def pop(self) -> tuple[Any, float]:
        if not self._heap:
            raise IndexError("pop from empty PriorityQueue")
        priority, _, item = heapq.heappop(self._heap)
        return item, self._sign * priority

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def __contains__(self, item: Any) -> bool:
        return any(element is item for _, _, element in self._heap)

    def is_empty(self) -> bool:
        return not self._heap

    def __str__(self) -> str:
        return str([(item, priority * self._sign) for priority, _, item in self._heap])


class Nodo:
    """Nodo de búsqueda: estado, padre, acción, costo acumulado y código."""

    def __init__(self, estado, madre, accion, costo_camino, codigo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo_camino = costo_camino
        self.codigo = codigo


def nodo_hijo(problema, madre: Nodo, accion) -> Nodo:
    """Construye un nodo sucesor usando la interfaz del problema."""
    estado = problema.transicion(madre.estado, accion)
    costo_camino = madre.costo_camino + problema.costo(madre.estado, accion)
    codigo = problema.codigo(estado)
    return Nodo(estado, madre, accion, costo_camino, codigo)


def solucion(nodo: Nodo) -> list:
    """Reconstruye las acciones desde el nodo inicial hasta el nodo dado."""
    actions = []
    current = nodo
    while current is not None and current.madre is not None:
        actions.append(current.accion)
        current = current.madre
    actions.reverse()
    return actions
