"""Regression tests for synchronized search graph, history, and comparison."""
from algorithms.backtracking import solve_backtracking
from algorithms.dijkstra import solve_dijkstra
from environment.sudoku import SudokuProblem
from instances.catalog import get_puzzle
from interface.callbacks import comparison_callback, render_step_callback, run_algorithm_callback
from visualization.tree import expansion_tree_html


def test_graph_tracks_real_search_nodes_and_rewinds():
    board = get_puzzle('clasico', 'Facil')
    for solver in (solve_backtracking, solve_dijkstra):
        result = solver(SudokuProblem(board, 'clasico'), event_limit=500)
        assert result.status == 'solved'
        assert result.events[0]['node_id'] == 0
        assert all('node_id' in event for event in result.events)
        assert any(event['parent_id'] == 0 for event in result.events)
        at_start = expansion_tree_html(result.to_state(), 0)
        at_end = expansion_tree_html(result.to_state(), len(result.events)-1)
        assert '#0' in at_start
        assert 'Nodos' not in at_start or 'nodos registrados' in at_start
        assert 'svg' in at_end
        assert at_start != at_end


def test_callback_synchronizes_graph_and_board():
    board = get_puzzle('clasico', 'Facil')
    state, html, original, status, metrics, index, label, graph = run_algorithm_callback(board, 'clasico', 'Backtracking')
    assert 'SOLVED' in status
    assert len(state['events']) > 2
    assert 'svg' in graph
    a = render_step_callback(0, state, original, 'clasico')
    b = render_step_callback(len(state['events'])-1, state, original, 'clasico')
    assert len(a) == len(b) == 3
    assert a[0] != b[0]
    assert a[2] != b[2]


def test_comparison_callback_has_two_results():
    table, plot, status = comparison_callback(get_puzzle('clasico', 'Facil'), 'clasico')
    assert table.shape[0] == 2
    assert set(table['Algoritmo']) == {'Backtracking', 'Dijkstra'}
    assert plot is not None
    assert 'mismo tablero' in status


def test_termination_survives_trace_limit():
    board = get_puzzle('clasico', 'Facil')
    for solver in (solve_backtracking, solve_dijkstra):
        result = solver(SudokuProblem(board, 'clasico'), event_limit=5)
        assert len(result.events) == 5
        assert result.events[-1]['type'] == 'solution'
        assert result.events_truncated
