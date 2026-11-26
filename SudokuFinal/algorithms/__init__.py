"""Algoritmos de búsqueda para Sudoku."""
from .backtracking import solve_backtracking
from .dijkstra import solve_dijkstra

__all__ = ["solve_backtracking", "solve_dijkstra"]
