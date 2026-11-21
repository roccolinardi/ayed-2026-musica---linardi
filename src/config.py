"""Elegir un tema y no cambiarlo entre entregas."""

from pathlib import Path

# "pokedex" | "recetario" | "musica"
TEMA = "musica"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

RUTA_CANCIONES_CSV = DATA_DIR / "canciones.csv"
RUTA_VERSIONES_CSV = DATA_DIR / "versiones.csv"
RUTA_CANCIONES_BIN = DATA_DIR / "canciones.bin"