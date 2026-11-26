
import platform
import pandas as pd

from instances.catalog import get_puzzle
from environment.sudoku import SudokuProblem
from algorithms.backtracking import solve_backtracking
from algorithms.dijkstra import solve_dijkstra

# Configuración del experimento
variantes = ["clasico", "diagonal"]
dificultades = ["Facil", "Medio", "Dificil"]
repeticiones = 3

resultados = []

# Información del equipo
print("Python:", platform.python_version())
print("Sistema operativo:", platform.platform())
print("Procesador:", platform.processor())

for variante in variantes:
    for dificultad in dificultades:

        tablero = get_puzzle(variante, dificultad)
        pistas = sum(v != 0 for fila in tablero for v in fila)

        print(f"\nProbando: {variante} - {dificultad}")

        for repeticion in range(1, repeticiones + 1):

            algoritmos = [
                ("Backtracking", solve_backtracking, 250000),
                ("Dijkstra", solve_dijkstra, 20000)
            ]

            for nombre, algoritmo, limite in algoritmos:

                problema = SudokuProblem(tablero, variante)

                resultado = algoritmo(
                    problema,
                    max_expansions=limite,
                    time_limit_seconds=8.0,
                    capture_events=False
                )

                m = resultado.metrics

                resultados.append({
                    "Variante": variante,
                    "Dificultad": dificultad,
                    "Algoritmo": nombre,
                    "Repeticion": repeticion,
                    "Pistas": pistas,
                    "Estado": resultado.status,
                    "Tiempo_ms": m["elapsed_seconds"] * 1000,
                    "Generados": m["nodes_generated"],
                    "Expandidos": m["nodes_expanded"],
                    "Visitados": m["nodes_visited"],
                    "Frontera_maxima": m["frontier_max"],
                    "Memoria_MB": m["estimated_memory_mb"],
                    "Longitud": m["solution_depth"],
                    "Costo": m["solution_cost"],
                    "Retrocesos": m["backtracks"],
                    "Optima": "Si" if resultado.status == "solved"
                              else "No determinada"
                })

                print(
                    f"{nombre} | Prueba {repeticion} | "
                    f"{m['elapsed_seconds'] * 1000:.3f} ms | "
                    f"Estado: {resultado.status}"
                )

# Guardar las 36 ejecuciones
df = pd.DataFrame(resultados)

df.to_csv(
    "resultados_completos.csv",
    index=False,
    encoding="utf-8-sig"
)

# Calcular la mediana de las métricas numéricas
columnas = [
    "Tiempo_ms", "Generados", "Expandidos",
    "Visitados", "Frontera_maxima", "Memoria_MB",
    "Longitud", "Costo", "Retrocesos"
]

resumen = df.groupby(
    ["Variante", "Dificultad", "Algoritmo", "Estado"],
    sort=False
)[columnas].median().reset_index()

resumen.to_csv(
    "resultados_resumen.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n -RESULTADOS FINALES- \n")
print(resumen.to_string(index=False))

print("\nArchivos generados correctamente.")
