from typing import List, Optional
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.vuelo import Vuelo

class VueloRepository(BaseRepository[Vuelo]):
    """Implementación del repositorio para la entidad Vuelo"""
    
    def __init__(self, session: Session):
        self.session = session
        
    def get_by_id(self, id: int) -> Optional[Vuelo]:
        return self.session.query(Vuelo).filter(Vuelo.id == id).first()
    
    def get_all(self) -> List[Vuelo]:
        return self.session.query(Vuelo).all()
    
    def add(self, entity: Vuelo) -> Vuelo:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity
    
    def update(self, entity: Vuelo) -> Vuelo:
        self.session.merge(entity)
        self.session.commit()
        return entity
    
    def delete(self, id: int) -> bool:
        vuelo = self.get_by_id(id)
        if vuelo:
            self.session.delete(vuelo)
            self.session.commit()
            return True
        return False
    
    # Métodos específicos para vuelos
    def get_by_numero_vuelo(self, numero_vuelo: str) -> Optional[Vuelo]:
        return self.session.query(Vuelo).filter(Vuelo.numero_vuelo == numero_vuelo).first()
        
    def get_vuelos_por_estado(self, estado: str) -> List[Vuelo]:
        return self.session.query(Vuelo).filter(Vuelo.estado == estado).all()
