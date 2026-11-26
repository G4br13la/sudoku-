"""Definición del espacio de estados para Sudoku clásico y diagonal."""
from __future__ import annotations

from typing import Sequence

from .constraints import (
    VARIANTS,
    candidates_for_cell,
    is_complete_board,
    normalize_board,
    select_mrv_cell,
    validate_complete_board,
    validate_partial_board,
)

Action = tuple[int, int, int]  # (fila, columna, valor), índices desde cero
Board = tuple[tuple[int, ...], ...]


class SudokuProblem:
    """Problema de búsqueda compatible con el contrato del notebook de clase.

    Atributos/métodos equivalentes al material docente:
    estado_inicial, acciones_aplicables, transicion, test_objetivo, costo, codigo.
    """

    def __init__(self, estado_inicial: Sequence[Sequence[object]], variante: str = "clasico"):
        if variante not in VARIANTS:
            raise ValueError(f"La variante debe ser una de estas: {sorted(VARIANTS)}.")
        self.estado_inicial: Board = normalize_board(estado_inicial)
        self.variante = variante
        self.valores_iniciales = tuple(
            tuple(value != 0 for value in row) for row in self.estado_inicial
        )

    def validar_estado_inicial(self) -> list[str]:
        return validate_partial_board(self.estado_inicial, self.variante)

    def validar_tablero(self, estado: Sequence[Sequence[int]] | None = None) -> list[str]:
        return validate_partial_board(estado or self.estado_inicial, self.variante)

    def acciones_aplicables(self, estado: Board) -> list[Action]:
        """Genera asignaciones válidas para la celda elegida por MRV.

        Fijar una sola variable por estado evita generar permutaciones de orden
        de asignación y mantiene el mismo espacio de búsqueda para ambos métodos.
        """
        if validate_partial_board(estado, self.variante):
            return []
        selected = select_mrv_cell(estado, self.variante)
        if selected is None:
            return []
        row, col, candidates = selected
        return [(row, col, value) for value in candidates]

    def transicion(self, estado: Board, accion: Action) -> Board:
        row, col, value = accion
        if not (0 <= row < 9 and 0 <= col < 9 and 1 <= value <= 9):
            raise ValueError("La acción debe contener fila, columna y valor válidos.")
        if self.valores_iniciales[row][col]:
            raise ValueError("No se puede modificar una casilla dada inicialmente.")
        if estado[row][col] != 0:
            raise ValueError("La celda seleccionada ya está ocupada.")
        if value not in candidates_for_cell(estado, row, col, self.variante):
            raise ValueError("La asignación viola las restricciones del Sudoku.")

        mutable = [list(current_row) for current_row in estado]
        mutable[row][col] = value
        return tuple(tuple(current_row) for current_row in mutable)

    def test_objetivo(self, estado: Board) -> bool:
        return not validate_complete_board(estado, self.variante)

    def costo(self, estado: Board, accion: Action) -> int:
        """Costo unitario por asignación, siguiendo el ejemplo del notebook."""
        return 1

    def codigo(self, estado: Board) -> str:
        """Codificación canónica de las 81 celdas para detectar repetidos."""
        return "".join(str(value) for row in estado for value in row)

    def cantidad_vacias(self, estado: Board | None = None) -> int:
        board = estado if estado is not None else self.estado_inicial
        return sum(value == 0 for row in board for value in row)

    def candidatos(self, estado: Board, row: int, col: int) -> list[int]:
        return candidates_for_cell(estado, row, col, self.variante)

    def copiar(self) -> "SudokuProblem":
        return SudokuProblem(self.estado_inicial, self.variante)
