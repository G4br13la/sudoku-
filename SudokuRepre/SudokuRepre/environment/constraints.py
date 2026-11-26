"""Reglas y comprobaciones del Sudoku clásico y diagonal.

Este módulo no utiliza solucionadores externos: todas las restricciones se
comprueban explícitamente sobre una matriz 9 x 9.
"""
from __future__ import annotations

from typing import Iterable, Sequence
import math

SIZE = 9
DIGITS = set(range(1, 10))
VARIANTS = {"clasico", "diagonal"}


def normalize_board(board: Sequence[Sequence[object]]) -> tuple[tuple[int, ...], ...]:
    """Convierte una matriz de entrada en una tupla inmutable de enteros.

    Celdas vacías aceptadas: None, cadena vacía, '.', o 0.
    """
    if hasattr(board, "tolist"):
        board = board.tolist()  # NumPy / pandas
    if not isinstance(board, (list, tuple)) or len(board) != SIZE:
        raise ValueError("El tablero debe tener exactamente 9 filas.")

    rows: list[tuple[int, ...]] = []
    for r, row in enumerate(board):
        if hasattr(row, "tolist"):
            row = row.tolist()
        if not isinstance(row, (list, tuple)) or len(row) != SIZE:
            raise ValueError(f"La fila {r + 1} debe contener exactamente 9 celdas.")
        values: list[int] = []
        for c, raw in enumerate(row):
            if raw is None or raw == "" or raw == "." or (isinstance(raw, float) and math.isnan(raw)):
                value = 0
            else:
                try:
                    numeric = float(raw)
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"Valor no numérico en fila {r + 1}, columna {c + 1}.") from exc
                if not numeric.is_integer():
                    raise ValueError(f"La celda ({r + 1}, {c + 1}) debe ser un entero.")
                value = int(numeric)
            if not 0 <= value <= 9:
                raise ValueError(f"La celda ({r + 1}, {c + 1}) debe estar entre 0 y 9.")
            values.append(value)
        rows.append(tuple(values))
    return tuple(rows)


def _duplicate_values(values: Iterable[int]) -> set[int]:
    seen: set[int] = set()
    duplicates: set[int] = set()
    for value in values:
        if value == 0:
            continue
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def validate_partial_board(
    board: Sequence[Sequence[object]], variant: str = "clasico"
) -> list[str]:
    """Devuelve los conflictos de un tablero parcial; vacío significa válido."""
    if variant not in VARIANTS:
        return [f"Variante desconocida: {variant}."]
    try:
        grid = normalize_board(board)
    except ValueError as exc:
        return [str(exc)]

    errors: list[str] = []
    for r in range(SIZE):
        duplicates = _duplicate_values(grid[r])
        if duplicates:
            errors.append(f"Fila {r + 1}: números repetidos {sorted(duplicates)}.")

    for c in range(SIZE):
        duplicates = _duplicate_values(grid[r][c] for r in range(SIZE))
        if duplicates:
            errors.append(f"Columna {c + 1}: números repetidos {sorted(duplicates)}.")

    for block_r in range(0, SIZE, 3):
        for block_c in range(0, SIZE, 3):
            values = (
                grid[r][c]
                for r in range(block_r, block_r + 3)
                for c in range(block_c, block_c + 3)
            )
            duplicates = _duplicate_values(values)
            if duplicates:
                errors.append(
                    f"Subcuadrícula ({block_r // 3 + 1}, {block_c // 3 + 1}): "
                    f"números repetidos {sorted(duplicates)}."
                )

    if variant == "diagonal":
        main = [grid[i][i] for i in range(SIZE)]
        secondary = [grid[i][SIZE - 1 - i] for i in range(SIZE)]
        duplicates = _duplicate_values(main)
        if duplicates:
            errors.append(f"Diagonal principal: números repetidos {sorted(duplicates)}.")
        duplicates = _duplicate_values(secondary)
        if duplicates:
            errors.append(f"Diagonal secundaria: números repetidos {sorted(duplicates)}.")

    return errors


def is_complete_board(board: Sequence[Sequence[object]]) -> bool:
    try:
        grid = normalize_board(board)
    except ValueError:
        return False
    return all(value != 0 for row in grid for value in row)


def validate_complete_board(
    board: Sequence[Sequence[object]], variant: str = "clasico"
) -> list[str]:
    errors = validate_partial_board(board, variant)
    if errors:
        return errors
    try:
        grid = normalize_board(board)
    except ValueError as exc:
        return [str(exc)]
    if any(value == 0 for row in grid for value in row):
        errors.append("El tablero está incompleto: todavía hay casillas vacías.")
    return errors


def candidates_for_cell(
    board: Sequence[Sequence[int]], row: int, col: int, variant: str = "clasico"
) -> list[int]:
    """Calcula los valores permitidos para una celda vacía."""
    if variant not in VARIANTS or not (0 <= row < SIZE and 0 <= col < SIZE):
        return []
    if board[row][col] != 0:
        return []

    forbidden = set(board[row])
    forbidden.update(board[r][col] for r in range(SIZE))

    start_r = (row // 3) * 3
    start_c = (col // 3) * 3
    forbidden.update(
        board[r][c]
        for r in range(start_r, start_r + 3)
        for c in range(start_c, start_c + 3)
    )

    if variant == "diagonal" and row == col:
        forbidden.update(board[i][i] for i in range(SIZE))
    if variant == "diagonal" and row + col == SIZE - 1:
        forbidden.update(board[i][SIZE - 1 - i] for i in range(SIZE))

    return sorted(DIGITS - forbidden)


def select_mrv_cell(
    board: Sequence[Sequence[int]], variant: str = "clasico"
) -> tuple[int, int, list[int]] | None:
    """Selecciona la celda vacía con menos candidatos (MRV).

    La selección es determinista: en caso de empate conserva el orden por filas.
    MRV es una regla de selección de variable dentro de la búsqueda, no un
    tercer algoritmo independiente.
    """
    best: tuple[int, int, list[int]] | None = None
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                candidates = candidates_for_cell(board, r, c, variant)
                if best is None or len(candidates) < len(best[2]):
                    best = (r, c, candidates)
                    if len(candidates) == 0:
                        return best
    return best
