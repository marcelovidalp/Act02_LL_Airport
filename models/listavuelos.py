from sqlalchemy.orm import Session
from models.vuelo import Vuelo
from models.nodo import Nodo


class ListaVuelos:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.size = 0

    def insertar_al_frente(self, vuelo: Vuelo):
        nuevo_nodo = Nodo(vuelo)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        self.size += 1

    def insertar_al_final(self, vuelo: Vuelo):
        nuevo_nodo = Nodo(vuelo)
        if not self.cola:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.size += 1

    def obtener_primero(self):
        return self.cabeza.vuelo if self.cabeza else None

    def obtener_ultimo(self):
        return self.cola.vuelo if self.cola else None

    def longitud(self):
        return self.size

    def insertar_en_posicion(self, vuelo: Vuelo, posicion: int):
        if posicion < 0 or posicion > self.size:
            raise IndexError("Posición fuera de rango")
        if posicion == 0:
            self.insertar_al_frente(vuelo)
        elif posicion == self.size:
            self.insertar_al_final(vuelo)
        else:
            nuevo_nodo = Nodo(vuelo)
            actual = self.cabeza
            for _ in range(posicion - 1):
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            nuevo_nodo.anterior = actual
            actual.siguiente.anterior = nuevo_nodo
            actual.siguiente = nuevo_nodo
            self.size += 1

    def extraer_de_posicion(self, posicion: int):
        if posicion < 0 or posicion >= self.size:
            raise IndexError("Posición fuera de rango")
        if posicion == 0:
            extraido = self.cabeza
            self.cabeza = self.cabeza.siguiente
            if self.cabeza:
                self.cabeza.anterior = None
            else:
                self.cola = None
        elif posicion == self.size - 1:
            extraido = self.cola
            self.cola = self.cola.anterior
            if self.cola:
                self.cola.siguiente = None
            else:
                self.cabeza = None
        else:
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
            extraido = actual
            actual.anterior.siguiente = actual.siguiente
            actual.siguiente.anterior = actual.anterior
        self.size -= 1
        return extraido.vuelo
