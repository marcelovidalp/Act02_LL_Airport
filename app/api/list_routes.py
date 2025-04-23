"""
Endpoints para gestión de listas de vuelos
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app import schemas
from app.db import get_db
from app.services import flight_service, linked_list

router = APIRouter()

@router.post("/listas/{lista_id}/vuelos/{vuelo_id}/inicio")
def add_vuelo_inicio(lista_id: int, vuelo_id: int, db: Session = Depends(get_db)):
    """
    Añade un vuelo existente al principio de una lista.
    """
    lista = flight_service.get_list_by_id(db, lista_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    vuelo = flight_service.get_flight(db, vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    
    nodo = linked_list.add_first(db, lista, vuelo)
    db.commit()
    return {"mensaje": f"Vuelo {vuelo.codigo} añadido al inicio de la lista"}

@router.post("/listas/{lista_id}/priorizar")
def priorizar_vuelos(lista_id: int, db: Session = Depends(get_db)):
    """
    Prioriza los vuelos en la lista según su estado.
    """
    lista = flight_service.get_list_by_id(db, lista_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    resultado = linked_list.prioritize_flights(db, lista)
    db.commit()
    return resultado
