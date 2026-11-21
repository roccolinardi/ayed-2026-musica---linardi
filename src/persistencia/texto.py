import csv
from pathlib import Path


def cargar_csv(ruta):
    """Carga secuencial. Devuelve una lista de dicts."""
    filas = []
    with open(ruta, mode="r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            filas.append(dict(fila))
    return filas


def guardar_csv(ruta, filas, encabezados):
    """Guarda una secuencia de dicts en un archivo CSV."""
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, mode="w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=encabezados)
        escritor.writeheader()
        for fila in filas:
            escritor.writerow({campo: fila[campo] for campo in encabezados})