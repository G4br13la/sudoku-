# Sudoku Search Lab

Agente para la resolución automática de Sudoku mediante algoritmos de búsqueda

## Descripción
Sudoku Search Lab es una aplicación interactiva desarrollada en Python que representa el Sudoku como un problema de búsqueda en espacios de estados y permite resolver Sudoku clásico y Sudoku diagonal mediante Backtracking y Dijkstra (búsqueda de costo uniforme). La interfaz está construida con Gradio e incluye generación de tableros, validación, animación del proceso de búsqueda, árbol de expansión y comparación de métricas.

## Objetivos
- Representar Sudoku como un espacio de estados con restricciones.
- Resolver tableros mediante Backtracking y Dijkstra.
- Trabajar con Sudoku clásico y diagonal.
- Generar tableros con niveles Fácil, Medio y Difícil.
- Visualizar el proceso de búsqueda y comparar métricas.
  
## Entornos
- Sudoku clásico: cada fila, columna y bloque 3×3 debe contener los dígitos 1–9 sin repetición.
- Sudoku diagonal: incorpora las reglas clásicas y exige que las dos diagonales principales también contengan los dígitos 1–9 sin repetición.
  
## Algoritmos
- **Backtracking:** búsqueda recursiva en profundidad; asigna valores y retrocede cuando una decisión lleva a un estado inválido.

- **Dijkstra:** búsqueda de costo uniforme mediante frontera prioritaria. Cada asignación tiene costo unitario, por lo que se explora por niveles de costo (equivalente a BFS cuando los costos son uniformes).

## Funcionalidades
- Selección de Sudoku clásico o diagonal.
- Dificultad Fácil, Medio o Difícil.
- Generación aleatoria de tableros con solución única y edición de valores (usar 0 para casillas vacías).
- Niveles fácil (48 pistas), medio (40 pistas) y difícil (34 pistas). La cantidad de pistas no garantiza la dificultad real.
- Validación de tablero.
- Resolución y registro de búsqueda con Backtracking o Dijkstra.
- Reproducción paso a paso: iniciar, pausar, reanudar, avanzar, retroceder y reiniciar.
- Visualización del tablero y árbol de expansión.
- Comparación de algoritmos mediante tabla y gráfica.
- Métricas: tiempo, nodos generados/expandidos/visitados, frontera o profundidad máxima, costo y memoria aproximada.

## Tecnologías
|Librería	| Uso |
| -------- | -------- |
|Python |	Lenguaje principal |
|Gradio |	Interfaz web interactiva |
|NumPy | Manejo de arreglos numéricos |
|Pandas	| Tablas de resultados y métricas |
|Plotly |	Gráficas de comparación |
|Pytest |	Pruebas automatizadas |


## Estructura del proyecto

```text
SudokuRepre/
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
├── screenshots/
│   ├── 01_inicio.png
│   ├── 02_tablero.png
│   ├── 03_validacion.png
│   ├── 04_solucion.png
│   ├── 05_comparacion.png
│   └── 06_arbol.png
│
├── tests/
│
├── reference/
│
├── utils_busqueda.py
├── pruebas_experimentales.py
├── resultados_completos.csv
├── resultados_resumen.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Requisitos previos
- Python 3.13 recomendado (las pruebas experimentales se realizaron con Python 3.13.1).
- Git (opcional, si se clona el repositorio).
- Navegador web moderno.
  
## Instalación

Abrir una terminal en la carpeta raíz del proyecto, donde se encuentra `app.py`.

### Windows (PowerShell)

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación, ejecutar en esa misma terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecución

Con el entorno virtual activado y desde la raíz del proyecto:

```bash
python app.py
```

Abrir en el navegador la dirección local que muestra Gradio, normalmente `http://127.0.0.1:7860`.

Mantener abierta la terminal mientras se utiliza la aplicación. Para detenerla, presionar `Ctrl + C`.

## Uso de la aplicación
1. Seleccionar el entorno: Sudoku clásico o Sudoku diagonal.
2. Elegir la dificultad (Fácil, Medio o Difícil) o generar otro tablero.
3. Editar las casillas; 0 representa una casilla vacía.
4. Presionar "Validar tablero" para comprobar las restricciones.
5. Seleccionar Backtracking o Dijkstra.
6. Presionar **Resolver y registrar búsqueda** para ejecutar y registrar la exploración.
7. Usar los controles de reproducción para recorrer los eventos de búsqueda.
8. Presionar **Comparar ambos algoritmos** para actualizar la tabla y gráfica de métricas.
   
## Pruebas automatizadas
Desde la raíz del proyecto, con el entorno virtual activo:

```bash
python -m pytest -q
```

La suite verifica las restricciones, generación de instancias, algoritmos, comparación y visualización.

## Pruebas experimentales

Desde la raíz del proyecto:

```bash
python pruebas_experimentales.py
```

Se realizan tres ejecuciones por algoritmo e instancia, sobre seis tableros fijos del catálogo (36 pruebas), sin animación. Los archivos `resultados_completos.csv` y `resultados_resumen.csv` contienen las ejecuciones individuales y las medianas de las métricas. Ejecutar el script de nuevo reemplaza estos archivos.

Los resultados incluidos se obtuvieron en Windows 11, con un Intel Core i5-12500H y Python 3.13.1. La memoria es una estimación, no una medición directa de RAM. Si se alcanza un límite de búsqueda, se informa `limit_reached`, sin afirmar que el tablero no tiene solución.

## Notebook

El archivo `notebooks/proyecto_sudoku.ipynb` muestra la creación de una instancia, sus atributos y métodos, la generación de tableros y la aplicación de ambos algoritmos. Incluye ejemplos para Sudoku clásico y diagonal.

Para ejecutarlo desde VS Code, abrir la carpeta raíz del proyecto, seleccionar el kernel del entorno virtual y ejecutar las celdas. Si faltan las dependencias del notebook, instalarlas por separado:

```bash
python -m pip install ipykernel nbformat
```

## Capturas de pantalla

### 1. Pantalla principal

Selección del entorno de Sudoku clásico o diagonal.

![Pantalla principal](screenshots/01_inicio.png)

### 2. Configuración del tablero

Selección de dificultad, algoritmo y velocidad de reproducción, con opciones de generación y edición.

![Configuración del tablero](screenshots/02_tablero.png)

### 3. Validación del tablero

Comprobación de las restricciones y mensaje de tablero válido.

![Validación del tablero](screenshots/03_validacion.png)

### 4. Solución mediante Backtracking

Tablero resuelto, con las asignaciones del agente diferenciadas de las pistas iniciales.

![Solución del Sudoku](screenshots/04_solucion.png)

### 5. Comparación de algoritmos

Tabla de métricas y gráfica comparativa sobre una misma instancia.

![Comparación de algoritmos](screenshots/05_comparacion.png)

### 6. Árbol de expansión

Vista de los estados explorados y sus asignaciones durante la búsqueda.

![Árbol de expansión](screenshots/06_arbol.png)
