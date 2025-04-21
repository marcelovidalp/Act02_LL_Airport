from models import vuelo, listavuelos, nodo, Base

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
        self._trailer._prev = self._header
        self._size = 0

    def __len__(self):
        return self._size   
    
    def is_empty(self):
        return self._size == 0
    
    def add_first(self, data):
        

