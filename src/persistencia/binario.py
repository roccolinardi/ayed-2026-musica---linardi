"""Registros de longitud fija con struct.

Layout definitivo (tema Biblioteca musical):

Header (<4s1sI = 9 bytes):
    magia     4s  b'AYED'
    tema      1s  b'M'
    cantidad  I   unsigned int (cantidad de registros)

Registro de canción (<I64s48s48s24sHH = 192 bytes):
    id            I    unsigned int (4 bytes)
    titulo        64s  UTF-8 con padding nulo (64 bytes)
    artista       48s  UTF-8 con padding nulo (48 bytes)
    album         48s  UTF-8 con padding nulo (48 bytes)
    genero        24s  UTF-8 con padding nulo (24 bytes)
    anio          H    unsigned short (2 bytes)
    duracion_seg  H    unsigned short (2 bytes)
"""

import struct
from pathlib import Path

MAGIA = b"AYED"
TEMA_MUSICA = b"M"

FMT_HEADER = "<4s1sI"
TAM_HEADER = struct.calcsize(FMT_HEADER)  # 9 bytes

FMT_REGISTRO = "<I64s48s48s24sHH"
TAM_REGISTRO = struct.calcsize(FMT_REGISTRO)  # 192 bytes


def _codificar_str(texto: str, ancho: int) -> bytes:
    """Codifica un string a UTF-8 truncando a `ancho` bytes como máximo."""
    return str(texto).encode("utf-8")[:ancho]


def _decodificar_str(crudo: bytes) -> str:
    """Decodifica bytes con padding nulo a string limpio."""
    return crudo.rstrip(b"\x00").decode("utf-8", errors="replace").strip()


def _empaquetar_item(item: dict) -> bytes:
    return struct.pack(
        FMT_REGISTRO,
        int(item["id"]),
        _codificar_str(item["titulo"], 64),
        _codificar_str(item["artista"], 48),
        _codificar_str(item["album"], 48),
        _codificar_str(item["genero"], 24),
        int(item["anio"]),
        int(item["duracion_seg"]),
    )


def _desempaquetar_item(bloque: bytes) -> dict:
    cid, titulo, artista, album, genero, anio, duracion = struct.unpack(FMT_REGISTRO, bloque)
    return {
        "id": cid,
        "titulo": _decodificar_str(titulo),
        "artista": _decodificar_str(artista),
        "album": _decodificar_str(album),
        "genero": _decodificar_str(genero),
        "anio": anio,
        "duracion_seg": duracion,
    }


def guardar_binario(ruta, items):
    """Guarda la colección completa en un archivo binario de registros fijos."""
    lista_items = list(items)
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, mode="wb") as archivo:
        header = struct.pack(FMT_HEADER, MAGIA, TEMA_MUSICA, len(lista_items))
        archivo.write(header)
        for item in lista_items:
            archivo.write(_empaquetar_item(item))


def cargar_binario(ruta):
    """Lee el header, valida magia/tema y carga todos los registros."""
    items = []
    with open(ruta, mode="rb") as archivo:
        header_bytes = archivo.read(TAM_HEADER)
        if len(header_bytes) < TAM_HEADER:
            raise ValueError("Archivo binario inválido o incompleto (header).")
        magia, tema, cantidad = struct.unpack(FMT_HEADER, header_bytes)
        if magia != MAGIA or tema != TEMA_MUSICA:
            raise ValueError(f"Header incompatible: magia={magia!r}, tema={tema!r}.")

        for _ in range(cantidad):
            bloque = archivo.read(TAM_REGISTRO)
            if len(bloque) < TAM_REGISTRO:
                raise ValueError("Archivo binario truncado al leer registros.")
            items.append(_desempaquetar_item(bloque))
    return items


def actualizar_registro(ruta, posicion, item):
    """Pisa un registro por posición (acceso directo). posicion es 0-based."""
    with open(ruta, mode="r+b") as archivo:
        header_bytes = archivo.read(TAM_HEADER)
        if len(header_bytes) < TAM_HEADER:
            raise ValueError("Archivo binario inválido o incompleto (header).")
        magia, tema, cantidad = struct.unpack(FMT_HEADER, header_bytes)
        if magia != MAGIA or tema != TEMA_MUSICA:
            raise ValueError(f"Header incompatible: magia={magia!r}, tema={tema!r}.")
        if posicion < 0 or posicion >= cantidad:
            raise IndexError(f"Posición {posicion} fuera de rango (0..{cantidad - 1}).")

        offset = TAM_HEADER + posicion * TAM_REGISTRO
        archivo.seek(offset)
        archivo.write(_empaquetar_item(item))