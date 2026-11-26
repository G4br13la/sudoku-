"""Interfaz principal Gradio para las dos variantes de Sudoku."""
from __future__ import annotations

import gradio as gr

from instances.catalog import get_puzzle
from instances.generator import generate_puzzle
from visualization.playback import board_html
from visualization.events import event_label
from visualization.tree import expansion_tree_html
from environment.constraints import normalize_board
from .callbacks import (
    comparison_callback,
    render_step_callback,
    run_algorithm_callback,
    validate_board_callback,
)

CSS = """
.gradio-container {max-width: 1400px !important; margin: auto !important;}
#app-header {text-align:center; padding:22px 12px 12px;}
#app-header h1 {font-size:2.25rem; letter-spacing:-.04em;}
.hero-card {border:1px solid var(--border-color-primary); border-radius:20px; padding:24px; min-height:155px; background:linear-gradient(135deg, rgba(123,97,255,.10), rgba(46,196,182,.08));}
.hero-card h2 {margin-top:0;}
.section-card {border:1px solid var(--border-color-primary); border-radius:16px; padding:16px;}
.primary-btn button {font-weight:700 !important;}
"""


def _home_result(variant: str):
    board = generate_puzzle(variant, "Facil")
    title = "Sudoku clásico" if variant == "clasico" else "Sudoku diagonal"
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        variant,
        f"# {title}\nSelecciona una dificultad, edita una instancia o ejecuta los algoritmos.",
        board,
        board,
        board_html(board, board, None, title),
        None,
        0,
        "Sin ejecución. Selecciona un algoritmo para comenzar.",
        "",
        "",
        None,
        None,
        "Pulsa Comparar o Resolver. Los dos métodos se ejecutan sobre el mismo tablero inicial.",
        gr.update(active=False),
        gr.update(value="Facil"),
        expansion_tree_html(None, 0),
    )


def create_app():
    initial_board = get_puzzle("clasico", "Facil")
    with gr.Blocks(title="Sudoku Search Lab") as demo:
        variant_state = gr.State("clasico")
        original_board_state = gr.State(initial_board)
        result_state = gr.State(None)

        with gr.Column(visible=True) as home_screen:
            gr.Markdown(
                "# Sudoku Search Lab\n### Laboratorio interactivo de búsqueda en espacios de estados",
                elem_id="app-header",
            )
            gr.Markdown(
                "Explora cómo **Backtracking** y **Dijkstra** resuelven dos variantes del Sudoku. "
                "Visualiza decisiones, retrocesos, frontera de búsqueda y métricas sobre la misma instancia."
            )
            with gr.Row(equal_height=True):
                with gr.Column(elem_classes=["hero-card"]):
                    gr.Markdown("## 🟣 Sudoku clásico\n\nReglas de filas, columnas y bloques de 3 × 3.")
                    classic_button = gr.Button("Abrir Sudoku clásico", variant="primary", elem_classes=["primary-btn"])
                with gr.Column(elem_classes=["hero-card"]):
                    gr.Markdown("## 🟢 Sudoku diagonal\n\nReglas clásicas más las dos diagonales principales.")
                    diagonal_button = gr.Button("Abrir Sudoku diagonal", variant="primary", elem_classes=["primary-btn"])
            gr.Markdown(
                "**Leyenda:** los valores iniciales no se modifican; las asignaciones se exploran "
                "paso a paso y el resultado se valida antes de presentarse."
            )

        with gr.Column(visible=False) as workspace:
            variant_title = gr.Markdown("# Sudoku clásico")
            with gr.Row():
                difficulty = gr.Dropdown(
                    choices=[("Fácil", "Facil"), ("Medio", "Medio"), ("Difícil", "Dificil")],
                    value="Facil",
                    label="Dificultad",
                    scale=1,
                )
                algorithm = gr.Radio(
                    choices=["Backtracking", "Dijkstra"],
                    value="Backtracking",
                    label="Algoritmo para animación",
                    scale=2,
                )
                speed = gr.Slider(0.15, 2.0, value=0.55, step=0.05, label="Velocidad (segundos por paso)", scale=2)

            with gr.Row(equal_height=True):
                with gr.Column(scale=5, elem_classes=["section-card"]):
                    gr.Markdown("### Tablero editable")
                    gr.Markdown("Usa **0** o una celda vacía para representar una casilla sin número. Editar un tablero establece sus valores no vacíos como datos iniciales.")
                    board_editor = gr.Dataframe(
                        value=initial_board,
                        headers=[str(i) for i in range(1, 10)],
                        row_count=9,
                        column_count=9,
                        datatype="number",
                        type="array",
                        interactive=True,
                        show_row_numbers=True,
                        wrap=True,
                        label="Matriz 9 × 9",
                        max_height=430,
                    )
                    with gr.Row():
                        generate_button = gr.Button("Generar otro tablero", variant="secondary")
                        reset_button = gr.Button("Reiniciar tablero", variant="secondary")
                    with gr.Row():
                        validate_button = gr.Button("Validar tablero")
                        validation_output = gr.Markdown("")
                    with gr.Row():
                        run_button = gr.Button("Resolver y registrar búsqueda", variant="primary")
                        compare_button = gr.Button("Comparar ambos algoritmos", variant="stop")
                    back_button = gr.Button("← Volver al inicio", variant="link")
                with gr.Column(scale=6, elem_classes=["section-card"]):
                    gr.Markdown("### Proceso de búsqueda")
                    board_view = gr.HTML(board_html(initial_board, initial_board, None, "Sudoku clásico"))
                    status_output = gr.Markdown("Sin ejecución. Selecciona un algoritmo para comenzar.")
                    metrics_output = gr.Markdown("")

            with gr.Column(elem_classes=["section-card"]):
                gr.Markdown("### Controles de animación")
                step_slider = gr.Slider(0, 1000, value=0, step=1, label="Paso de búsqueda")
                step_label = gr.Markdown("Sin eventos registrados.")
                with gr.Row():
                    play_button = gr.Button("▶ Iniciar animación", variant="primary")
                    pause_button = gr.Button("⏸ Pausar")
                    resume_button = gr.Button("▶ Reanudar")
                    previous_button = gr.Button("← Retroceder")
                    next_button = gr.Button("Avanzar →")
                    restart_animation_button = gr.Button("↺ Reiniciar")
                timer = gr.Timer(value=0.55, active=False)

            with gr.Column(elem_classes=["section-card"]):
                gr.Markdown("### Comparación experimental")
                gr.Markdown("**Automática al resolver** o al pulsar «Comparar ambos algoritmos». "
                            "Se comparan ejecuciones independientes con el mismo tablero de entrada.")
                comparison_note = gr.Markdown("La comparación aparecerá aquí.")
                comparison_table = gr.Dataframe(
                    value=None,
                    interactive=False,
                    label="Métricas de Backtracking y Dijkstra",
                    wrap=True,
                )
                comparison_plot = gr.Plot(label="Comparación de nodos")


            with gr.Column(elem_classes=["section-card"]):
                gr.Markdown("### Árbol de expansión paso a paso")
                gr.Markdown("**Grafo real de estados explorados**: las flechas son asignaciones de celdas. "
                            "Usa los mismos controles de arriba para retroceder o avanzar; "
                            "la vista se centra en la rama activa y sus vecinos para seguir siendo legible.")
                graph_view = gr.HTML(expansion_tree_html(None, 0))


        open_outputs = [
            home_screen, workspace, variant_state, variant_title, board_editor,
            original_board_state, board_view, result_state, step_slider,
            status_output, metrics_output, step_label, comparison_table,
            comparison_plot, comparison_note, timer, difficulty, graph_view,
        ]
        classic_button.click(fn=lambda: _home_result("clasico"), outputs=open_outputs)
        diagonal_button.click(fn=lambda: _home_result("diagonal"), outputs=open_outputs)

        def load_difficulty(variant, level):
            board = generate_puzzle(variant, level)
            title = "Sudoku clásico" if variant == "clasico" else "Sudoku diagonal"
            return (
                board, board, board_html(board, board, None, title), None,
                "Tablero nuevo cargado.", "", "", gr.update(value=0, maximum=1000),
                None, None, "Pulsa Comparar o Resolver para calcular las métricas.", gr.update(active=False),
                expansion_tree_html(None, 0),
            )

        difficulty.input(
            fn=load_difficulty,
            inputs=[variant_state, difficulty],
            outputs=[board_editor, original_board_state, board_view, result_state,
                     status_output, metrics_output, step_label, step_slider,
                     comparison_table, comparison_plot, comparison_note, timer, graph_view],
        )

        def generate_new(variant, level):
            board = generate_puzzle(variant, level)
            title = "Sudoku clásico" if variant == "clasico" else "Sudoku diagonal"
            return (
                board, board, board_html(board, board, None, title),
                None, "Se generó un tablero válido con solución única.", "", "",
                gr.update(value=0, maximum=1000), None, None,
                "Pulsa Comparar o Resolver para calcular las métricas.", gr.update(active=False),
                expansion_tree_html(None, 0),
            )

        generate_button.click(
            fn=generate_new,
            inputs=[variant_state, difficulty],
            outputs=[board_editor, original_board_state, board_view,
                     result_state, status_output, metrics_output, step_label,
                     step_slider, comparison_table, comparison_plot, comparison_note, timer, graph_view],
        )

        def reset_board(original, variant):
            title = "Sudoku clásico" if variant == "clasico" else "Sudoku diagonal"
            return (
                original, board_html(original, original, None, title), "Tablero reiniciado.",
                None, "", gr.update(value=0, maximum=1000), "Sin eventos registrados.",
                gr.update(active=False), None, None, "Pulsa Comparar o Resolver para calcular las métricas.", "",
                expansion_tree_html(None, 0),
            )

        reset_button.click(
            fn=reset_board,
            inputs=[original_board_state, variant_state],
            outputs=[board_editor, board_view, status_output, result_state, metrics_output,
                     step_slider, step_label, timer, comparison_table, comparison_plot,
                     comparison_note, validation_output, graph_view],
        )

        validate_button.click(
            fn=validate_board_callback,
            inputs=[board_editor, variant_state],
            outputs=[validation_output],
        )

        def preview_board(board, variant):
            title = "Sudoku clásico" if variant == "clasico" else "Sudoku diagonal"
            try:
                normalized = normalize_board(board)
                visual = board_html(normalized, normalized, None, title)
                return (
                    visual, None, "Tablero editado. Valídalo antes de ejecutar la búsqueda.",
                    gr.update(value=0, maximum=1000), gr.update(active=False),
                    None, None, "Pulsa Comparar o Resolver para calcular las métricas.", "", "Sin eventos registrados.", "",
                    expansion_tree_html(None, 0),
                )
            except Exception:
                return (
                    "<p>No se puede mostrar el tablero. Verifica que sea una matriz 9 × 9.</p>",
                    None, "Formato de tablero incorrecto.", gr.update(value=0, maximum=1000),
                    gr.update(active=False), None, None, "Pulsa Comparar o Resolver para calcular las métricas.",
                    "", "Sin eventos registrados.", "", expansion_tree_html(None, 0),
                )

        board_editor.input(
            fn=preview_board,
            inputs=[board_editor, variant_state],
            outputs=[board_view, result_state, status_output, step_slider, timer,
                     comparison_table, comparison_plot, comparison_note, metrics_output,
                     step_label, validation_output, graph_view],
        )

        def run_and_display(board, variant, algo):
            state, html, initial, status, metrics, index, label, graph = run_algorithm_callback(board, variant, algo)
            max_index = max(0, len(state.get("events", [])) - 1) if state else 0
            # El usuario espera que la comparación se actualice al resolver.
            table, plot, note = comparison_callback(board, variant)
            return (
                state, html, initial, status, metrics,
                gr.update(value=index, maximum=max_index), label, gr.update(active=False),
                graph, table, plot, note,
            )

        run_button.click(
            fn=run_and_display,
            inputs=[board_editor, variant_state, algorithm],
            outputs=[result_state, board_view, original_board_state, status_output,
                     metrics_output, step_slider, step_label, timer, graph_view,
                     comparison_table, comparison_plot, comparison_note],
        )

        compare_button.click(
            fn=comparison_callback,
            inputs=[board_editor, variant_state],
            outputs=[comparison_table, comparison_plot, comparison_note],
        )

        step_slider.change(
            fn=render_step_callback,
            inputs=[step_slider, result_state, original_board_state, variant_state],
            outputs=[board_view, step_label, graph_view],
        )

        def previous_step(index, result):
            count = len(result.get("events", [])) if result else 0
            return max(0, min(int(index) - 1, max(0, count - 1)))

        def next_step(index, result):
            count = len(result.get("events", [])) if result else 0
            return max(0, min(int(index) + 1, max(0, count - 1)))

        previous_button.click(previous_step, inputs=[step_slider, result_state], outputs=[step_slider])
        next_button.click(next_step, inputs=[step_slider, result_state], outputs=[step_slider])

        def play_from_start(speed_value):
            return 0, gr.update(value=float(speed_value), active=True)

        def resume_play(speed_value):
            return gr.update(value=float(speed_value), active=True)

        play_button.click(play_from_start, inputs=[speed], outputs=[step_slider, timer])
        resume_button.click(resume_play, inputs=[speed], outputs=[timer])
        pause_button.click(lambda: gr.update(active=False), outputs=[timer])
        restart_animation_button.click(
            lambda: (0, gr.update(active=False)), outputs=[step_slider, timer]
        )

        def timer_tick(index, result, original, variant):
            count = len(result.get("events", [])) if result else 0
            if count == 0:
                return 0, board_html(original, original), "Sin eventos.", gr.update(active=False), expansion_tree_html(None, 0)
            next_index = min(int(index) + 1, count - 1)
            event = result["events"][next_index]
            title = "Sudoku clásico" if variant == "clasico" else "Sudoku diagonal"
            html = board_html(event["board"], original, event, title)
            label = event_label(event, next_index, count)
            return next_index, html, label, gr.update(active=next_index < count - 1), expansion_tree_html(result, next_index)

        timer.tick(
            fn=timer_tick,
            inputs=[step_slider, result_state, original_board_state, variant_state],
            outputs=[step_slider, board_view, step_label, timer, graph_view],
        )

        def return_home():
            return gr.update(visible=True), gr.update(visible=False), gr.update(active=False)

        back_button.click(return_home, outputs=[home_screen, workspace, timer])

    return demo
