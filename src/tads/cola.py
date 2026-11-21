from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColaVaciaError


class Cola:
    """TAD cola implementado sobre ListaEnlazada."""

    def __init__(self):
        self._lista = ListaEnlazada()

    def encolar(self, dato):
        self._lista.insertar_al_final(dato)

    def desencolar(self):
        if self.esta_vacia():
            raise ColaVaciaError("La cola está vacía.")
        return self._lista.eliminar_al_inicio()

    def ver_frente(self):
        if self.esta_vacia():
            raise ColaVaciaError("La cola está vacía.")
        return self._lista.ver_primero()

    def esta_vacia(self):
        return self._lista.esta_vacia()

    def tamanio(self):
        return self._lista.tamanio()

    def __iter__(self):
        return iter(self._lista)