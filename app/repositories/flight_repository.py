"""
Repositorio para operaciones con vuelos en la base de datos
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Vuelo, ListaVuelos, EstadoVuelo

class FlightRepository:
    """
    Repositorio para operaciones de base de datos relacionadas con vuelos
    """
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Vuelo]:
        """Obtiene todos los vuelos con paginación"""
        return self.db.query(Vuelo).order_by(Vuelo.id).offset(skip).limit(limit).all()
    
    def get_by_id(self, flight_id: int) -> Optional[Vuelo]:
        """Obtiene un vuelo por su ID"""
        return self.db.query(Vuelo).filter(Vuelo.id == flight_id).first()
    
    def get_by_code(self, code: str) -> Optional[Vuelo]:
        """Obtiene un vuelo por su código"""
        return self.db.query(Vuelo).filter(Vuelo.codigo == code).first()
    
    def create(self, flight: Vuelo) -> Vuelo:
        """Crea un nuevo vuelo"""
        self.db.add(flight)
        self.db.commit()
        self.db.refresh(flight)
        return flight
    
    def update(self, flight: Vuelo) -> Vuelo:
        """Actualiza un vuelo existente"""
        self.db.commit()
        self.db.refresh(flight)
        return flight
    
    def delete(self, flight: Vuelo) -> None:
        """Elimina un vuelo"""
        self.db.delete(flight)
        self.db.commit()
    
    def get_flights_by_list_id(self, list_id: int) -> List[Vuelo]:
        """Obtiene todos los vuelos asociados a una lista"""
        return self.db.query(Vuelo).filter(Vuelo.lista_vuelos_id == list_id).all()
    
    def get_flights_by_status(self, status: EstadoVuelo) -> List[Vuelo]:
        """Obtiene todos los vuelos con un estado específico"""
        return self.db.query(Vuelo).filter(Vuelo.estado == status).all()
