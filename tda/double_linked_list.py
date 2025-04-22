from models import base, vuelo, listavuelos, nodo

class DoubleLinkedList:
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

    def __len__(self):
        return self._size   
    
    def is_empty(self):
        return self._size == 0
    
    def add_first(self, data):
        new_node = self.Node(data)
        new_node._next = self._header._next
        new_node._prev = self._header
        self._header._next._prev = new_node
        self._header._next = new_node
        self._size += 1
        return new_node
    
    def add_last(self, data):
        new_node = self.Node(data)
        new_node._prev = self._tail._prev
        new_node._next = self._tail
        self._tail._prev._next = new_node
        self._tail._prev = new_node
        self._size += 1
        return new_node
    
    def insert_between(self, succesor, predecessor, data):
        new_node = self.Node(data)
        new_node._prev = predecessor
        new_node._next = succesor
        predecessor._next = new_node
        succesor._prev = new_node
        self._size += 1
        return new_node

