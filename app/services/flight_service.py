"""
Lógica de negocio relacionada con vuelos
"""
from sqlalchemy.orm import Session
from app import models, schemas

def get_flight(db: Session, flight_id: int):
    """
    Obtiene un vuelo por su ID.
    """
    return db.query(models.Vuelo).filter(models.Vuelo.id == flight_id).first()

def get_flight_by_code(db: Session, code: str):
    """
    Obtiene un vuelo por su código.
    """
    return db.query(models.Vuelo).filter(models.Vuelo.codigo == code).first()

def create_flight(db: Session, flight: schemas.VueloCreate):
    """
    Crea un nuevo vuelo en la base de datos.
    """
    db_vuelo = models.Vuelo(**flight.dict())
    db.add(db_vuelo)
    db.commit()
    db.refresh(db_vuelo)
    return db_vuelo

def update_flight_status(db: Session, flight_id: int, new_status: models.EstadoVuelo):
    """
    Actualiza el estado de un vuelo.
    """
    db_vuelo = get_flight(db, flight_id)
    if not db_vuelo:
        return None
    db_vuelo.estado = new_status
    db.commit()
    db.refresh(db_vuelo)
    return db_vuelo

def get_all_flights(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene todos los vuelos con paginación.
    """
    return db.query(models.Vuelo).offset(skip).limit(limit).all()

def get_list_by_id(db: Session, list_id: int):
    """
    Obtiene una lista de vuelos por su ID.
    """
    return db.query(models.ListaVuelos).filter(models.ListaVuelos.id == list_id).first()
