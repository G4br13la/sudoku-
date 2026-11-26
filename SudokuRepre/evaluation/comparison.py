"""Ejecución reproducible y comparación de Backtracking y Dijkstra."""
from __future__ import annotations

import pandas as pd
import plotly.express as px

from algorithms.backtracking import solve_backtracking
from algorithms.dijkstra import solve_dijkstra
from environment.sudoku import SudokuProblem
from .metrics import result_to_row


def compare_algorithms(
    board,
    variant: str,
    *,
    backtracking_expansions: int = 250_000,
    dijkstra_expansions: int = 20_000,
    time_limit_seconds: float = 8.0,
) -> tuple[pd.DataFrame, object, object, str]:
    """Ejecuta ambos algoritmos sobre copias idénticas de una misma instancia."""
    base = SudokuProblem(board, variant)
    errors = base.validar_estado_inicial()
    if errors:
        raise ValueError("Tablero inválido: " + " ".join(errors))

    # Dos objetos independientes evitan que una implementación altere la otra.
    problem_bt = SudokuProblem(base.estado_inicial, variant)
    problem_dijkstra = SudokuProblem(base.estado_inicial, variant)

    result_bt = solve_backtracking(
        problem_bt,
        max_expansions=backtracking_expansions,
        time_limit_seconds=time_limit_seconds,
        capture_events=False,
    )
    result_dijkstra = solve_dijkstra(
        problem_dijkstra,
        max_expansions=dijkstra_expansions,
        time_limit_seconds=time_limit_seconds,
        capture_events=False,
    )

    rows = [result_to_row(result_bt), result_to_row(result_dijkstra)]
    dataframe = pd.DataFrame(rows)

    metric_frame = pd.DataFrame(
        [
            {"Algoritmo": result.algorithm, "Métrica": "Generados", "Valor": result.metrics["nodes_generated"]}
            for result in (result_bt, result_dijkstra)
        ]
        + [
            {"Algoritmo": result.algorithm, "Métrica": "Expandidos", "Valor": result.metrics["nodes_expanded"]}
            for result in (result_bt, result_dijkstra)
        ]
        + [
            {"Algoritmo": result.algorithm, "Métrica": "Frontera máx.", "Valor": result.metrics["frontier_max"]}
            for result in (result_bt, result_dijkstra)
        ]
    )
    figure = px.bar(
        metric_frame,
        x="Métrica",
        y="Valor",
        color="Algoritmo",
        barmode="group",
        title="Comparación de trabajo de búsqueda",
        text_auto=True,
    )
    figure.update_layout(template="plotly_white", height=380, legend_title_text="")

    summary = (
        "**Cómo interpretar la comparación:** ambos métodos recibieron el mismo tablero inicial. "
        "La longitud de cualquier solución completa es igual al número de celdas vacías iniciales, "
        "porque cada transición asigna exactamente una celda. Con costo unitario, Dijkstra es búsqueda "
        "de costo uniforme y ordena por profundidad; el límite de recursos se informa como `limit_reached`, "
        "nunca como ausencia de solución. La memoria es una estimación basada en las estructuras de búsqueda."
    )
    return dataframe, figure, (result_bt, result_dijkstra), summary
