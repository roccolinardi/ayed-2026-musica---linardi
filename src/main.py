import csv
from src.config import RUTA_CANCIONES_CSV, RUTA_VERSIONES_CSV, TEMA
from src.algoritmos.recursion import (
    cargar_versiones_csv,
    cadena_hasta_original,
    versiones_derivadas,
)

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}


def formatear_duracion(segundos: int) -> str:
    """Convierte segundos a formato mm:ss."""
    minutos = segundos // 60
    resto = segundos % 60
    return f"{minutos}:{resto:02d}"


def cargar_catalogo_csv() -> list[dict]:
    """Lee canciones.csv y devuelve una lista de diccionarios."""
    catalogo = []
    with open(RUTA_CANCIONES_CSV, mode="r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            catalogo.append({
                "id": int(fila["id"]),
                "titulo": fila["titulo"].strip(),
                "artista": fila["artista"].strip(),
                "album": fila["album"].strip(),
                "genero": fila["genero"].strip(),
                "anio": int(fila["anio"]),
                "duracion_seg": int(fila["duracion_seg"]),
            })
    return catalogo


def buscar_por_id(catalogo: list[dict], id_buscado: int) -> dict | None:
    """Devuelve el diccionario de la canción con ese ID, o None si no existe."""
    for c in catalogo:
        if c["id"] == id_buscado:
            return c
    return None


def listar_catalogo(catalogo: list[dict]) -> None:
    """Muestra todas las canciones del catálogo en formato tabla."""
    print(f"\n--- Catálogo: {TEMAS[TEMA]} ({len(catalogo)} canciones) ---")
    print(f"{'ID':>3} | {'Título':<32} | {'Artista':<24} | {'Año':>4} | {'Dur.':>5}")
    print("-" * 80)
    for c in catalogo:
        dur = formatear_duracion(c["duracion_seg"])
        print(f"{c['id']:>3} | {c['titulo'][:32]:<32} | {c['artista'][:24]:<24} | {c['anio']:>4} | {dur:>5}")


def ver_detalle(catalogo: list[dict]) -> None:
    """Pide un ID por consola y muestra todos los datos de esa canción."""
    entrada = input("Ingresá el ID de la canción: ").strip()
    if not entrada.isdigit():
        print("Error: tenés que ingresar un número entero.")
        return

    c = buscar_por_id(catalogo, int(entrada))
    if c is None:
        print(f"No se encontró ninguna canción con ID {entrada}.")
        return

    print("\n--- Detalle de la canción ---")
    print(f"ID:       {c['id']}")
    print(f"Título:   {c['titulo']}")
    print(f"Artista:  {c['artista']}")
    print(f"Álbum:    {c['album']}")
    print(f"Género:   {c['genero']}")
    print(f"Año:      {c['anio']}")
    print(f"Duración: {formatear_duracion(c['duracion_seg'])} ({c['duracion_seg']} seg)")


def ver_cadena_versiones(catalogo: list[dict], versiones: dict[int, tuple[int, str]]) -> None:
    """Opción 5 (E2): muestra la cadena recursiva hacia la original y versiones derivadas."""
    entrada = input("Ingresá el ID de la canción (ej: 62, 13, 1): ").strip()
    if not entrada.isdigit():
        print("Error: tenés que ingresar un número entero.")
        return

    id_buscado = int(entrada)
    cancion = buscar_por_id(catalogo, id_buscado)
    if cancion is None:
        print(f"No se encontró ninguna canción con ID {id_buscado}.")
        return

    print(f"\n--- Cadena de versiones (recursiva) para [{id_buscado}] {cancion['titulo']} ---")
    cadena = cadena_hasta_original(id_buscado, versiones)
    for idx, (cid, tipo) in enumerate(cadena):
        c = buscar_por_id(catalogo, cid)
        nombre = f"{c['titulo']} - {c['artista']}" if c else f"ID {cid}"
        prefijo = "  └─► " if idx > 0 else "  ● "
        print(f"{prefijo}[{cid}] {nombre} ({tipo})")

    derivadas = versiones_derivadas(id_buscado, versiones)
    if derivadas:
        print("\nVersiones derivadas de esta canción:")
        for cid, tipo in derivadas:
            c = buscar_por_id(catalogo, cid)
            nombre = f"{c['titulo']} - {c['artista']}" if c else f"ID {cid}"
            print(f"  - [{cid}] {nombre} ({tipo})")
    else:
        print("\nNo tiene versiones derivadas registradas en versiones.csv.")


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")


def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print()
    print(f"=== {nombre} – AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva (versiones)")
    print("6. Colección principal (playlist)")
    print("7. Historial (pila)")
    print("8. Cola de reproducción")
    print("9. Guardar / cargar archivos")
    print("0. Salir")


def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return

    catalogo = cargar_catalogo_csv()
    versiones = cargar_versiones_csv(RUTA_VERSIONES_CSV)

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            listar_catalogo(catalogo)
        elif opcion == "2":
            ver_detalle(catalogo)
        elif opcion == "5":
            ver_cadena_versiones(catalogo, versiones)
        elif opcion in {"3", "4", "6", "7", "8", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()