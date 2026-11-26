"""Punto de entrada de Sudoku Search Lab."""
from interface.layout import create_app, CSS
import gradio as gr


def main():
    app = create_app()
    app.queue(default_concurrency_limit=2).launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        theme=gr.themes.Soft(primary_hue="violet", secondary_hue="teal", neutral_hue="slate"),
        css=CSS,
    )


if __name__ == "__main__":
    main()
