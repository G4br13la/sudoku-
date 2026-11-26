# Sudoku Search Lab

Aplicación interactiva para resolver y comparar Sudoku clásico y Sudoku diagonal mediante **Backtracking** y **Dijkstra (búsqueda de costo uniforme)**. La interfaz está construida con Gradio.

## 1. Funcionalidades

- Dos variantes integradas: Sudoku clásico y Sudoku diagonal.
- Tres niveles de instancia: Fácil (48 pistas), Medio (40 pistas) y Difícil (34 pistas). Son niveles internos de este proyecto, no una clasificación oficial universal; la dificultad también depende de la distribución de pistas y del esfuerzo medido.
- Catálogo reproducible para pruebas. La interfaz genera instancias nuevas al abrir una variante, cambiar el nivel o pulsar «Generar otro tablero». El generador crea una solución completa aleatoria desde cero, elimina pistas comprobando unicidad y permite una semilla explícita para reproducir experimentos.
- Validación de números, filas, columnas, bloques y diagonales.
- Comprobación de unicidad en el generador mediante búsqueda propia.
- Backtracking recursivo con registro de pruebas, callejones sin salida y retrocesos.
- Dijkstra con `Nodo`, `nodo_hijo` y `ListaPrioritaria`, siguiendo el contrato del notebook de clase.
- Animación paso a paso, reproducción automática, pausa, reanudación, avance, retroceso y reinicio.
- Métricas y comparación sobre copias independientes del mismo tablero.
- Límites de tiempo, nodos y frontera para evitar que las búsquedas grandes consuman recursos sin control.

## 2. Estructura

```text
Sudoku_Project/
├── app.py
├── environment/
│   ├── __init__.py
│   ├── constraints.py
│   └── sudoku.py
├── algorithms/
│   ├── __init__.py
│   ├── common.py
│   ├── backtracking.py
│   └── dijkstra.py
├── instances/
│   ├── __init__.py
│   ├── catalog.py
│   └── generator.py
├── evaluation/
│   ├── __init__.py
│   ├── metrics.py
│   └── comparison.py
├── visualization/
│   ├── __init__.py
│   ├── events.py
│   └── playback.py
├── interface/
│   ├── __init__.py
│   ├── callbacks.py
│   └── layout.py
├── tests/
├── notebooks/
├── data/
│   ├── instances.json
│   └── solutions.json
├── reference/
├── utils_busqueda.py
├── requirements.txt
└── README.md
```

## 3. Instalación en Windows (PowerShell)

Se recomienda Python 3.11 o 3.12.

```powershell
cd Sudoku_Project
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloquea la activación del entorno virtual, en esa terminal puedes ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Instalación en macOS / Linux

```bash
cd Sudoku_Project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Ejecutar la aplicación

Desde la carpeta raíz y con el entorno virtual activado:

```bash
python app.py
```

Abre en el navegador la dirección que indique Gradio, normalmente:

`http://127.0.0.1:7860`

## 6. Ejecutar las pruebas

```bash
pytest -q
```

Las pruebas verifican restricciones de ambas variantes, transiciones inmutables, resultados de los dos algoritmos, límites de recursos, unicidad de instancias y comparación.

## 7. Uso de la aplicación

1. Abre Sudoku clásico o Sudoku diagonal.
2. Selecciona Fácil, Medio o Difícil.
3. Puedes editar la matriz: usa `0` para una casilla vacía. Los valores no vacíos se consideran pistas iniciales al ejecutar.
4. Pulsa **Validar tablero** antes de buscar.
5. Selecciona Backtracking o Dijkstra y pulsa **Resolver y registrar búsqueda**.
6. Usa los controles de animación para reproducir la secuencia real de eventos.
7. Pulsa **Comparar ambos algoritmos** para obtener la tabla y la gráfica comparativa.

## 8. Interfaz de búsqueda compatible con el notebook

El entorno expone los métodos que se usan en el notebook de espacios de estados:

- `estado_inicial`
- `acciones_aplicables(estado)`
- `transicion(estado, accion)`
- `test_objetivo(estado)`
- `costo(estado, accion)`
- `codigo(estado)`

La acción es una terna `(fila, columna, valor)`, con índices de Python desde cero. El estado es una tupla inmutable de nueve tuplas.

`utils_busqueda.py` conserva la interfaz de clase `Nodo`, `nodo_hijo` y `ListaPrioritaria`. En Dijkstra se instancia `ListaPrioritaria(max_heap=False)` para extraer el menor costo. También se usa `costo_camino`, que es el atributo definido por `Nodo` en el material de clase.

## 9. Interpretación de Dijkstra en Sudoku

Cada transición asigna un valor a una celda y tiene costo 1. Por tanto, el costo acumulado es el número de asignaciones realizadas. Como todo tablero completo requiere asignar exactamente las casillas vacías iniciales, todas las soluciones completas de una misma instancia tienen la misma longitud y el mismo costo.

Con costos unitarios, Dijkstra es búsqueda de costo uniforme y expande por niveles de costo, igual que una búsqueda en anchura en el mismo grafo. No debe presentarse como si fuera una estrategia distinta de BFS bajo esta función de costo. La frontera puede crecer mucho; por eso el proyecto informa `limit_reached` cuando se alcanza un límite de recursos y no lo confunde con `unsolvable`.

La implementación usa MRV (mínimo número de candidatos) como regla determinista para seleccionar la próxima celda. Esa regla se comparte entre los algoritmos para que trabajen sobre el mismo espacio de estados. Backtracking sigue siendo una búsqueda en profundidad con retroceso; Dijkstra sigue siendo costo uniforme con frontera prioritaria.

## 10. Métricas y memoria

- **Generados:** nodos sucesores creados.
- **Expandidos:** estados procesados para producir sucesores.
- **Visitados:** códigos de estado únicos procesados.
- **Frontera máxima:** máximo de estados pendientes para Dijkstra; profundidad máxima de la pila recursiva para Backtracking. Estas estructuras no son idénticas y deben interpretarse con esa diferencia.
- **Memoria aproximada:** estimación a partir del número de estados retenidos y el tamaño aproximado de la representación; no sustituye un perfilador de memoria del proceso.
- **Tiempo:** medido durante la búsqueda, sin incluir la reproducción visual posterior.

## 11. Límites de ejecución

La interfaz utiliza límites conservadores por defecto:

- Backtracking: hasta 250.000 nodos expandidos y 8 segundos.
- Dijkstra: hasta 20.000 nodos expandidos, 40.000 elementos en frontera y 8 segundos.

Los límites pueden modificarse en `interface/callbacks.py`. Un estado `limit_reached` significa que la ejecución se detuvo por recursos y **no** demuestra que el tablero carezca de solución.

## 12. Notebook

`notebooks/proyecto_sudoku.ipynb` muestra la creación del entorno, sus métodos principales, una ejecución de Backtracking y otra de Dijkstra. Puede abrirse desde Jupyter o VS Code después de instalar los requisitos.


## Árbol de expansión y comparación (versión corregida)

- **Resolver y registrar búsqueda** dibuja el tablero, el **árbol real de expansión**, la
  información del nodo actual y **calcula automáticamente** una comparación independiente
  de Backtracking y Dijkstra sobre la misma instancia inicial.
- **Comparar ambos algoritmos** también sirve para actualizar la tabla y gráfica sin
  iniciar una animación nueva. No es necesario resolver cada algoritmo primero.
- En el **árbol**, cada nodo `#id · Pprofundidad` es un estado generado. Su etiqueta
  `Ffila Ccolumna = valor` indica la transición desde su padre. El color distingue
  estados generados/en frontera, expandidos, callejones sin salida, retrocesos y solución;
  el borde morado identifica el evento actual.
- Los botones **Retroceder**, **Avanzar**, **Iniciar**, **Pausar**, **Reanudar**, **Reiniciar**
  y el deslizador controlan **simultáneamente** tablero y árbol. El grafo muestra la ruta
  activa y sus ramas próximas, no miles de nodos superpuestos; indica cuántos están
  ocultos. Los nodos y conexiones provienen del registro real de los algoritmos.
- Para proteger el navegador, el historial de animación limita los eventos a 6000.
  En búsquedas mayores se conserva el evento de terminación y se indica el truncamiento;
  el árbol sólo muestra los nodos capturados (no inventa transiciones omitidas).
- Los límites de tiempo, expansiones y frontera se muestran como `limit_reached`, no
  como demostración de que el Sudoku es irresoluble.

### Windows: ejecución desde la carpeta ya extraída

Abre PowerShell en la carpeta que contiene `app.py` y ejecuta `python app.py`.
No vuelvas a hacer `cd Sudoku_Project` si ya estás dentro de esa carpeta.
Las dependencias son compatibles con el Python 3.13 instalado, siempre que
`pip install -r requirements.txt` haya finalizado correctamente.
Después abre http://127.0.0.1:7860 y deja la terminal ejecutándose.
