from environment.constraints import (
    validate_complete_board,
    validate_partial_board,
)
from environment.sudoku import SudokuProblem
from instances.catalog import get_puzzle


def test_classic_catalog_boards_are_valid():
    for level in ("Facil", "Medio", "Dificil"):
        board = get_puzzle("clasico", level)
        assert validate_partial_board(board, "clasico") == []


def test_diagonal_catalog_boards_are_valid():
    for level in ("Facil", "Medio", "Dificil"):
        board = get_puzzle("diagonal", level)
        assert validate_partial_board(board, "diagonal") == []


def test_detects_classic_row_conflict():
    board = [row[:] for row in get_puzzle("clasico", "Facil")]
    board[0] = [5, 5, 0, 0, 0, 0, 0, 0, 0]
    assert any("Fila 1" in error for error in validate_partial_board(board, "clasico"))


def test_detects_diagonal_conflict():
    board = [row[:] for row in get_puzzle("diagonal", "Facil")]
    board[0][0] = 1
    board[4][4] = 1
    errors = validate_partial_board(board, "diagonal")
    assert any("Diagonal principal" in error for error in errors)


def test_solution_grid_is_complete_and_valid():
    solution = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [9, 3, 5, 2, 4, 1, 8, 6, 7],
        [6, 1, 7, 5, 3, 8, 2, 9, 4],
        [8, 4, 2, 6, 9, 7, 5, 3, 1],
        [2, 9, 8, 3, 1, 4, 6, 7, 5],
        [3, 7, 1, 8, 6, 5, 9, 4, 2],
        [5, 6, 4, 9, 7, 2, 3, 1, 8],
    ]
    assert validate_complete_board(solution, "diagonal") == []


def test_transition_preserves_given_cells_and_does_not_mutate_parent():
    board = get_puzzle("clasico", "Facil")
    problem = SudokuProblem(board, "clasico")
    original = problem.estado_inicial
    action = problem.acciones_aplicables(original)[0]
    child = problem.transicion(original, action)
    assert original == problem.estado_inicial
    assert child != original
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                assert child[r][c] == board[r][c]
