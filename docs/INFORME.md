## 1. Grupo y tema

- Tema: Biblioteca musical
- Por qué lo eligieron (5-8 líneas):
  Elegimos el tema Biblioteca musical porque es un dominio cotidiano y fácil de modelar con las estructuras de datos de la materia.
  Permite representar un catálogo de canciones reales con atributos variados (texto, números enteros y duraciones en segundos) y relaciones entre versiones originales y covers o remixes.
  Además, las estructuras pedidas en el TP encajan de forma natural con el funcionamiento de cualquier reproductor de música:
  una lista enlazada para armar playlists, una pila para el historial de canciones reproducidas y una cola para la lista de reproducción ("a continuación").
  Esto hace que el programa por consola sea intuitivo de probar y defender.

## 2. Modelo

Un ítem del catálogo representa una **canción** cargada desde `data/canciones.csv`, compuesta por siete campos: `id`, `titulo`, `artista`, `album`, `genero`, `anio` y `duracion_seg`.

* **Tipos inmutables:** `int` (`id`, `anio`, `duracion_seg`), `str` (`titulo`, `artista`, `album`, `genero`) y `pathlib.Path` para las rutas de archivos. Evitan modificaciones accidentales de los valores individuales.
* **Tipos mutables:** en esta primera entrega cada canción se almacena en un `dict` y el catálogo completo en una `list` dinámica (en entregas posteriores se migrará a clases de dominio y TADs propios).
* **Relación entre estructuras (arquitectura objetivo):** el **catálogo** contiene todas las canciones disponibles; la **colección principal (playlist)** referencia canciones seleccionadas por el usuario; la **pila** registra el historial de reproducción (última escuchada arriba); y la **cola** ordena las próximas canciones a reproducir (FIFO).

```text
Catálogo (canciones.csv)
  ├──► Playlist (ListaEnlazada)  [E3]
  ├──► Historial (Pila - LIFO)   [E3]
  └──► Cola de reproducción (FIFO) [E3]
```

## 3. Recursión (E2)

- Función: `cadena_hasta_original(cancion_id, versiones, visitados)` en `src/algoritmos/recursion.py` (complementada con `versiones_derivadas` para recorrer en sentido inverso).
- Caso base: cuando `cancion_id` no figura como clave en `versiones` (significa que es la canción original) o ya está en el conjunto `visitados` (corta posibles ciclos). Devuelve `[(cancion_id, "original")]`.
- Caso recursivo: agrega `cancion_id` a `visitados`, obtiene `(version_de_id, tipo)` desde `versiones[cancion_id]` y devuelve `[(cancion_id, tipo)] + cadena_hasta_original(version_de_id, versiones, visitados)`.
- Traza de un ejemplo real del dataset (`id = 62`, *De Musica Ligera (Unplugged)*):
  1. `cadena_hasta_original(62, versiones, set())` → `62` está en `versiones` (`(1, "live")`). Agrega `62` a `visitados` y llama a `cadena_hasta_original(1, versiones, {62})`.
  2. `cadena_hasta_original(1, versiones, {62})` → `1` no está en `versiones` (caso base). Devuelve `[(1, "original")]`.
  3. Retorno: `[(62, "live")] + [(1, "original")]` = `[(62, "live"), (1, "original")]`.

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada | `esta_vacia`, `tamanio`, `ver_primero`, `insertar_al_inicio`, `insertar_al_final`, `insertar_ordenado`, `eliminar_al_inicio`, `eliminar`, `buscar`, `__iter__` | `_tamanio` coincide siempre con la cantidad de nodos alcanzables desde `_cabeza`; si `_tamanio == 0`, `_cabeza` y `_cola` son `None`; si no, `_cola.siguiente` es `None`. No usa `list` de Python por debajo. |
| Pila | `apilar`, `desapilar`, `ver_tope`, `esta_vacia`, `tamanio`, `__iter__` | Política LIFO (último en entrar, primero en salir) implementada sobre `ListaEnlazada` operando siempre en la cabeza en $O(1)$. Lanza `PilaVaciaError` al desapilar o ver tope estando vacía. |
| Cola | `encolar`, `desencolar`, `ver_frente`, `esta_vacia`, `tamanio`, `__iter__` | Política FIFO (primero en entrar, primero en salir) implementada sobre `ListaEnlazada` encolando al final y desencolando al inicio en $O(1)$. Lanza `ColaVaciaError` al desencolar o ver frente estando vacía. |

- **Uso en el dominio:** `ListaEnlazada` gestiona la **playlist** (permite agregar al final, insertar ordenado por título y eliminar por ID); `Pila` lleva el **historial de reproducción** (la última canción escuchada queda en el tope); `Cola` administra la **cola de reproducción** (se reproducen en el orden en que fueron encoladas y pasan automáticamente al historial).

## 5. Complejidad (E4)

| Operación | Tiempo | Espacio | Por qué |
| --- | --- | --- | --- |
|  |  |  |  |

Mediciones (`time.perf_counter`):

| Operación | n | segundos |
| --- | --- | --- |
|  |  |  |

## 6. Persistencia (E5)

- Layout del registro binario (campos, `struct`, anchos):
- Header:
- Cómo se actualiza un registro por posición:

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
|  |  |  |
