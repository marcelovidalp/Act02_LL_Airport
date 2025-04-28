"""
Implementación en memoria de los nodos para la lista doblemente enlazada
"""
from typing import TypeVar, Generic, Optional
from app.models import Vuelo

T = TypeVar('T', bound=Vuelo)

class Node(Generic[T]):
    """
    Nodo para lista doblemente enlazada implementado en memoria
    """
    def __init__(self, data: T):
        self.data = data
        self.next: Optional[Node[T]] = None
        self.prev: Optional[Node[T]] = None
    
    def __str__(self) -> str:
        """Representación legible del nodo para visualización"""
        vuelo = self.data
        return f"Nodo({vuelo.codigo}:{vuelo.estado.name})"
    
    def __repr__(self) -> str:
        """Representación técnica del nodo para depuración"""
        vuelo = self.data
        prev_code = self.prev.data.codigo if self.prev else "None"
        next_code = self.next.data.codigo if self.next else "None"
        return f"Nodo(vuelo={vuelo.codigo}, prev={prev_code}, next={next_code})"
