"""Callbacks de aplicación: cargan instancias, validan y ejecutan búsquedas."""
from __future__ import annotations

from environment.constraints import normalize_board
from environment.sudoku import SudokuProblem
from instances.catalog import get_puzzle
from instances.generator import generate_puzzle
from algorithms.backtracking import solve_backtracking
from algorithms.dijkstra import solve_dijkstra
from evaluation.comparison import compare_algorithms
from evaluation.metrics import metrics_markdown
from visualization.playback import board_html, event_at
from visualization.tree import expansion_tree_html
from visualization.events import event_label


def load_board(variant: str, difficulty: str):
    return get_puzzle(variant, difficulty)


def create_board(variant: str, difficulty: str, seed: int):
    return generate_puzzle(variant, difficulty, seed)


def validate_board_callback(board_data, variant: str):
    try:
        board = normalize_board(board_data)
        problem = SudokuProblem(board, variant)
    except Exception as exc:
        return f"<span style='color:#b42318'>Tablero inválido: {exc}</span>"
    errors = problem.validar_estado_inicial()
    if errors:
        return "<span style='color:#b42318'>" + "<br>".join(errors) + "</span>"
    return "<span style='color:#16834a'><b>Tablero válido.</b> No hay conflictos en las restricciones.</span>"


def run_algorithm_callback(board_data, variant: str, algorithm: str):
    try:
        board = normalize_board(board_data)
        problem = SudokuProblem(board, variant)
    except Exception as exc:
        return None, None, board_data, f"**Error de entrada:** {exc}", "", 0, "No se pudo iniciar la búsqueda.", expansion_tree_html(None, 0)

    if algorithm == "Dijkstra":
        result = solve_dijkstra(
            problem,
            max_expansions=20_000,
            time_limit_seconds=8.0,
            max_frontier=40_000,
            event_limit=6000,
            capture_events=True,
        )
    else:
        result = solve_backtracking(
            problem,
            max_expansions=250_000,
            time_limit_seconds=8.0,
            event_limit=6000,
            capture_events=True,
        )

    state = result.to_state()
    first_event = event_at(state, 0)
    if first_event:
        visual = board_html(first_event["board"], board, first_event, f"Sudoku {variant}")
    else:
        visual = board_html(board, board, None, f"Sudoku {variant}")
    status = f"**{result.status.upper()}** — {result.message}"
    metrics = metrics_markdown(result)
    total = len(state.get("events", []))
    label = event_label(first_event, 0, total) if total and first_event else "No hay eventos de búsqueda registrados."
    return state, visual, [list(row) for row in board], status, metrics, 0, label, expansion_tree_html(state, 0)


def render_step_callback(index, result_state, original_board, variant):
    event = event_at(result_state, index)
    if event is None:
        return board_html(original_board, original_board, None, f"Sudoku {variant}"), "Sin eventos registrados.", expansion_tree_html(None, 0)
    html = board_html(event["board"], original_board, event, f"Sudoku {variant}")
    events = result_state.get("events", [])
    label = event_label(event, int(index), len(events))
    if result_state.get("events_truncated"):
        label += "\n\n<small>El historial se truncó para controlar el uso de memoria.</small>"
    return html, label, expansion_tree_html(result_state, int(index))


def comparison_callback(board_data, variant: str):
    try:
        board = normalize_board(board_data)
        dataframe, figure, results, summary = compare_algorithms(
            board,
            variant,
            backtracking_expansions=250_000,
            dijkstra_expansions=20_000,
            time_limit_seconds=8.0,
        )
        return dataframe, figure, summary
    except Exception as exc:
        return None, None, f"**No se pudo ejecutar la comparación:** {exc}"
