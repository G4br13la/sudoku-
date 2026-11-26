"""Normalización y presentación de métricas de búsqueda."""
from __future__ import annotations


def result_to_row(result) -> dict:
    m = result.metrics
    solved = result.status == "solved"
    return {
        "Algoritmo": result.algorithm,
        "Estado": result.status,
        "Tiempo (s)": round(m.get("elapsed_seconds", 0.0), 6),
        "Nodos generados": m.get("nodes_generated", 0),
        "Nodos expandidos": m.get("nodes_expanded", 0),
        "Nodos visitados": m.get("nodes_visited", 0),
        "Frontera máxima": m.get("frontier_max", 0),
        "Memoria aprox. (MB)": round(m.get("estimated_memory_mb", 0.0), 4),
        "Longitud solución": m.get("solution_depth"),
        "Costo solución": m.get("solution_cost"),
        "Retrocesos": m.get("backtracks", 0),
        "Óptima": "Sí" if solved else ("No encontrada" if result.status == "unsolvable" else "No determinada"),
    }


def metrics_markdown(result) -> str:
    m = result.metrics
    return (
        f"**Algoritmo:** {result.algorithm}  \n"
        f"**Estado:** {result.status}  \n"
        f"**Tiempo:** {m.get('elapsed_seconds', 0):.6f} s  \n"
        f"**Generados:** {m.get('nodes_generated', 0):,}  ·  "
        f"**Expandidos:** {m.get('nodes_expanded', 0):,}  ·  "
        f"**Visitados:** {m.get('nodes_visited', 0):,}  \n"
        f"**Frontera máxima:** {m.get('frontier_max', 0):,}  ·  "
        f"**Memoria aproximada:** {m.get('estimated_memory_mb', 0):.4f} MB  \n"
        f"**Longitud:** {m.get('solution_depth')}  ·  "
        f"**Costo:** {m.get('solution_cost')}  ·  "
        f"**Retrocesos:** {m.get('backtracks', 0):,}"
    )
