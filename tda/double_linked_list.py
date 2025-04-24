from typing import TypeVar, Generic, Optional, Iterator
from tda.abstract_list import AbstractList

T = TypeVar('T')

class DoubleLinkedList(AbstractList[T]):
    """Implementación concreta de lista doblemente enlazada que implementa AbstractList"""
    
    class Node:
        __slots__ = '_data', '_next', '_prev'
        def __init__(self, data):
            self._data = data
            self._next = None
            self._prev = None

    def __init__(self):
        self._header = self.Node(None)  # Dummy header
        self._tail = self.Node(None)    # Dummy tail
        self._header._next = self._tail
        self._tail._prev = self._header
        self._size = 0

    def size(self) -> int:
        """Retorna el tamaño de la lista"""
        return self._size   
    
    def is_empty(self) -> bool:
        """Verifica si la lista está vacía"""
        return self._size == 0
    
    def add_first(self, data: T):
        """Añade un elemento al inicio de la lista"""
        new_node = self.Node(data)
        new_node._next = self._header._next
        new_node._prev = self._header
        self._header._next._prev = new_node
        self._header._next = new_node
        self._size += 1
        return new_node
    
    def add_last(self, data: T):
        """Añade un elemento al final de la lista"""
        new_node = self.Node(data)
        new_node._prev = self._tail._prev
        new_node._next = self._tail
        self._tail._prev._next = new_node
        self._tail._prev = new_node
        self._size += 1
        return new_node
    
    def _insert_between(self, predecessor, successor, data: T):
        """Método auxiliar para insertar entre dos nodos"""
        new_node = self.Node(data)
        new_node._prev = predecessor
        new_node._next = successor
        predecessor._next = new_node
        successor._prev = new_node
        self._size += 1
        return new_node
    
    def insert_at(self, position: int, data: T):
        """Inserta un elemento en una posición específica"""
        if position < 0 or position > self._size:
            raise IndexError("Posición fuera de rango")
            
        if position == 0:
            return self.add_first(data)
        elif position == self._size:
            return self.add_last(data)
        else:
            # Encontrar el nodo en la posición correcta
            current = self._header
            for _ in range(position):
                current = current._next
            # Insertar entre el actual y el anterior
            return self._insert_between(current._prev, current, data)
    
    def _delete_node(self, node):
        """Método auxiliar para eliminar un nodo específico"""
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        data = node._data
        # Ayudar al garbage collector
        node._prev = node._next = node._data = None
        return data
    
    def remove_first(self) -> Optional[T]:
        """Elimina y devuelve el primer elemento"""
        if self.is_empty():
            return None
        return self._delete_node(self._header._next)
    
    def remove_last(self) -> Optional[T]:
        """Elimina y devuelve el último elemento"""
        if self.is_empty():
            return None
        return self._delete_node(self._tail._prev)
    
    def remove_at(self, position: int) -> Optional[T]:
        """Elimina y devuelve el elemento en una posición específica"""
        if position < 0 or position >= self._size:
            raise IndexError("Posición fuera de rango")
            
        if position == 0:
            return self.remove_first()
        elif position == self._size - 1:
            return self.remove_last()
        else:
            current = self._header._next
            for _ in range(position):
                current = current._next
            return self._delete_node(current)
    
    def get_first(self) -> Optional[T]:
        """Devuelve el primer elemento sin eliminarlo"""
        if self.is_empty():
            return None
        return self._header._next._data
    
    def get_last(self) -> Optional[T]:
        """Devuelve el último elemento sin eliminarlo"""
        if self.is_empty():
            return None
        return self._tail._prev._data
    
    def get_at(self, position: int) -> Optional[T]:
        """Devuelve el elemento en una posición específica sin eliminarlo"""
        if position < 0 or position >= self._size:
            raise IndexError("Posición fuera de rango")
            
        current = self._header._next
        for _ in range(position):
            current = current._next
        return current._data
    
    def __iter__(self) -> Iterator[T]:
        """Permite iterar sobre los elementos de la lista"""
        current = self._header._next
        while current != self._tail:
            yield current._data
            current = current._next
