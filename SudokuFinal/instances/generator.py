"""Generación reproducible de tableros con unicidad comprobada."""
from __future__ import annotations

import random

from environment.constraints import candidates_for_cell, validate_partial_board, validate_complete_board

DIFFICULTY_CLUES = {
    "Facil": 48,
    "Medio": 40,
    "Dificil": 34,
}


def _generate_solution(variant: str, rng: random.Random) -> list[list[int]]:
    """Construye una solución desde cero con backtracking aleatorizado."""
    grid = [[0] * 9 for _ in range(9)]
    # El orden de las celdas resuelve aleatoriamente los empates de MRV.
    cells = [(r, c) for r in range(9) for c in range(9)]
    rng.shuffle(cells)

    def fill() -> bool:
        selected = None
        for row, col in cells:
            if grid[row][col] != 0:
                continue
            candidates = candidates_for_cell(grid, row, col, variant)
            if not candidates:
                return False
            if selected is None or len(candidates) < len(selected[2]):
                selected = (row, col, candidates)
        if selected is None:
            return True
        row, col, candidates = selected
        rng.shuffle(candidates)
        for value in candidates:
            grid[row][col] = value
            if fill():
                return True
            grid[row][col] = 0
        return False

    if not fill() or validate_complete_board(grid, variant):
        raise RuntimeError("No se pudo construir una solución completa válida.")
    return grid


def count_solutions(board, variant: str, limit: int = 2) -> int:
    """Cuenta soluciones hasta `limit`; se usa para validar unicidad."""
    if validate_partial_board(board, variant):
        return 0
    grid = [list(row) for row in board]
    count = 0

    def search():
        nonlocal count
        if count >= limit:
            return
        selected = None
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    candidates = candidates_for_cell(grid, r, c, variant)
                    if not candidates:
                        return
                    if selected is None or len(candidates) < len(selected[2]):
                        selected = (r, c, candidates)
                        if len(candidates) == 1:
                            break
            if selected is not None and len(selected[2]) == 1:
                break
        if selected is None:
            count += 1
            return
        row, col, candidates = selected
        for value in candidates:
            grid[row][col] = value
            search()
            grid[row][col] = 0
            if count >= limit:
                return

    search()
    return count


def generate_puzzle(variant: str, difficulty: str, seed: int | None = None) -> list[list[int]]:
    """Genera un Sudoku con solución única, reproducible con semilla explícita.

    Cada intento parte de una solución completa nueva. El nivel controla el
    número de pistas, no una clasificación universal de dificultad.
    """
    if variant not in ("clasico", "diagonal"):
        raise ValueError("Variante desconocida.")
    if difficulty not in DIFFICULTY_CLUES:
        raise ValueError("Dificultad debe ser Facil, Medio o Dificil.")

    target = DIFFICULTY_CLUES[difficulty]
    rng = random.Random(seed)
    # Si un orden de eliminación no alcanza el objetivo, prueba otro tablero.
    for _ in range(20):
        puzzle = _generate_solution(variant, rng)
        cells = [(r, c) for r in range(9) for c in range(9)]
        rng.shuffle(cells)
        clues = 81
        for row, col in cells:
            previous = puzzle[row][col]
            puzzle[row][col] = 0
            if count_solutions(puzzle, variant, limit=2) == 1:
                clues -= 1
                if clues == target:
                    return puzzle
            else:
                puzzle[row][col] = previous

    raise RuntimeError("No se pudo generar un tablero único con el número de pistas solicitado.")
