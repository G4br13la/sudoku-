from algorithms.backtracking import solve_backtracking
from algorithms.dijkstra import solve_dijkstra
from environment.sudoku import SudokuProblem
from environment.constraints import validate_complete_board
from instances.catalog import get_puzzle


def test_backtracking_solves_classic_and_diagonal():
    for variant in ("clasico", "diagonal"):
        problem = SudokuProblem(get_puzzle(variant, "Facil"), variant)
        result = solve_backtracking(problem, time_limit_seconds=5, capture_events=True)
        assert result.status == "solved"
        assert validate_complete_board(result.solution, variant) == []
        assert result.metrics["solution_depth"] == problem.cantidad_vacias()
        assert result.events[0]["type"] == "initial"
        assert result.events[-1]["type"] == "solution"


def test_dijkstra_solves_classic_and_diagonal():
    for variant in ("clasico", "diagonal"):
        problem = SudokuProblem(get_puzzle(variant, "Facil"), variant)
        result = solve_dijkstra(problem, time_limit_seconds=5, capture_events=True)
        assert result.status == "solved"
        assert validate_complete_board(result.solution, variant) == []
        assert result.metrics["solution_cost"] == problem.cantidad_vacias()


def test_dijkstra_reports_resource_limit_separately_from_unsolvable():
    problem = SudokuProblem(get_puzzle("clasico", "Dificil"), "clasico")
    result = solve_dijkstra(
        problem,
        max_expansions=0,
        time_limit_seconds=5,
        capture_events=False,
    )
    assert result.status == "limit_reached"
    assert result.solution is None


def test_invalid_board_is_rejected_by_search():
    board = [row[:] for row in get_puzzle("clasico", "Facil")]
    board[0][0] = board[0][4]
    result = solve_backtracking(SudokuProblem(board, "clasico"), capture_events=False)
    assert result.status == "invalid"


def test_all_six_catalog_instances_are_solved_by_both_algorithms():
    for variant in ("clasico", "diagonal"):
        for level in ("Facil", "Medio", "Dificil"):
            board = get_puzzle(variant, level)
            bt = solve_backtracking(
                SudokuProblem(board, variant),
                max_expansions=250_000,
                time_limit_seconds=8,
                capture_events=False,
            )
            dijkstra = solve_dijkstra(
                SudokuProblem(board, variant),
                max_expansions=20_000,
                time_limit_seconds=8,
                max_frontier=40_000,
                capture_events=False,
            )
            assert bt.status == "solved", (variant, level, bt.message)
            assert dijkstra.status == "solved", (variant, level, dijkstra.message)
            assert validate_complete_board(bt.solution, variant) == []
            assert validate_complete_board(dijkstra.solution, variant) == []
