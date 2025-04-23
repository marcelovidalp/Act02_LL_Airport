"""
Endpoints de API relacionados con vuelos
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app import models, schemas
from app.db import get_db
from app.services import flight_service, linked_list

router = APIRouter()

@router.get("/vuelos/", response_model=List[schemas.VueloResponse])
def read_vuelos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene todos los vuelos de la base de datos con paginación.
    """
    vuelos = flight_service.get_all_flights(db, skip, limit)
    return vuelos

@router.post("/vuelos/", response_model=schemas.VueloResponse)
def create_vuelo(vuelo: schemas.VueloCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo vuelo en la base de datos.
    """
    return flight_service.create_flight(db, vuelo)

@router.get("/vuelos/{vuelo_id}", response_model=schemas.VueloResponse)
def read_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    """
    Obtiene detalles de un vuelo específico por ID.
    """
    vuelo = flight_service.get_flight(db, vuelo_id)
    if vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return vuelo

@router.patch("/vuelos/{vuelo_id}/estado", response_model=schemas.VueloResponse)
def update_estado(vuelo_id: int, estado: schemas.VueloUpdate, db: Session = Depends(get_db)):
    """
    Actualiza el estado de un vuelo.
    """
    try:
        nuevo_estado = models.EstadoVuelo[estado.estado.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Estado inválido: {estado.estado}")
    
    vuelo = flight_service.update_flight_status(db, vuelo_id, nuevo_estado)
    if vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return vuelo

@router.get("/vuelos/total", response_model=Dict[str, int])
def get_total_flights(lista_id: int = 1, db: Session = Depends(get_db)):
    """
    Obtiene el número total de vuelos en la lista.
    """
    lista = flight_service.get_list_by_id(db, lista_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
    
    total = linked_list.get_length(lista)
    return {"total": total}

@router.get("/vuelos/proximo", response_model=schemas.VueloResponse)
def get_next_flight(lista_id: int = 1, db: Session = Depends(get_db)):
    """
    Obtiene el próximo vuelo (primero en la lista).
    """
    lista = flight_service.get_list_by_id(db, lista_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
    
    vuelo = linked_list.get_first(lista)
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos en la lista")
    
    return vuelo

@router.post("/vuelos", response_model=schemas.VueloResponse)
def add_flight(vuelo: schemas.VueloCreate, position: str = "last", lista_id: int = 1, db: Session = Depends(get_db)):
    """
    Agrega un vuelo al inicio o al final de la lista.
    """
    # Crear vuelo
    db_vuelo = flight_service.create_flight(db, vuelo)
    
    # Obtener lista
    lista = flight_service.get_list_by_id(db, lista_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
    
    # Agregar a la lista
    if position.lower() == "first":
        linked_list.add_first(db, lista, db_vuelo)
    else:
        linked_list.add_last(db, lista, db_vuelo)
    
    db.commit()
    return db_vuelo

@router.get("/vuelos/ultimo", response_model=schemas.VueloResponse)
def get_last_flight(lista_id: int = 1, db: Session = Depends(get_db)):
    """
    Obtiene el último vuelo en la lista.
    """
    lista = flight_service.get_list_by_id(db, lista_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
    
    vuelo = linked_list.get_last(lista)
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos en la lista")
    
    return vuelo

@router.post("/vuelos/insertar", response_model=schemas.VueloResponse)
def insert_flight_at_position(vuelo: schemas.VueloCreate, position: int, lista_id: int = 1, db: Session = Depends(get_db)):
    """
    Inserta un vuelo en una posición específica.
    """
    # Crear vuelo
    db_vuelo = flight_service.create_flight(db, vuelo)
    
    # Obtener lista
    lista = flight_service.get_list_by_id(db, lista_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
    
    # Insertar en la posición
    linked_list.add_at_position(db, lista, db_vuelo, position)
    
    db.commit()
    return db_vuelo

@router.delete("/vuelos/extraer", response_model=schemas.VueloResponse)
def extract_flight_from_position(position: int, lista_id: int = 1, db: Session = Depends(get_db)):
    """
    Extrae un vuelo de una posición específica.
    """
    lista = flight_service.get_list_by_id(db, lista_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
    
    vuelo = linked_list.remove_at_position(db, lista, position)
    if not vuelo:
        raise HTTPException(status_code=404, detail="No se pudo extraer el vuelo de la posición especificada")
    
    db.commit()
    return vuelo

@router.get("/vuelos/lista", response_model=List[schemas.VueloResponse])
def get_all_flights_in_list(lista_id: int = 1, db: Session = Depends(get_db)):
    """
    Obtiene todos los vuelos recorriendo toda la lista enlazada.
    """
    lista = flight_service.get_list_by_id(db, lista_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
    
    vuelos = linked_list.get_all_flights(lista)
    return vuelos

@router.patch("/vuelos/reordenar", response_model=schemas.VueloResponse)
def reorder_flight(from_pos: int, to_pos: int, lista_id: int = 1, db: Session = Depends(get_db)):
    """
    Reordena un vuelo moviéndolo de una posición a otra.
    """
    lista = flight_service.get_list_by_id(db, lista_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
    
    vuelo = linked_list.reorder_flight(db, lista, from_pos, to_pos)
    if not vuelo:
        raise HTTPException(status_code=404, detail="No se pudo reordenar el vuelo")
    
    db.commit()
    return vuelo
