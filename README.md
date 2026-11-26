# sudoku-
es un proyecto de representacion y solucion automatica de problemas donde utilizamos diferentes métodos para solucionar el juego en diferentes dificultades

# Sudoku Search Lab
### Agente para la resolución automática de Sudoku mediante algoritmos de búsqueda

## Descripción

Sudoku Search Lab es un proyecto desarrollado en Python que implementa un agente capaz de resolver instancias de Sudoku clásico y Sudoku diagonal mediante algoritmos de búsqueda. La aplicación integra la generación de tableros, validación de restricciones, ejecución y visualización de los procesos de búsqueda, así como la evaluación comparativa de los algoritmos implementados.

El proyecto aborda el Sudoku como un problema de búsqueda en espacios de estados, permitiendo analizar cómo las diferentes estrategias de exploración se comportan frente a distintas configuraciones del problema y niveles de dificultad.

## Objetivos

- Representar el Sudoku como un problema de búsqueda en espacios de estados.
- Implementar algoritmos de búsqueda para encontrar soluciones válidas.
- Incorporar restricciones propias de las variantes clásica y diagonal.
- Generar instancias de Sudoku con diferentes niveles de dificultad.
- Visualizar el proceso de exploración realizado por los algoritmos.
- Evaluar y comparar el desempeño de las estrategias implementadas.

## Entornos

### Sudoku clásico

Tablero de 9 × 9 en el que cada fila, columna y subcuadrícula de 3 × 3 debe contener los dígitos del 1 al 9 sin repetición.

### Sudoku diagonal

Variante que incorpora las restricciones del Sudoku clásico, junto con la condición de que las dos diagonales principales también contengan los dígitos del 1 al 9 sin repetición.

## Algoritmos de búsqueda

### Backtracking

Implementación de una estrategia de búsqueda en profundidad que asigna valores a las casillas vacías, verifica las restricciones del entorno y retrocede cuando una asignación conduce a un estado inconsistente.

### Dijkstra

Implementación de búsqueda de costo uniforme mediante una estructura de prioridad, adaptada a la exploración de estados del Sudoku. Cada transición representa una asignación válida y tiene un costo unitario.

Dado que las transiciones poseen costos uniformes, el comportamiento de búsqueda corresponde a una exploración por niveles del espacio de estados, equivalente a BFS bajo estas condiciones.

## Funcionalidades

- Selección entre Sudoku clásico y Sudoku diagonal.
- Configuración de niveles de dificultad: fácil, medio y difícil.
- Generación de instancias aleatorias.
- Validación de tableros y restricciones.
- Resolución mediante Backtracking y Dijkstra.
- Visualización del proceso de búsqueda.
- Ejecución paso a paso y reproducción de la búsqueda.
- Comparación del desempeño de los algoritmos.
- Registro y análisis de métricas de evaluación.

## Evaluación

El desempeño de los algoritmos se analiza mediante indicadores que permiten estudiar su comportamiento durante el proceso de búsqueda, incluyendo:

- Tiempo de ejecución.
- Nodos explorados.
- Estados generados.
- Costo de búsqueda.

Las comparaciones se realizan sobre una misma instancia, con el propósito de mantener condiciones equivalentes de evaluación.

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python | Implementación del proyecto y algoritmos |
| Gradio | Desarrollo de la interfaz interactiva |
| NumPy | Manejo de estructuras de datos numéricas |
| Plotly | Visualización de resultados y métricas |
| Pytest | Pruebas y validación del sistema |
| Jupyter Notebook | Experimentación y documentación del entorno |

## Estructura del proyecto

```text
Sudoku_Search_Lab/
│
├── app.py
├── algorithms/
├── environment/
├── instances/
├── evaluation/
├── visualization/
├── interface/
├── data/
├── notebooks/
├── tests/
├── reference/
├── utils_busqueda.py
├├── requirements.txt
├── README.md
└── .gitignore
```

### Descripción de los módulos

| Módulo | Responsabilidad |
|---|---|
| `app.py` | Punto de entrada de la aplicación. |
| `algorithms/` | Implementación de los algoritmos de búsqueda. |
| `environment/` | Representación del Sudoku, estados y restricciones. |
| `instances/` | Generación y gestión de instancias. |
| `evaluation/` | Cálculo de métricas y comparación de resultados. |
| `visualization/` | Registro y visualización de los procesos de búsqueda. |
| `interface/` | Componentes de interfaz y conexión con la lógica. |
| `data/` | Almacenamiento de instancias y soluciones. |
| `notebooks/` | Notebook de experimentación y documentación. |
| `tests/` | Pruebas de funcionamiento y validación. |
| `reference/` | Material de referencia del proyecto. |
| `utils_busqueda.py` | Estructuras y utilidades auxiliares de búsqueda. |

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/sudoku-search-lab.git
```

### 2. Acceder al directorio

```bash
cd sudoku-search-lab
```

### 3. Crear un entorno virtual

**macOS / Linux**

```bash
python3 -m venv .venv
```

**Windows**

```bash
py -m venv .venv
```

### 4. Activar el entorno virtual

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar las dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Ejecutar la aplicación

```bash
python app.py
```

Una vez iniciada la aplicación, Gradio proporcionará una dirección local para acceder a la interfaz desde el navegador.

## Pruebas

Las pruebas del proyecto pueden ejecutarse mediante:

```bash
pytest -q
```

Este proceso permite verificar las restricciones de los entornos, la validez de las soluciones, el funcionamiento de los algoritmos y los componentes principales del sistema.

## Notebook

El proyecto incluye un notebook de Jupyter para la demostración del entorno, la creación de instancias, la descripción de sus métodos y atributos, y la ejecución de ejemplos de los algoritmos implementados. Puede utilizarse desde Jupyter Notebook o Google Colab.

## Contexto académico

Proyecto desarrollado para la asignatura **Representación y Solución Automática de Problemas**, orientado a la aplicación de conceptos de inteligencia artificial, representación de estados, restricciones y algoritmos de búsqueda.

El proyecto busca no solo obtener soluciones válidas, sino también analizar y comparar el comportamiento de las estrategias implementadas frente a diferentes instancias del problema.
