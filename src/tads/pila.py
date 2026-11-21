from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import PilaVaciaError


class Pila:
    """TAD pila implementado sobre ListaEnlazada."""

    def __init__(self):
        self._lista = ListaEnlazada()

    def apilar(self, dato):
        self._lista.insertar_al_inicio(dato)

    def desapilar(self):
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía.")
        return self._lista.eliminar_al_inicio()

    def ver_tope(self):
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía.")
        return self._lista.ver_primero()

    def esta_vacia(self):
        return self._lista.esta_vacia()

    def tamanio(self):
        return self._lista.tamanio()

    def __iter__(self):
        return iter(self._lista)