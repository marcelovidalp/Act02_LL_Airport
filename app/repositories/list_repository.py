from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import ListaVuelos



class ListRepository:
    """
    Repositorio para operaciones de base de datos relacionadas con listas de vuelos
    """
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ListaVuelos]:
        """Obtiene todas las listas de vuelos"""
        return self.db.query(ListaVuelos).offset(skip).limit(limit).all()
    
    def get_by_id(self, list_id: int) -> Optional[ListaVuelos]:
        """Obtiene una lista por su ID"""
        return self.db.query(ListaVuelos).filter(ListaVuelos.id == list_id).first()
    
    def create(self, lista: ListaVuelos) -> ListaVuelos:
        """Crea una nueva lista de vuelos"""
        self.db.add(lista)
        self.db.commit()
        self.db.refresh(lista)
        return lista
    
    def update(self, lista: ListaVuelos) -> ListaVuelos:
        """Actualiza una lista existente"""
        self.db.commit()
        self.db.refresh(lista)
        return lista
    
    def delete(self, lista: ListaVuelos) -> None:
        """Elimina una lista"""
        self.db.delete(lista)
        self.db.commit()