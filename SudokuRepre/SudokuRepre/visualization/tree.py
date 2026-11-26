"""Árbol de expansión SVG a partir de los eventos reales de los buscadores.

No sintetiza nodos: muestra una ventana local del grafo registrado hasta el paso elegido.
Cada nodo contiene id, profundidad y asignación; los colores representan eventos reales.
"""
from __future__ import annotations

from collections import defaultdict
from html import escape

COLORS = {
    "initial": ("#e6e8f0", "#49516c"),
    "try": ("#d9edff", "#2367a1"),
    "enqueue": ("#d9edff", "#2367a1"),
    "expand": ("#c9f1db", "#23754a"),
    "dead_end": ("#ffe2c5", "#9a5a22"),
    "backtrack": ("#ffd9dc", "#ae3845"),
    "solution": ("#baf1ce", "#12723c"),
}


def expansion_tree_html(result_state: dict | None, index: int) -> str:
    events = (result_state or {}).get("events", [])
    if not events:
        return '<div style="padding:16px">Ejecuta un algoritmo para ver su árbol de expansión.</div>'
    end = min(max(0, int(index)), len(events) - 1)
    nodes = {}
    children = defaultdict(list)
    for event in events[:end + 1]:
        nid = event.get("node_id")
        if nid is None:
            continue
        pid = event.get("parent_id")
        if nid not in nodes:
            action = event.get("action")
            nodes[nid] = {"parent": pid, "depth": event.get("depth") or 0,
                          "action": action, "type": event["type"]}
            if pid is not None:
                children[pid].append(nid)
        nodes[nid]["type"] = event["type"]

    current_id = events[end].get("node_id")
    if current_id is None or current_id not in nodes:
        current_id = max(nodes) if nodes else 0
    if not nodes:
        return '<div style="padding:16px">Sin nodos registrados.</div>'

    # Ruta de antecesores, más hermanos y descendientes inmediatos, manteniendo
    # la visualización manejable incluso con miles de estados expandidos.
    ancestors = []
    seen = set()
    nid = current_id
    while nid is not None and nid in nodes and nid not in seen:
        ancestors.append(nid)
        seen.add(nid)
        nid = nodes[nid]["parent"]
    ancestors.reverse()
    core = ancestors[-5:]
    selected = set(core)
    for nid in core:
        pid = nodes[nid]["parent"]
        if pid is not None:
            selected.update(children[pid][:8])
        selected.update(children[nid][:8])
    # Evita un SVG gigantesco, conserva siempre la ruta activa.
    extra = sorted(selected - set(core), key=lambda n: (nodes[n]["depth"], n))
    selected = set(core + extra[:max(0, 43 - len(core))])
    levels = defaultdict(list)
    for nid in selected:
        levels[nodes[nid]["depth"]].append(nid)
    for depth in levels:
        levels[depth].sort()
    min_depth = min(levels)
    max_depth = max(levels)
    max_width = max(len(v) for v in levels.values())
    width = max(750, max_width * 138 + 40)
    height = max(185, (max_depth - min_depth + 1) * 112 + 35)
    positions = {}
    for depth, ids in levels.items():
        count = len(ids)
        for idx, nid in enumerate(ids):
            positions[nid] = (width * (idx + 1) / (count + 1), 58 + (depth - min_depth) * 112)

    edges = []
    boxes = []
    for nid in sorted(selected):
        data = nodes[nid]
        x, y = positions[nid]
        pid = data["parent"]
        if pid in positions:
            px, py = positions[pid]
            edges.append(f'<path d="M {px:.1f} {py+24:.1f} C {px:.1f} {py+58:.1f}, {x:.1f} {y-58:.1f}, {x:.1f} {y-24:.1f}" '
                         'stroke="#a8b2c3" stroke-width="2" fill="none"/>')
        depth_value = data["depth"]
        kind = data["type"]
        fill, stroke = COLORS.get(kind, COLORS["initial"])
        active = nid == current_id
        if active:
            stroke = "#4338ca"
        action = data["action"]
        label = f'F{action[0]+1} C{action[1]+1} = {action[2]}' if action else "Raíz"
        boxes.append(
            f'<g><title>{escape(f"Nodo {nid}, profundidad {depth_value}, {label}, {kind}")}</title>'
            f'<rect x="{x-56:.1f}" y="{y-23:.1f}" width="112" height="48" rx="9" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{3 if active else 1.6}"/>'
            f'<text x="{x:.1f}" y="{y-5:.1f}" font-size="12" font-weight="700" '
            f'text-anchor="middle" fill="#26334a">#{nid} · P{data["depth"]}</text>'
            f'<text x="{x:.1f}" y="{y+13:.1f}" font-size="11" '
            f'text-anchor="middle" fill="#26334a">{escape(label)}</text></g>'
        )
    legend = (
        '<span style="color:#2367a1">● Generado/en frontera</span> &nbsp; '
        '<span style="color:#23754a">● Expandido</span> &nbsp; '
        '<span style="color:#ae3845">● Retroceso</span> &nbsp; '
        '<span style="color:#9a5a22">● Sin salida</span> &nbsp; '
        '<span style="color:#4338ca">▣ Nodo actual</span>'
    )
    hidden = max(0, len(nodes) - len(selected))
    note = f"Vista local: {len(selected)} de {len(nodes)} nodos registrados hasta este paso"
    if hidden:
        note += f"; {hidden} ocultos para mantener legible el árbol"
    return (
        '<div style="font-family:system-ui,sans-serif;color:var(--body-text-color,#283449)">'
        '<div style="font-size:12px;line-height:1.9;margin-bottom:8px">' + legend + '</div>'
        '<div style="overflow:auto;max-height:580px;background:var(--block-background-fill,#fff);'
        'border:1px solid var(--border-color-primary,#d9dfea);border-radius:12px">'
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="Árbol de expansión real de la búsqueda" viewBox="0 0 {width} {height}" '
        f'style="min-width:{min(width,1000)}px;width:100%;height:auto;display:block">'
        + "".join(edges) + "".join(boxes) + "</svg></div>"
        f'<p style="font-size:12px;opacity:.8;margin:9px 0">{escape(note)}. '
        'Cada rama corresponde a una asignación del Sudoku. F = fila; C = columna; P = profundidad. '
        'Retrocede o avanza para ver cuándo aparece y cambia cada nodo.</p></div>'
    )
