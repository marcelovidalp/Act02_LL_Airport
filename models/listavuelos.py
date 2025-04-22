from sqlalchemy.orm import Session
from models.vuelo import Vuelo
from models.nodo import Nodo


class ListaVuelos:
    def __init__(self, session: Session = None):
        self.cabeza = None
        self.cola = None
        self.size = 0
        self.session = session

    def insertar_al_frente(self, vuelo: Vuelo):
        """Añade al inicio (emergencias)"""
        nuevo_nodo = Nodo(vuelo_id=vuelo.id)
        if self.session:
            self.session.add(nuevo_nodo)
            self.session.flush()
            
        if not self.cabeza:
            self.cabeza = self.cola = nuevo_nodo.id
        else:
            # Actualizar referencias
            if self.session:
                nodo_cabeza = self.session.query(Nodo).get(self.cabeza)
                nodo_cabeza.anterior = nuevo_nodo.id
                nuevo_nodo.siguiente = self.cabeza
                self.cabeza = nuevo_nodo.id
                self.session.flush()
        self.size += 1
        return nuevo_nodo

    def insertar_al_final(self, vuelo: Vuelo):
        """Añade al final (vuelos normales)"""
        nuevo_nodo = Nodo(vuelo_id=vuelo.id)
        if self.session:
            self.session.add(nuevo_nodo)
            self.session.flush() 
            
        if not self.cola:
            self.cabeza = self.cola = nuevo_nodo.id
        else:
            # Actualizar referencias
            if self.session:
                nodo_cola = self.session.query(Nodo).get(self.cola)
                nodo_cola.siguiente = nuevo_nodo.id
                nuevo_nodo.anterior = self.cola
                self.cola = nuevo_nodo.id
                self.session.flush()
        self.size += 1
        return nuevo_nodo

    def obtener_primero(self):
        if not self.cabeza:
            return None
        if self.session:
            nodo = self.session.query(Nodo).get(self.cabeza)
            return self.session.query(Vuelo).get(nodo.vuelo_id) if nodo else None
        return None

    def obtener_ultimo(self):
        if not self.cola:
            return None
        if self.session:
            nodo = self.session.query(Nodo).get(self.cola)
            return self.session.query(Vuelo).get(nodo.vuelo_id) if nodo else None
        return None

    def longitud(self):
        return self.size+1

    def insertar_en_posicion(self, vuelo: Vuelo, posicion: int):
        if posicion < 0 or posicion > self.size:
            raise IndexError("Posición fuera de rango")
        
        if posicion == 0:
            return self.insertar_al_frente(vuelo)
        elif posicion == self.size:
            return self.insertar_al_final(vuelo)
        else:
            nuevo_nodo = Nodo(vuelo_id=vuelo.id)
            if self.session:
                self.session.add(nuevo_nodo)
                self.session.flush()
                
                # Encontrar el nodo en la posición deseada
                actual_id = self.cabeza
                for _ in range(posicion - 1):
                    actual = self.session.query(Nodo).get(actual_id)
                    actual_id = actual.siguiente
                
                actual = self.session.query(Nodo).get(actual_id)
                siguiente = self.session.query(Nodo).get(actual.siguiente)
                
                # Actualizar referencias
                nuevo_nodo.siguiente = actual.siguiente
                nuevo_nodo.anterior = actual_id
                actual.siguiente = nuevo_nodo.id
                siguiente.anterior = nuevo_nodo.id
                
                self.session.flush()
                self.size += 1
                return nuevo_nodo
        return None

    def extraer_de_posicion(self, posicion: int):
        if posicion < 0 or posicion >= self.size:
            raise IndexError("Posición fuera de rango")
        
        if self.session:
            if posicion == 0:
                # Extraer el primer nodo
                nodo = self.session.query(Nodo).get(self.cabeza)
                vuelo = self.session.query(Vuelo).get(nodo.vuelo_id)
                
                if nodo.siguiente:
                    self.cabeza = nodo.siguiente
                    siguiente = self.session.query(Nodo).get(nodo.siguiente)
                    siguiente.anterior = None
                else:
                    self.cabeza = self.cola = None
                
                self.session.delete(nodo)
                self.size -= 1
                return vuelo
                
            elif posicion == self.size - 1:
                # Extraer el último nodo
                nodo = self.session.query(Nodo).get(self.cola)
                vuelo = self.session.query(Vuelo).get(nodo.vuelo_id)
                
                if nodo.anterior:
                    self.cola = nodo.anterior
                    anterior = self.session.query(Nodo).get(nodo.anterior)
                    anterior.siguiente = None
                else:
                    self.cabeza = self.cola = None
                
                self.session.delete(nodo)
                self.size -= 1
                return vuelo
                
            else:
                # Extraer un nodo intermedio
                actual_id = self.cabeza
                for _ in range(posicion):
                    actual = self.session.query(Nodo).get(actual_id)
                    actual_id = actual.siguiente
                
                nodo = self.session.query(Nodo).get(actual_id)
                vuelo = self.session.query(Vuelo).get(nodo.vuelo_id)
                
                anterior = self.session.query(Nodo).get(nodo.anterior)
                siguiente = self.session.query(Nodo).get(nodo.siguiente)
                
                anterior.siguiente = nodo.siguiente
                siguiente.anterior = nodo.anterior
                
                self.session.delete(nodo)
                self.size -= 1
                return vuelo
        
        return None
