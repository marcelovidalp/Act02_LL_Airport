"""
Servicio para gestión de listas de vuelos
"""
from sqlalchemy.orm import Session
from app.models import ListaVuelos, Vuelo, EstadoVuelo
from app.services import linked_list

class ListService:
    """Servicio para gestionar listas de vuelos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_list(self, nombre: str = "Lista de vuelos"):
        """
        Crea una nueva lista de vuelos.
        """
        lista = ListaVuelos(nombre=nombre)
        self.db.add(lista)
        self.db.commit()
        self.db.refresh(lista)
        return lista
    
    def get_list(self, list_id: int):
        """
        Obtiene una lista de vuelos por su ID.
        """
        return self.db.query(ListaVuelos).filter(ListaVuelos.id == list_id).first()
    
    def get_all_lists(self, skip: int = 0, limit: int = 100):
        """
        Obtiene todas las listas de vuelos con paginación.
        """
        return self.db.query(ListaVuelos).offset(skip).limit(limit).all()
    
    def prioritize_flights(self, lista_id: int):
        """
        Prioriza los vuelos de una lista según su estado.
        """
        lista = self.get_list(lista_id)
        if not lista:
            return None
            
        result = linked_list.prioritize_flights(self.db, lista)
        self.db.commit()
        return result
    
    def get_flights_in_list(self, lista_id: int):
        """
        Obtiene todos los vuelos de una lista en su orden actual.
        """
        lista = self.get_list(lista_id)
        if not lista:
            return []
            
        return linked_list.get_all_flights(lista)
