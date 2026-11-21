# Declaración de uso de IA

Actualizar **en cada entrega**. Si no usaron IA, dejar una fila que lo diga. No declarar cuando sí se usó anula la entrega.

Fecha de esta versión del archivo: 21/11/2026

| Entrega | Fecha | Herramienta (ChatGPT, Cursor, Copilot, otra) | Para qué (diseño, código, debug, docs) | Qué pegaron o generaron | Qué reescribieron / revisaron a mano | Integrante |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | 21/11/2026 | Gemini | diseño, código, docs | Consultas sobre lectura de archivos con `csv.DictReader` y estructura base del menú CLI. | Se integró al esqueleto de la cátedra, se configuraron las rutas en `src/config.py`, se ajustó el formato de salida y se probó localmente con el dataset. | Rocco Mateo Linardi |
| E2 | 21/11/2026 | Gemini | diseño, código, docs | Consultas sobre recursión con prevención de ciclos (`visitados`) y lectura de `versiones.csv`. | Se creó `src/algoritmos/recursion.py`, se integró la opción 5 en `src/main.py`, se probó con el dataset real y se documentó en `INFORME.md`. | Rocco Mateo Linardi |
| E3 | 21/11/2026 | Gemini | diseño, código, docs | Consultas sobre implementación de `ListaEnlazada` con punteros `_cabeza` y `_cola` para operaciones en `Pila` y `Cola`, y manejo de excepciones propias. | Se implementaron `lista_enlazada.py`, `pila.py` y `cola.py`, se integraron las opciones 6, 7 y 8 en `src/main.py`, se probaron los flujos y se completó la sección 4 de `INFORME.md`. | Rocco Mateo Linardi 
| E4 | 21/11/2026 | Gemini | diseño, código, docs | Consulta sobre implementación de búsqueda lineal/binaria, ordenamiento por selección/inserción sin usar `sorted` y análisis de complejidad temporal y espacial. | Se implementaron `src/algoritmos/busqueda.py` y `src/algoritmos/ordenamiento.py`, se integraron las opciones 3 y 4 en `src/main.py`, se probaron con el catálogo real y se completó la sección 5 de `INFORME.md`. | Rocco Mateo Linardi |
| E5 | 21/11/2026 | Gemini | diseño, código, docs | Consultas sobre persistencia en CSV (`DictReader`/`DictWriter`), empaquetado binario de longitud fija con `struct` y acceso directo mediante `seek`. | Se implementaron `src/persistencia/texto.py` y `src/persistencia/binario.py`, se integró la opción 9 en `src/main.py`, se probaron guardado, carga y exportación con el catálogo real y se completó la sección 6 de `INFORME.md`. | Rocco Mateo Linardi |
| E6 |  |  |  |  |  |  |

Compromiso: cualquiera del grupo puede explicar cualquier archivo del tag.
