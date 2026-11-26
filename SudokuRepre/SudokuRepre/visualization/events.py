"""Etiquetas y utilidades para los eventos de búsqueda."""

EVENT_LABELS = {
    "initial": "Estado inicial",
    "expand": "Expansión de estado",
    "try": "Prueba de asignación",
    "enqueue": "Estado agregado a la frontera",
    "dead_end": "Callejón sin salida",
    "backtrack": "Retroceso",
    "solution": "Solución encontrada",
    "finished": "Búsqueda finalizada",
}


def event_label(event: dict, index: int, total: int) -> str:
    label = EVENT_LABELS.get(event.get("type"), event.get("type", "Evento"))
    stats = event.get("stats", {})
    detail = (
        f"\n\n**Generados:** {stats.get('nodes_generated', 0):,} · "
        f"**Expandidos:** {stats.get('nodes_expanded', 0):,} · "
        f"**Visitados:** {stats.get('nodes_visited', 0):,}  "
        f"\n**Frontera/pila actual:** {stats.get('frontier_current', 0):,} · "
        f"**Máximo:** {stats.get('frontier_max', 0):,} · "
        f"**Retrocesos:** {stats.get('backtracks', 0):,}"
    )
    return f"**Paso {index + 1} de {total}: {label}**  \n{event.get('message', '')}{detail}"
