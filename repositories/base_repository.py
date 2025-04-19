from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any

T = TypeVar('T')  # Tipo genérico para las entidades

class BaseRepository(ABC, Generic[T]):
    """Interfaz base para el patrón Repository"""
    
    @abstractmethod
    def get_by_id(self, id: Any) -> Optional[T]:
        """Obtiene una entidad por su ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Obtiene todas las entidades"""
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Agrega una nueva entidad"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Actualiza una entidad existente"""
        pass
    
    @abstractmethod
    def delete(self, id: Any) -> bool:
        """Elimina una entidad por su ID"""
        pass
