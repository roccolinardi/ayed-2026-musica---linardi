from src.tads.nodo import Nodo
from src.excepciones import ItemNoEncontradoError, ColeccionVaciaError


class ListaEnlazada:
    """TAD lista enlazada simple. No usar list de Python por debajo."""

    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._tamanio = 0

    def esta_vacia(self):
        return self._tamanio == 0

    def tamanio(self):
        return self._tamanio

    def ver_primero(self):
        if self.esta_vacia():
            raise ColeccionVaciaError("La lista está vacía.")
        return self._cabeza.dato

    def insertar_al_inicio(self, dato):
        nuevo = Nodo(dato, self._cabeza)
        self._cabeza = nuevo
        if self._cola is None:
            self._cola = nuevo
        self._tamanio += 1

    def insertar_al_final(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self._cabeza = nuevo
            self._cola = nuevo
        else:
            self._cola.siguiente = nuevo
            self._cola = nuevo
        self._tamanio += 1

    def insertar_ordenado(self, dato, clave=lambda x: x):
        if self.esta_vacia() or clave(dato) <= clave(self._cabeza.dato):
            self.insertar_al_inicio(dato)
            return

        actual = self._cabeza
        while actual.siguiente is not None and clave(actual.siguiente.dato) < clave(dato):
            actual = actual.siguiente

        nuevo = Nodo(dato, actual.siguiente)
        actual.siguiente = nuevo
        if nuevo.siguiente is None:
            self._cola = nuevo
        self._tamanio += 1

    def eliminar_al_inicio(self):
        if self.esta_vacia():
            raise ColeccionVaciaError("La lista está vacía.")
        dato = self._cabeza.dato
        self._cabeza = self._cabeza.siguiente
        if self._cabeza is None:
            self._cola = None
        self._tamanio -= 1
        return dato

    def eliminar(self, dato):
        if self.esta_vacia():
            raise ItemNoEncontradoError(f"No se encontró el elemento: {dato}")

        if self._cabeza.dato == dato:
            self.eliminar_al_inicio()
            return

        actual = self._cabeza
        while actual.siguiente is not None and actual.siguiente.dato != dato:
            actual = actual.siguiente

        if actual.siguiente is None:
            raise ItemNoEncontradoError(f"No se encontró el elemento: {dato}")

        eliminado = actual.siguiente
        actual.siguiente = eliminado.siguiente
        if actual.siguiente is None:
            self._cola = actual
        self._tamanio -= 1

    def buscar(self, dato):
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                return actual.dato
            actual = actual.siguiente
        return None

    def __iter__(self):
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente