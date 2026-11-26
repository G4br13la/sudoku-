Sudoku Search Lab

Agente para la resolución automática de Sudoku mediante algoritmos de búsqueda

**Descripción**

Sudoku Search Lab es una aplicación interactiva desarrollada en Python que representa el Sudoku como un problema de búsqueda en espacios de estados y permite resolver Sudoku clásico y Sudoku diagonal mediante Backtracking y Dijkstra (búsqueda de costo uniforme). La interfaz está construida con Gradio e incluye generación de tableros, validación, animación del proceso de búsqueda, árbol de expansión y comparación de métricas.

**Objetivos**

- Representar Sudoku como un espacio de estados con restricciones.
- Resolver tableros mediante Backtracking y Dijkstra.
- Trabajar con Sudoku clásico y diagonal.
- Generar tableros con niveles Fácil, Medio y Difícil.
- Visualizar el proceso de búsqueda y comparar métricas.
  
**Entornos**

- Sudoku clásico: cada fila, columna y bloque 3×3 debe contener los dígitos 1–9 sin repetición.
- Sudoku diagonal: incorpora las reglas clásicas y exige que las dos diagonales principales también contengan los dígitos 1–9 sin repetición.
  
**Algoritmos**

**- Backtracking:** búsqueda recursiva en profundidad; asigna valores y retrocede cuando una decisión lleva a un estado inválido.

**- Dijkstra:** búsqueda de costo uniforme mediante frontera prioritaria. Cada asignación tiene costo unitario, por lo que se explora por niveles de costo (equivalente a BFS cuando los costos son uniformes).
Funcionalidades
- Selección de Sudoku clásico o diagonal.
- Dificultad Fácil, Medio o Difícil.
- Generación de tableros y edición de valores (usar 0 para casillas vacías).
- Validación de tablero.
- Resolución y registro de búsqueda con Backtracking o Dijkstra.
- Reproducción paso a paso: iniciar, pausar, reanudar, avanzar, retroceder y reiniciar.
- Visualización del tablero y árbol de expansión.
- Comparación de algoritmos mediante tabla y gráfica.
- Métricas: tiempo, nodos generados/expandidos/visitados, frontera o profundidad máxima, costo y memoria aproximada.

**Tecnologías**

|Librería	| Uso |
| -------- | -------- |
|Python |	Lenguaje principal |
|Gradio |	Interfaz web interactiva |
|Pandas	| Tablas de resultados y métricas |
|Plotly |	Gráficas de comparación |
|Pytest |	Pruebas automatizadas |


**Estructura del proyecto**

## Estructura del proyecto

```text
Sudoku_Aleatorio_VERIFICADO/
│
├── app.py
│
├── algorithms/
│   ├── backtracking.py
│   ├── common.py
│   └── dijkstra.py
│
├── environment/
│   ├── constraints.py
│   └── sudoku.py
│
├── instances/
│   ├── catalog.py
│   └── generator.py
│
├── evaluation/
│   ├── comparison.py
│   └── metrics.py
│
├── visualization/
│   ├── events.py
│   ├── playback.py
│   └── tree.py
│
├── interface/
│   ├── callbacks.py
│   └── layout.py
│
├── data/
│   ├── instances.json
│   └── solutions.json
│
├── notebooks/
│   └── proyecto_sudoku.ipynb
│
├── tests/
│
├── reference/
│
├── utils_busqueda.py
├── pruebas_experimentales.py
├── resultados_completos.csv
├── resultados_resumen.csv
└── utils_busqueda.py
```

**Requisitos previos**

- Python 3.11 o 3.12 recomendado (el proyecto también está preparado para Python 3.13).
- Git (opcional, si se clona el repositorio).
- Navegador web moderno.
  
**Instalación**
  
**1. Crear un entorno virtual:**

macOS / Linux
python3 -m venv .venv
Windows
py -m venv .venv

**2. Activar el entorno virtual:**

macOS / Linux
source .venv/bin/activate
Windows PowerShell
.\.venv\Scripts\Activate.ps1
Si PowerShell bloquea la activación, ejecute en esa misma terminal:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

**3. Instalar librerías:**

Desde la raíz del proyecto:
python -m pip install --upgrade pip
pip install -r requirements.txt
Ejecución
Con el entorno virtual activado y ubicado en la carpeta raíz:
python app.py
Gradio mostrará una dirección local. Abra en el navegador:
http://127.0.0.1:7860

Toca mantener abierta la terminal mientras se utiliza la aplicación y para detenerla, toca presionar Ctrl + C.
Uso de la aplicación
1. Seleccionar el entorno: Sudoku clásico o Sudoku diagonal.
2. Elijir la dificultad (Fácil, Medio o Difícil) o genere otro tablero.
3. Editar las casillas; 0 representa una casilla vacía.
4. Presionar "Validar tablero" para comprobar las restricciones.
5. Seleccione Backtracking o Dijkstra.
6. Presione Resolver y registrar búsqueda para ejecutar y registrar la exploración.
7. Use los controles de reproducción para recorrer los eventos de búsqueda.
8. Presione Comparar ambos algoritmos para actualizar la tabla y gráfica de métricas.
   
**Pruebas automatizadas**

Desde la raíz del proyecto, con el entorno virtual activo:
pytest -q
La suite verifica las restricciones, generación de instancias, algoritmos, comparación y visualización.
Capturas de pantalla
Las capturas se guardan dentro de screenshots/ y se insertan en el README con Markdown. Cree esa carpeta en la raíz del proyecto y use estos nombres:

**1. Pantalla principal:**

Captura la interfaz completa recién abierta, mostrando la selección del tipo de Sudoku y la dificultad.
Guarde como screenshots/01_inicio.png.

**2. Tablero generado:**

Captura un tablero con una dificultad seleccionada, que se vea el Sudoku y los controles de generación/validación.
Guarde como screenshots/02_tablero.png.

**3. Validación del tablero:**
   
Capture el resultado de pulsar Validar tablero, mostrando el mensaje de tablero válido (o la validación que se quiera documentar).
Guarde como screenshots/03_validacion.png.

**4. Ejecución de un algoritmo:**

Capture la interfaz luego de ejecutar Backtracking o Dijkstra, mostrando el tablero y el estado o resultado de la búsqueda.
Guarde como screenshots/04_busqueda.png.

**5. Visualización del árbol:**

Capture el árbol de expansión, incluyendo nodos/ramas y el estado del evento actual.
Guarde como screenshots/05_arbol.png.

**6. Comparación de algoritmos:**

Capture la tabla y la gráfica de comparación, con métricas visibles.
Guarde como screenshots/06_comparacion.png.
