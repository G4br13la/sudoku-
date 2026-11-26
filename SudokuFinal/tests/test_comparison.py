from evaluation.comparison import compare_algorithms
from instances.catalog import get_puzzle


def test_comparison_uses_same_board_and_returns_both_algorithms():
    board = get_puzzle("clasico", "Facil")
    dataframe, figure, results, summary = compare_algorithms(board, "clasico")
    assert list(dataframe["Algoritmo"]) == ["Backtracking", "Dijkstra"]
    assert results[0].solution == results[1].solution or (
        results[0].status == "solved" and results[1].status == "solved"
    )
    assert figure is not None
    assert "mismo tablero inicial" in summary
