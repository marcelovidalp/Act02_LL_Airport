"""
Implementación en memoria de una lista doblemente enlazada
"""
from typing import TypeVar, Generic, Optional, List, Iterator
from app.models import Vuelo
from app.domain.in_memory_node import Node

T = TypeVar('T', bound=Vuelo)

class MemoryLinkedList(Generic[T]):
    """
    Lista doblemente enlazada implementada en memoria
    """
    def __init__(self):
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self._size = 0
    
    def size(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self.head is None
    
    def add_first(self, data: T) -> None:
        """Añade un elemento al inicio de la lista"""
        new_node = Node(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self._size += 1
    
    def add_last(self, data: T) -> None:
        """Añade un elemento al final de la lista"""
        new_node = Node(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self._size += 1
    
    def insert_at(self, position: int, data: T) -> None:
        """Inserta un elemento en una posición específica"""
        if position <= 0:
            self.add_first(data)
            return
        
        if position >= self._size:
            self.add_last(data)
            return
        
        # Encontrar la posición
        current = self.head
        for _ in range(position):
            if current:
                current = current.next
        
        if not current:
            self.add_last(data)
            return
        
        # Insertar antes del nodo actual
        new_node = Node(data)
        new_node.prev = current.prev
        new_node.next = current
        
        if current.prev:
            current.prev.next = new_node
        current.prev = new_node
        
        self._size += 1
    
    def remove_first(self) -> Optional[T]:
        """Elimina y devuelve el primer elemento"""
        if self.is_empty():
            return None
        
        removed_node = self.head
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
        
        self._size -= 1
        return removed_node.data if removed_node else None
    
    def remove_last(self) -> Optional[T]:
        """Elimina y devuelve el último elemento"""
        if self.is_empty():
            return None
        
        removed_node = self.tail
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None
        
        self._size -= 1
        return removed_node.data if removed_node else None
    
    def remove_at(self, position: int) -> Optional[T]:
        """Elimina y devuelve el elemento en una posición específica"""
        if position < 0 or self.is_empty():
            return None
        
        if position == 0:
            return self.remove_first()
        
        if position >= self._size - 1:
            return self.remove_last()
        
        # Encontrar el nodo
        current = self.head
        for _ in range(position):
            if current:
                current = current.next
        
        if not current:
            return None
        
        # Eliminar el nodo
        if current.prev:
            current.prev.next = current.next
        if current.next:
            current.next.prev = current.prev
        
        self._size -= 1
        return current.data
    
    def get_first(self) -> Optional[T]:
        """Devuelve el primer elemento sin eliminarlo"""
        return self.head.data if self.head else None
    
    def get_last(self) -> Optional[T]:
        """Devuelve el último elemento sin eliminarlo"""
        return self.tail.data if self.tail else None
    
    def get_at(self, position: int) -> Optional[T]:
        """Devuelve el elemento en una posición específica sin eliminarlo"""
        if position < 0 or self.is_empty() or position >= self._size:
            return None
        
        current = self.head
        for _ in range(position):
            if current:
                current = current.next
        
        return current.data if current else None
    
    def get_all(self) -> List[T]:
        """Retorna todos los elementos de la lista"""
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements
    
    def __iter__(self) -> Iterator[T]:
        """Permite iterar sobre los elementos de la lista"""
        current = self.head
        while current:
            yield current.data
            current = current.next
    
    def visualize(self) -> str:
        """
        Genera una representación visual de la lista enlazada.
        Útil para depuración y para visualizar la estructura de nodos.
        """
        if self.is_empty():
            return "[Lista vacía]"
        
        # Crear representación visual
        result = []
        result.append(f"Lista (tamaño: {self._size})")
        result.append("HEAD")
        
        current = self.head
        position = 0
        while current:
            # Crear representación del nodo con flechas para mostrar enlaces
            prev_arrow = "←" if current.prev else "×"
            next_arrow = "→" if current.next else "×"
            
            vuelo = current.data
            result.append(f"{position}: {prev_arrow} [{vuelo.codigo}: {vuelo.estado.name}] {next_arrow}")
            
            current = current.next
            position += 1
        
        result.append("TAIL")
        return "\n".join(result)
