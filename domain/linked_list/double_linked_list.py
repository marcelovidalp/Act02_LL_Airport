from .node import Node
from ...models.vuelo import PrioridadVuelo

class DoubleLinkedList:
    """Implementación de lista doblemente enlazada con centinelas (header y trailer)"""
    
    def __init__(self):
        """Inicializa una lista vacía con nodos centinela"""
        self.header = Node()    # Centinela de inicio
        self.trailer = Node()   # Centinela final
        
        # Conectar los centinelas
        self.header.next = self.trailer
        self.trailer.prev = self.header
        
        self._size = 0
        
    def __len__(self):
        """Devuelve la cantidad de elementos en la lista"""
        return self._size
    
    def is_empty(self):
        """Verifica si la lista está vacía"""
        return self._size == 0
        
    def _insert_between(self, vuelo, predecessor, successor):
        """Inserta un nuevo nodo entre dos nodos existentes"""
        nuevo_nodo = Node(vuelo)
        nuevo_nodo.prev = predecessor
        nuevo_nodo.next = successor
        predecessor.next = nuevo_nodo
        successor.prev = nuevo_nodo
        self._size += 1
        return nuevo_nodo
        
    def add_first(self, vuelo):
        """Agrega un vuelo al principio de la lista (después del header)"""
        return self._insert_between(vuelo, self.header, self.header.next)
        
    def add_last(self, vuelo):
        """Agrega un vuelo al final de la lista (antes del trailer)"""
        return self._insert_between(vuelo, self.trailer.prev, self.trailer)
        
    def insert_by_priority(self, vuelo):
        """
        Inserta un vuelo según su prioridad
        - Emergencia: al inicio
        - Regular: al final
        - Urgente: entre emergencias y regulares
        """
        if vuelo.prioridad == PrioridadVuelo.EMERGENCIA:
            return self.add_first(vuelo)
            
        if vuelo.prioridad == PrioridadVuelo.REGULAR:
            return self.add_last(vuelo)
            
        # Para vuelos urgentes o cualquier otra prioridad intermedia
        # Recorrer la lista desde el final hacia el principio
        current = self.trailer.prev
        # Avanzar hasta encontrar un vuelo con mayor o igual prioridad
        while current != self.header and current.vuelo.prioridad.value >= vuelo.prioridad.value:
            current = current.prev
            
        # Insertar después del vuelo encontrado
        return self._insert_between(vuelo, current, current.next)
    
    def remove(self, node):
        """Elimina el nodo especificado de la lista"""
        if self.is_empty() or node is self.header or node is self.trailer:
            return None
            
        # Desconectar el nodo
        predecessor = node.prev
        successor = node.next
        predecessor.next = successor
        successor.prev = predecessor
        
        # Ayudar al garbage collector
        node.prev = node.next = None
        self._size -= 1
        
        return node.vuelo
    
    def reorder_by_priority(self):
        """Reordena todos los vuelos según su prioridad actual"""
        if self._size <= 1:
            return  # Nada que reordenar
        
        # Crear una lista temporal con todos los vuelos
        vuelos = []
        current = self.header.next
        while current != self.trailer:
            vuelos.append(current.vuelo)
            current = current.next
        
        # Vaciar la lista original
        self.header.next = self.trailer
        self.trailer.prev = self.header
        self._size = 0
        
        # Volver a insertar los vuelos por prioridad
        for vuelo in vuelos:
            self.insert_by_priority(vuelo)
