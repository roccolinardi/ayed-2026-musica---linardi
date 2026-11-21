import csv
from pathlib import Path


def cargar_versiones_csv(ruta: Path) -> dict[int, tuple[int, str]]:
    """
    Lee versiones.csv y devuelve un diccionario:
    { cancion_id: (version_de_id, tipo) }
    """
    versiones: dict[int, tuple[int, str]] = {}
    with open(ruta, mode="r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            cancion_id = int(fila["cancion_id"])
            version_de_id = int(fila["version_de_id"])
            tipo = fila["tipo"].strip()
            versiones[cancion_id] = (version_de_id, tipo)
    return versiones


def cadena_hasta_original(
    cancion_id: int,
    versiones: dict[int, tuple[int, str]],
    visitados: set[int] | None = None,
) -> list[tuple[int, str]]:
    """
    Recorre recursivamente desde una canción hasta su versión original.
    Devuelve una lista de tuplas (id, tipo), terminando en (id_original, "original").
    """
    if visitados is None:
        visitados = set()

    # Caso base: es la canción original (no deriva de otra) o ya fue visitada (evita ciclos)
    if cancion_id not in versiones or cancion_id in visitados:
        return [(cancion_id, "original")]

    # Caso recursivo: avanzamos hacia la canción de la cual deriva
    visitados.add(cancion_id)
    version_de_id, tipo = versiones[cancion_id]
    return [(cancion_id, tipo)] + cadena_hasta_original(version_de_id, versiones, visitados)


def versiones_derivadas(
    cancion_id: int,
    versiones: dict[int, tuple[int, str]],
    visitados: set[int] | None = None,
) -> list[tuple[int, str]]:
    """
    Busca recursivamente todas las versiones que derivan directa o indirectamente
    de una canción dada.
    """
    if visitados is None:
        visitados = set()

    visitados.add(cancion_id)
    resultado: list[tuple[int, str]] = []

    for cid, (vid, tipo) in versiones.items():
        if vid == cancion_id and cid not in visitados:
            resultado.append((cid, tipo))
            resultado.extend(versiones_derivadas(cid, versiones, visitados))

    return resultado