from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Iterator

T = TypeVar('T')  # Tipo genérico para los elementos de la lista

class AbstractList(Generic[T], ABC):
    """Interfaz abstracta para implementaciones de TDA Lista"""
    
    @abstractmethod
    def size(self) -> int:
        """Retorna el tamaño de la lista"""
        pass
        
    @abstractmethod
    def is_empty(self) -> bool:
        """Verifica si la lista está vacía"""
        pass
        
    @abstractmethod
    def add_first(self, data: T):
        """Añade un elemento al inicio de la lista"""
        pass
        
    @abstractmethod
    def add_last(self, data: T):
        """Añade un elemento al final de la lista"""
        pass
        
    @abstractmethod
    def insert_at(self, position: int, data: T):
        """Inserta un elemento en una posición específica"""
        pass
        
    @abstractmethod
    def remove_first(self) -> Optional[T]:
        """Elimina y retorna el primer elemento"""
        pass
        
    @abstractmethod
    def remove_last(self) -> Optional[T]:
        """Elimina y retorna el último elemento"""
        pass
        
    @abstractmethod
    def remove_at(self, position: int) -> Optional[T]:
        """Elimina y retorna el elemento en una posición específica"""
        pass
        
    @abstractmethod
    def get_first(self) -> Optional[T]:
        """Retorna el primer elemento sin eliminarlo"""
        pass
        
    @abstractmethod
    def get_last(self) -> Optional[T]:
        """Retorna el último elemento sin eliminarlo"""
        pass
        
    @abstractmethod
    def get_at(self, position: int) -> Optional[T]:
        """Retorna el elemento en una posición específica sin eliminarlo"""
        pass
        
    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        """Permite iterar sobre los elementos de la lista"""
        pass
