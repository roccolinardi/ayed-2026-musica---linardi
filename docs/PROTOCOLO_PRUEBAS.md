# Protocolo de pruebas

Pruebas **manuales**. Cada fila es un caso. Ejecutar sobre el tag que entregan.

Leyenda de resultado: `pasa` / `no pasa` / `no corrido`.

Mínimos: 8 casos escritos en E2; ejecutados en E3; 15 de regresión en E6 (pila, cola, archivos, recursión, búsquedas).

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | E1 | Arrancar el programa y listar catálogo | `canciones.csv` (67 canciones) | lista no vacía, sin traceback | pasa | Muestra las 67 canciones en tabla formateada |
| P02 | E1 | Elegir un ítem inexistente | `id = -1` o `999` | mensaje claro, el menú sigue | pasa | Valida entero positivo e informa que no existe |
| P03 | E2 | Operación recursiva sobre un ítem con cadena | `id = 62` (`De Musica Ligera (Unplugged)`) | imprime la cadena completa | pasa | Muestra `62 (live) -> 1 (original)` |
| P04 | E2 | Operación recursiva sobre un ítem sin derivados | `id = 42` (`505`) | solo el ítem (caso base) | pasa | Devuelve únicamente `(42, "original")` sin derivadas |
| P05 | E3 | Agregar y quitar en colección principal (`ListaEnlazada`) | `id = 62`, quitar ID inexistente en playlist | inserta ordenado y lanza `ItemNoEncontradoError` al quitar inexistente | pasa | La playlist no tiene tope fijo; captura excepción propia sin caer |
| P06 | E3 | Desapilar / ver tope en historial vacío | pila vacía | excepción propia (`PilaVaciaError`), menú sigue | pasa | Informa "El historial está vacío." y vuelve al menú |
| P07 | E3 | Desencolar / ver frente en cola vacía | cola vacía | excepción propia (`ColaVaciaError`), menú sigue | pasa | Informa "La cola de reproducción está vacía." y sigue |
| P08 | E3 | Listar colección con el iterador | 2+ canciones en playlist | el orden coincide con las inserciones / orden elegido | pasa | Recorre `ListaEnlazada` mediante `__iter__` |
| P09 | E4 | Búsqueda lineal de un nombre que existe | `De Musica Ligera (Unplugged)` | lo encuentra | pasa | Devuelve `[62] De Musica Ligera (Unplugged) - Soda Stereo` |
| P10 | E4 | Búsqueda lineal de un nombre que no existe | `Cancion Inexistente` | no encontrado, sin traceback | pasa | Muestra "No se encontró ninguna coincidencia." |
| P11 | E4 | Búsqueda binaria con catálogo desordenado | `id = 62` / título exacto | reordena antes de buscar; no da un falso hit | pasa | Ordena previamente con `ordenar_insercion` y encuentra el ítem |
| P12 | E4 | Ordenar por un criterio y después por otro | Título (Selección) y luego Año/Duración (Inserción) | el orden cambia | pasa | Devuelve nueva lista ordenada sin mutar el catálogo original |
| P13 | E5 | Exportar CSV, salir, volver a entrar | `data/catalogo_export.csv` | los datos siguen | pasa | Archivo generado con encabezados y los 67 registros |
| P14 | E5 | Guardar binario y modificar un registro por posición | `data/catalogo.bin`, posición `0` | al recargar, ese campo cambió | pasa | `actualizar_registro` usa `seek` en `O(1)` y persiste el cambio |
| P15 | E5 | Abrir un binario truncado o con magia mala | archivo con bytes inválidos | excepción de archivo inválido (`ValueError`) | pasa | `cargar_binario` valida magia `b'AYED'` y tema `b'M'` sin romper el menú |