import heapq
import itertools
from typing import Tuple


class ListaPrioritaria():
    """
    Minimal priority queue backed by heapq.

    - Min-heap by default; pass max_heap=True for max-heap behavior.
    - Stable for equal priorities (insertion order preserved).
    """

    def __init__(self, *, max_heap: bool = True) -> None:
        self._heap: list[tuple[int | float, int]] = []
        self._counter = itertools.count()  # tie-breaker for stability
        self._sign = -1 if max_heap else 1

    def push(self, item, priority: int | float) -> None:
        """Insert (priority, item)."""
        heapq.heappush(self._heap, (self._sign * priority, next(self._counter), item))

    def pop(self) -> Tuple[int | float]:
        """
        Remove and return the (priority, item) with best priority.
        Raises IndexError if empty.
        """
        if not self._heap:
            raise IndexError("pop from empty PriorityQueue")
        p, _, item = heapq.heappop(self._heap)
        return (item, self._sign * p)

    # (Optional niceties)
    def __len__(self) -> int:  # allows: len(pq)
        return len(self._heap)

    def __bool__(self) -> bool:  # allows: if pq:
        return bool(self._heap)

    def __str__(self):
        cadena = '['
        inicial = True
        for valor, elemento in self._heap:
            if inicial:
                cadena += '(' + str(elemento) + ',' + str(valor) + ')'
                inicial = False
            else:
                cadena += ', (' + str(elemento) + ',' + str(valor) + ')'
        return cadena + ']'

    def is_empty(self):
        return not bool(self._heap)


class Nodo:

    # Clase para crear los nodos

    def __init__(self, estado, madre, accion, costo_camino, codigo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo_camino = costo_camino
        self.codigo = codigo

def nodo_hijo(problema, madre, accion):

    # Función para crear un nuevo nodo
    # Input: problema, que es un objeto de clase ocho_reinas
    #        madre, que es un nodo,
    #        accion, que es una acción que da lugar al estado del nuevo nodo
    # Output: nodo

    estado = problema.transicion(madre.estado, accion)
    costo_camino = madre.costo_camino + problema.costo(madre.estado, accion)
    codigo = problema.codigo(estado)
    return Nodo(estado, madre, accion, costo_camino, codigo)




