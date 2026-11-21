from pathlib import Path
from src.config import RUTA_CANCIONES_CSV, RUTA_VERSIONES_CSV, TEMA
from src.algoritmos.recursion import (
    cargar_versiones_csv,
    cadena_hasta_original,
    versiones_derivadas,
)
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion
from src.tads.lista_enlazada import ListaEnlazada
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.persistencia.texto import cargar_csv, guardar_csv
from src.persistencia.binario import (
    guardar_binario,
    cargar_binario,
    actualizar_registro,
)
from src.excepciones import (
    ItemNoEncontradoError,
    PilaVaciaError,
    ColaVaciaError,
)

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}

ENCABEZADOS_CSV = ["id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"]
CARPETA_DATA = Path(RUTA_CANCIONES_CSV).parent
RUTA_BINARIO = CARPETA_DATA / "catalogo.bin"
RUTA_EXPORT_CSV = CARPETA_DATA / "catalogo_export.csv"
RUTA_PLAYLIST_CSV = CARPETA_DATA / "playlist.csv"


def formatear_duracion(segundos: int) -> str:
    """Convierte segundos a formato mm:ss."""
    minutos = segundos // 60
    resto = segundos % 60
    return f"{minutos}:{resto:02d}"


def cargar_catalogo_csv() -> list[dict]:
    """Lee canciones.csv usando persistencia.texto y convierte tipos numéricos."""
    filas = cargar_csv(RUTA_CANCIONES_CSV)
    catalogo = []
    for fila in filas:
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
    return busqueda_lineal(catalogo, id_buscado, lambda c: c["id"])


def pedir_cancion_por_id(catalogo: list[dict]) -> dict | None:
    """Pide un ID por consola, valida que sea entero y devuelve la canción o None."""
    entrada = input("Ingresá el ID de la canción: ").strip()
    if not entrada.isdigit():
        print("Error: tenés que ingresar un número entero.")
        return None
    cancion = buscar_por_id(catalogo, int(entrada))
    if cancion is None:
        print(f"No se encontró ninguna canción con ID {entrada}.")
    return cancion


def mostrar_tabla_canciones(canciones: list[dict], titulo_tabla: str) -> None:
    """Muestra una lista de canciones en formato tabla."""
    print(f"\n--- {titulo_tabla} ({len(canciones)} canciones) ---")
    print(f"{'ID':>3} | {'Título':<32} | {'Artista':<24} | {'Año':>4} | {'Dur.':>5}")
    print("-" * 80)
    for c in canciones:
        dur = formatear_duracion(c["duracion_seg"])
        print(f"{c['id']:>3} | {c['titulo'][:32]:<32} | {c['artista'][:24]:<24} | {c['anio']:>4} | {dur:>5}")


def listar_catalogo(catalogo: list[dict]) -> None:
    """Muestra todas las canciones del catálogo en formato tabla."""
    mostrar_tabla_canciones(catalogo, f"Catálogo: {TEMAS[TEMA]}")


def ver_detalle(catalogo: list[dict]) -> None:
    """Pide un ID por consola y muestra todos los datos de esa canción."""
    c = pedir_cancion_por_id(catalogo)
    if c is None:
        return

    print("\n--- Detalle de la canción ---")
    print(f"ID:       {c['id']}")
    print(f"Título:   {c['titulo']}")
    print(f"Artista:  {c['artista']}")
    print(f"Álbum:    {c['album']}")
    print(f"Género:   {c['genero']}")
    print(f"Año:      {c['anio']}")
    print(f"Duración: {formatear_duracion(c['duracion_seg'])} ({c['duracion_seg']} seg)")


def menu_buscar(catalogo: list[dict]) -> None:
    """Opción 3 (E4): búsqueda lineal y búsqueda binaria."""
    print("\n--- Buscar canción ---")
    print("1. Búsqueda lineal por título exacto")
    print("2. Búsqueda binaria por ID (ordena primero por ID)")
    print("3. Búsqueda binaria por título exacto (ordena primero por título)")
    print("0. Volver")
    op = input("> ").strip()

    if op == "0":
        return
    elif op == "1":
        titulo = input("Ingresá el título exacto: ").strip().lower()
        res = busqueda_lineal(catalogo, titulo, lambda c: c["titulo"].lower())
    elif op == "2":
        entrada = input("Ingresá el ID: ").strip()
        if not entrada.isdigit():
            print("Error: tenés que ingresar un número entero.")
            return
        ordenado = ordenar_insercion(catalogo, lambda c: c["id"])
        res = busqueda_binaria(ordenado, int(entrada), lambda c: c["id"])
    elif op == "3":
        titulo = input("Ingresá el título exacto: ").strip().lower()
        ordenado = ordenar_insercion(catalogo, lambda c: c["titulo"].lower())
        res = busqueda_binaria(ordenado, titulo, lambda c: c["titulo"].lower())
    else:
        print("Opción inválida.")
        return

    if res is None:
        print("No se encontró ninguna coincidencia.")
    else:
        print(f"Encontrada: [{res['id']}] {res['titulo']} - {res['artista']} ({res['anio']}, {formatear_duracion(res['duracion_seg'])})")


def menu_ordenar(catalogo: list[dict]) -> None:
    """Opción 4 (E4): ordenamiento por selección e inserción."""
    print("\n--- Ordenar catálogo ---")
    print("Algoritmo:")
    print("1. Selección (ordenar_seleccion)")
    print("2. Inserción (ordenar_insercion)")
    alg = input("> ").strip()
    if alg not in {"1", "2"}:
        print("Opción inválida.")
        return

    print("\nCriterio:")
    print("1. Título (A-Z)")
    print("2. Artista (A-Z)")
    print("3. Año (ascendente)")
    print("4. Duración (ascendente)")
    crit = input("> ").strip()

    criterios = {
        "1": ("Título", lambda c: c["titulo"].lower()),
        "2": ("Artista", lambda c: c["artista"].lower()),
        "3": ("Año", lambda c: c["anio"]),
        "4": ("Duración", lambda c: c["duracion_seg"]),
    }
    if crit not in criterios:
        print("Opción inválida.")
        return

    nombre_crit, fn_clave = criterios[crit]
    if alg == "1":
        ordenado = ordenar_seleccion(catalogo, fn_clave)
        nombre_alg = "Selección"
    else:
        ordenado = ordenar_insercion(catalogo, fn_clave)
        nombre_alg = "Inserción"

    mostrar_tabla_canciones(ordenado, f"Catálogo ordenado por {nombre_crit} ({nombre_alg})")


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


def menu_playlist(catalogo: list[dict], playlist: ListaEnlazada) -> None:
    """Opción 6 (E3): gestión de playlist sobre ListaEnlazada."""
    while True:
        print(f"\n--- Playlist ({playlist.tamanio()} canciones) ---")
        print("1. Ver playlist")
        print("2. Agregar canción al final")
        print("3. Agregar canción ordenada por título")
        print("4. Quitar canción por ID")
        print("0. Volver")
        op = input("> ").strip()

        if op == "0":
            break
        elif op == "1":
            if playlist.esta_vacia():
                print("La playlist está vacía.")
            else:
                for i, c in enumerate(playlist, start=1):
                    print(f"  {i}. [{c['id']}] {c['titulo']} - {c['artista']} ({formatear_duracion(c['duracion_seg'])})")
        elif op == "2":
            c = pedir_cancion_por_id(catalogo)
            if c is not None:
                playlist.insertar_al_final(c)
                print(f"Agregada al final: {c['titulo']}")
        elif op == "3":
            c = pedir_cancion_por_id(catalogo)
            if c is not None:
                playlist.insertar_ordenado(c, clave=lambda x: x["titulo"].lower())
                print(f"Agregada ordenada por título: {c['titulo']}")
        elif op == "4":
            c = pedir_cancion_por_id(catalogo)
            if c is not None:
                try:
                    playlist.eliminar(c)
                    print(f"Eliminada de la playlist: {c['titulo']}")
                except ItemNoEncontradoError:
                    print("Esa canción no está en la playlist.")
        else:
            print("Opción inválida.")


def menu_historial(catalogo: list[dict], historial: Pila) -> None:
    """Opción 7 (E3): historial de reproducción sobre Pila (LIFO)."""
    while True:
        print(f"\n--- Historial de reproducción - Pila ({historial.tamanio()} canciones) ---")
        print("1. Ver historial completo (más reciente primero)")
        print("2. Ver última canción escuchada (tope)")
        print("3. Registrar reproducción manual (apilar)")
        print("4. Quitar última reproducción (desapilar)")
        print("0. Volver")
        op = input("> ").strip()

        if op == "0":
            break
        elif op == "1":
            if historial.esta_vacia():
                print("El historial está vacío.")
            else:
                for i, c in enumerate(historial, start=1):
                    print(f"  {i}. [{c['id']}] {c['titulo']} - {c['artista']}")
        elif op == "2":
            try:
                c = historial.ver_tope()
                print(f"Última escuchada: [{c['id']}] {c['titulo']} - {c['artista']}")
            except PilaVaciaError:
                print("El historial está vacío.")
        elif op == "3":
            c = pedir_cancion_por_id(catalogo)
            if c is not None:
                historial.apilar(c)
                print(f"Registrada en historial: {c['titulo']}")
        elif op == "4":
            try:
                c = historial.desapilar()
                print(f"Se quitó del historial: [{c['id']}] {c['titulo']}")
            except PilaVaciaError:
                print("El historial está vacío.")
        else:
            print("Opción inválida.")


def menu_cola(catalogo: list[dict], cola: Cola, historial: Pila) -> None:
    """Opción 8 (E3): cola de reproducción sobre Cola (FIFO)."""
    while True:
        print(f"\n--- Cola de reproducción ({cola.tamanio()} pendientes) ---")
        print("1. Ver cola")
        print("2. Agregar canción a la cola (encolar)")
        print("3. Ver próxima canción (frente)")
        print("4. Reproducir siguiente (desencolar y pasar al historial)")
        print("0. Volver")
        op = input("> ").strip()

        if op == "0":
            break
        elif op == "1":
            if cola.esta_vacia():
                print("La cola de reproducción está vacía.")
            else:
                for i, c in enumerate(cola, start=1):
                    print(f"  {i}. [{c['id']}] {c['titulo']} - {c['artista']}")
        elif op == "2":
            c = pedir_cancion_por_id(catalogo)
            if c is not None:
                cola.encolar(c)
                print(f"Encolada: {c['titulo']}")
        elif op == "3":
            try:
                c = cola.ver_frente()
                print(f"Próxima a reproducir: [{c['id']}] {c['titulo']} - {c['artista']}")
            except ColaVaciaError:
                print("La cola de reproducción está vacía.")
        elif op == "4":
            try:
                c = cola.desencolar()
                historial.apilar(c)
                print(f"Reproduciendo ahora: [{c['id']}] {c['titulo']} - {c['artista']} (guardada en historial)")
            except ColaVaciaError:
                print("La cola de reproducción está vacía.")
        else:
            print("Opción inválida.")


def menu_persistencia(catalogo: list[dict], playlist: ListaEnlazada) -> list[dict]:
    """Opción 9 (E5): persistencia en CSV y binario con acceso directo."""
    while True:
        print("\n--- Guardar / cargar archivos (E5) ---")
        print(f"1. Guardar catálogo en binario ({RUTA_BINARIO.name})")
        print(f"2. Cargar catálogo desde binario ({RUTA_BINARIO.name})")
        print("3. Actualizar registro por posición en binario (acceso directo)")
        print(f"4. Exportar catálogo a CSV ({RUTA_EXPORT_CSV.name})")
        print(f"5. Exportar playlist actual a CSV ({RUTA_PLAYLIST_CSV.name})")
        print("0. Volver")
        op = input("> ").strip()

        if op == "0":
            break
        elif op == "1":
            guardar_binario(RUTA_BINARIO, catalogo)
            print(f"Catálogo guardado en {RUTA_BINARIO} ({len(catalogo)} registros).")
        elif op == "2":
            try:
                catalogo = cargar_binario(RUTA_BINARIO)
                print(f"Catálogo cargado desde {RUTA_BINARIO} ({len(catalogo)} registros).")
            except (FileNotFoundError, ValueError) as err:
                print(f"Error al cargar binario: {err}")
        elif op == "3":
            if not RUTA_BINARIO.exists():
                print("Primero guardá el catálogo en binario (opción 1).")
                continue
            pos_str = input(f"Ingresá la posición 0-based (0 a {len(catalogo) - 1}): ").strip()
            if not pos_str.isdigit():
                print("Error: ingresá un número entero no negativo.")
                continue
            pos = int(pos_str)
            if pos < 0 or pos >= len(catalogo):
                print("Posición fuera de rango.")
                continue
            actual = dict(catalogo[pos])
            print(f"Registro actual en [{pos}]: [{actual['id']}] {actual['titulo']} - {actual['artista']} ({actual['anio']})")
            nuevo_titulo = input("Nuevo título (Enter para dejar igual): ").strip()
            if nuevo_titulo:
                actual["titulo"] = nuevo_titulo
            try:
                actualizar_registro(RUTA_BINARIO, pos, actual)
                catalogo[pos] = actual
                print(f"Registro en posición {pos} actualizado directamente en {RUTA_BINARIO}.")
            except (FileNotFoundError, ValueError, IndexError) as err:
                print(f"Error al actualizar registro: {err}")
        elif op == "4":
            guardar_csv(RUTA_EXPORT_CSV, catalogo, ENCABEZADOS_CSV)
            print(f"Catálogo exportado a {RUTA_EXPORT_CSV}.")
        elif op == "5":
            if playlist.esta_vacia():
                print("La playlist está vacía, no hay nada para exportar.")
            else:
                guardar_csv(RUTA_PLAYLIST_CSV, list(playlist), ENCABEZADOS_CSV)
                print(f"Playlist exportada a {RUTA_PLAYLIST_CSV} ({playlist.tamanio()} canciones).")
        else:
            print("Opción inválida.")
    return catalogo


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
    playlist = ListaEnlazada()
    historial = Pila()
    cola = Cola()

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
        elif opcion == "3":
            menu_buscar(catalogo)
        elif opcion == "4":
            menu_ordenar(catalogo)
        elif opcion == "5":
            ver_cadena_versiones(catalogo, versiones)
        elif opcion == "6":
            menu_playlist(catalogo, playlist)
        elif opcion == "7":
            menu_historial(catalogo, historial)
        elif opcion == "8":
            menu_cola(catalogo, cola, historial)
        elif opcion == "9":
            catalogo = menu_persistencia(catalogo, playlist)
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()