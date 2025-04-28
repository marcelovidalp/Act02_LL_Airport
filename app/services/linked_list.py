"""
Operaciones de lista doblemente enlazada para la gestión de vuelos
Adaptador para el LinkedListManager
"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.models import Vuelo, ListaVuelos
from app.services.linked_list_manager import LinkedListManager

# Funciones adaptadoras para mantener compatibilidad con el código existente

def get_length(lista: ListaVuelos) -> int:
    """
    Obtiene la longitud de la lista.
    """
    from app.db import SessionLocal
    db = SessionLocal()
    try:
        return LinkedListManager.size(db, lista.id)
    finally:
        db.close()

def get_first(lista: ListaVuelos) -> Optional[Vuelo]:
    """
    Obtiene el primer vuelo sin eliminarlo.
    """
    from app.db import SessionLocal
    db = SessionLocal()
    try:
        return LinkedListManager.get_first(db, lista.id)
    finally:
        db.close()

def get_last(lista: ListaVuelos) -> Optional[Vuelo]:
    """
    Obtiene el último vuelo sin eliminarlo.
    """
    from app.db import SessionLocal
    db = SessionLocal()
    try:
        return LinkedListManager.get_last(db, lista.id)
    finally:
        db.close()

def get_all_flights(lista: ListaVuelos) -> List[Vuelo]:
    """
    Recorre toda la lista y devuelve todos los vuelos.
    """
    from app.db import SessionLocal
    db = SessionLocal()
    try:
        return LinkedListManager.get_all(db, lista.id)
    finally:
        db.close()

def add_first(db: Session, lista: ListaVuelos, vuelo: Vuelo) -> Vuelo:
    """
    Añade un vuelo al principio de la lista.
    """
    return LinkedListManager.add_first(db, lista.id, vuelo)

def add_last(db: Session, lista: ListaVuelos, vuelo: Vuelo) -> Vuelo:
    """
    Añade un vuelo al final de la lista.
    """
    return LinkedListManager.add_last(db, lista.id, vuelo)

def add_at_position(db: Session, lista: ListaVuelos, vuelo: Vuelo, position: int) -> Vuelo:
    """
    Inserta un vuelo en una posición específica.
    """
    return LinkedListManager.insert_at(db, lista.id, vuelo, position)

def remove_at_position(db: Session, lista: ListaVuelos, position: int) -> Optional[Vuelo]:
    """
    Elimina un vuelo de una posición específica.
    """
    return LinkedListManager.remove_at(db, lista.id, position)

def prioritize_flights(db: Session, lista: ListaVuelos) -> Dict:
    """
    Reorganiza la lista según la prioridad del estado de los vuelos.
    """
    result = LinkedListManager.prioritize(db, lista.id)
    return {
        "mensaje": f"Lista priorizada: {result['emergencias']} emergencias, " +
                   f"{result['embarques']} embarques, " +
                   f"{result['programados']} programados, " +
                   f"{result['otros']} otros"
    }

def rebuild_list_from_db(db: Session, lista: ListaVuelos, vuelos: List[Vuelo]) -> None:
    """
    Reconstruye la lista a partir de los vuelos de la base de datos.
    """
    # Forzar recarga desde la BD
    LinkedListManager.clear_cache(lista.id)
    return LinkedListManager.get_list_instance(db, lista.id)

def reorder_flight(db: Session, lista: ListaVuelos, from_pos: int, to_pos: int) -> Optional[Vuelo]:
    """
    Reordena un vuelo de una posición a otra.
    """
    # Obtener el vuelo a mover
    vuelo = LinkedListManager.get_at(db, lista.id, from_pos)
    if not vuelo:
        return None
    
    # Eliminarlo de la posición actual
    LinkedListManager.remove_at(db, lista.id, from_pos)
    
    # Ajustar la posición destino si es necesaria
    if to_pos > from_pos:
        to_pos -= 1
    
    # Insertar en la nueva posición
    LinkedListManager.insert_at(db, lista.id, vuelo, to_pos)
    
    return vuelo
