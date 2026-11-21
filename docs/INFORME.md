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

- Función:
- Caso base:
- Caso recursivo:
- Traza de un ejemplo real del dataset:

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada |  |  |
| Pila |  |  |
| Cola |  |  |

Dónde se usa cada uno en el dominio.

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
