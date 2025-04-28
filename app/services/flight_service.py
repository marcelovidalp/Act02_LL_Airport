"""
Lógica de negocio relacionada con vuelos
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app import schemas
from app.models import Vuelo, EstadoVuelo, ListaVuelos
from app.repositories.flight_repository import FlightRepository
from app.repositories.list_repository import ListRepository
from app.services.linked_list_manager import LinkedListManager

class FlightService:
    """
    Servicio para gestión de vuelos
    """
    def __init__(self, db: Session):
        self.db = db
        self.flight_repo = FlightRepository(db)
        self.list_repo = ListRepository(db)
    
    def get_flight(self, flight_id: int) -> Optional[Vuelo]:
        """
        Obtiene un vuelo por su ID.
        """
        return self.flight_repo.get_by_id(flight_id)
    
    def get_flight_by_code(self, code: str) -> Optional[Vuelo]:
        """
        Obtiene un vuelo por su código.
        """
        return self.flight_repo.get_by_code(code)
    
    def create_flight(self, flight_data: schemas.VueloCreate) -> Vuelo:
        """
        Crea un nuevo vuelo en la base de datos.
        """
        try:
            # Crear el vuelo en la base de datos
            vuelo = Vuelo(**flight_data.dict())
            return self.flight_repo.create(vuelo)
        except Exception as e:
            print(f"Error al crear vuelo: {e}")
            raise
    
    def add_flight_to_list(self, vuelo: Vuelo, lista_id: int = 1) -> Vuelo:
        """
        Añade un vuelo existente a una lista según su estado.
        """
        try:
            # Verificar que la lista existe
            if not self.list_repo.get_by_id(lista_id):
                raise ValueError(f"Lista con ID {lista_id} no encontrada")
            
            # Determinar la posición según el estado y añadir vuelo
            if vuelo.estado == EstadoVuelo.EMERGENCIA:
                # Emergencia: al principio
                LinkedListManager.add_first(self.db, lista_id, vuelo)
            else:
                # Cualquier otro estado: al final
                LinkedListManager.add_last(self.db, lista_id, vuelo)
            
            return vuelo
        except Exception as e:
            print(f"Error al añadir vuelo a la lista: {e}")
            raise
    
    def update_flight_status(self, flight_id: int, new_status: EstadoVuelo, reorder: bool = True) -> Optional[Vuelo]:
        """
        Actualiza el estado de un vuelo y lo reordena en la lista si es necesario.
        """
        try:
            # Obtener el vuelo
            vuelo = self.get_flight(flight_id)
            if not vuelo:
                return None
            
            # Guardar el estado anterior
            old_status = vuelo.estado
            
            # Actualizar estado
            vuelo.estado = new_status
            self.flight_repo.update(vuelo)
            
            # Si hay que reordenar y el estado ha cambiado
            if reorder and old_status != new_status and vuelo.lista_vuelos_id:
                # Limpiar la caché para que se reconstruya con la nueva prioridad
                LinkedListManager.clear_cache(vuelo.lista_vuelos_id)
                
                # Obtener nueva instancia con priorización actualizada
                LinkedListManager.prioritize(self.db, vuelo.lista_vuelos_id)
            
            return vuelo
        except Exception as e:
            print(f"Error al actualizar estado: {e}")
            raise
    
    def get_all_flights(self, skip: int = 0, limit: int = 100) -> List[Vuelo]:
        """
        Obtiene todos los vuelos de la base de datos.
        """
        return self.flight_repo.get_all(skip, limit)
    
    def get_list_by_id(self, list_id: int) -> Optional[ListaVuelos]:
        """
        Obtiene una lista de vuelos por su ID.
        """
        return self.list_repo.get_by_id(list_id)
    
    def get_all_flights_for_list(self, list_id: int) -> List[Vuelo]:
        """
        Obtiene todos los vuelos asociados a una lista desde la base de datos.
        """
        return self.flight_repo.get_flights_by_list_id(list_id)
    
    def get_all_flights_in_order(self, list_id: int) -> List[Vuelo]:
        """
        Obtiene todos los vuelos de una lista en su orden priorizado.
        """
        return LinkedListManager.get_all(self.db, list_id)

# Funciones de nivel de módulo para mantener compatibilidad con el código existente
def get_flight(db: Session, flight_id: int) -> Optional[Vuelo]:
    service = FlightService(db)
    return service.get_flight(flight_id)

def get_flight_by_code(db: Session, code: str) -> Optional[Vuelo]:
    service = FlightService(db)
    return service.get_flight_by_code(code)

def create_flight(db: Session, flight_data: schemas.VueloCreate) -> Vuelo:
    service = FlightService(db)
    return service.create_flight(flight_data)

def add_flight_to_list(db: Session, vuelo: Vuelo, lista_id: int = 1) -> Vuelo:
    service = FlightService(db)
    return service.add_flight_to_list(vuelo, lista_id)

def update_flight_status(db: Session, flight_id: int, new_status: EstadoVuelo, reorder: bool = True) -> Optional[Vuelo]:
    service = FlightService(db)
    return service.update_flight_status(flight_id, new_status, reorder)

def get_all_flights(db: Session, skip: int = 0, limit: int = 100) -> List[Vuelo]:
    service = FlightService(db)
    return service.get_all_flights(skip, limit)

def get_list_by_id(db: Session, list_id: int) -> Optional[ListaVuelos]:
    service = FlightService(db)
    return service.get_list_by_id(list_id)

def get_all_flights_for_list(db: Session, list_id: int) -> List[Vuelo]:
    service = FlightService(db)
    return service.get_all_flights_for_list(list_id)
