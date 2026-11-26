"""Renderizado HTML del tablero y herramientas de reproducción."""
from __future__ import annotations

from html import escape


def board_html(board, original_board=None, event=None, title="Tablero de Sudoku") -> str:
    original_board = original_board or [[0] * 9 for _ in range(9)]
    event = event or {}
    event_type = event.get("type", "")
    action = event.get("action")
    active_cell = tuple(action[:2]) if action else None
    current_board = board or original_board

    styles = """
    <style>
      .sdk-wrap{font-family:Inter,system-ui,sans-serif;max-width:620px;margin:8px auto;color:#202438}
      .sdk-title{font-weight:700;font-size:16px;margin:0 0 10px 2px;color:#36324d}
      .sdk-grid{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));border:3px solid #34304a;border-radius:10px;overflow:hidden;background:white;box-shadow:0 8px 28px rgba(40,35,70,.10)}
      .sdk-cell{aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;font-size:clamp(15px,2.3vw,23px);font-weight:600;border-right:1px solid #d9d9e5;border-bottom:1px solid #d9d9e5;min-width:0}
      .sdk-cell.given{background:#ecebf2;color:#37334b;font-weight:800}
      .sdk-cell.filled{background:#f8f8fc;color:#4d4a62}
      .sdk-cell.current{background:#d9e9ff;color:#1158a6;box-shadow:inset 0 0 0 3px #4389d6}
      .sdk-cell.backtrack{background:#ffe1e1;color:#9f2727;box-shadow:inset 0 0 0 3px #df6565}
      .sdk-cell.solution{background:#d9f5e4;color:#176b3e}
      .sdk-cell:nth-child(3n){border-right:3px solid #77738d}
      .sdk-cell:nth-child(9n){border-right:0}
      .sdk-cell:nth-child(n+19):nth-child(-n+27),.sdk-cell:nth-child(n+46):nth-child(-n+54){border-bottom:3px solid #77738d}
      .sdk-cell:nth-child(n+73){border-bottom:0}
      .sdk-legend{display:flex;flex-wrap:wrap;gap:8px 14px;margin:12px 2px 2px;font-size:12px;color:#55536a}
      .sdk-key{display:inline-flex;align-items:center;gap:5px}
      .sdk-dot{width:12px;height:12px;border-radius:3px;display:inline-block;border:1px solid #c7c7d4}
      .sdk-note{font-size:12px;color:#77738d;margin:8px 2px}
      @media(max-width:500px){.sdk-cell{font-size:14px}.sdk-wrap{margin:0}}
    </style>
    """

    cells = []
    for r in range(9):
        for c in range(9):
            value = current_board[r][c]
            was_given = original_board[r][c] != 0
            cls = "given" if was_given else ("filled" if value else "")
            if event_type == "solution" and value and not was_given:
                cls = "solution"
            if active_cell == (r, c):
                cls = "backtrack" if event_type == "backtrack" else "current"
            shown = str(value) if value else "·"
            cells.append(f'<div class="sdk-cell {cls}">{escape(shown)}</div>')

    return (
        styles
        + '<div class="sdk-wrap">'
        + f'<div class="sdk-title">{escape(title)}</div>'
        + '<div class="sdk-grid">' + "".join(cells) + '</div>'
        + '<div class="sdk-legend">'
        + '<span class="sdk-key"><i class="sdk-dot" style="background:#ecebf2"></i>Inicial</span>'
        + '<span class="sdk-key"><i class="sdk-dot" style="background:#d9e9ff"></i>Evaluando / frontera</span>'
        + '<span class="sdk-key"><i class="sdk-dot" style="background:#ffe1e1"></i>Retroceso</span>'
        + '<span class="sdk-key"><i class="sdk-dot" style="background:#d9f5e4"></i>Solución</span>'
        + '</div>'
        + '<div class="sdk-note">Las celdas dadas originalmente permanecen protegidas durante la búsqueda.</div>'
        + '</div>'
    )


def event_at(result_state: dict | None, index: int) -> dict | None:
    if not result_state:
        return None
    events = result_state.get("events", [])
    if not events:
        return None
    index = max(0, min(int(index), len(events) - 1))
    return events[index]
