"""Catálogo reproducible de instancias incluidas en el proyecto."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "instances.json"


def load_catalog() -> dict:
    with CATALOG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_puzzle(variant: str, difficulty: str) -> list[list[int]]:
    catalog = load_catalog()
    try:
        return [list(row) for row in catalog[variant][difficulty]]
    except KeyError as exc:
        raise ValueError(f"No existe instancia para {variant}/{difficulty}.") from exc


def clue_count(board) -> int:
    return sum(value != 0 for row in board for value in row)
