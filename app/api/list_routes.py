"""
Endpoints para gestión de listas de vuelos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app import schemas
from app.db import get_db
from app.services import flight_service, linked_list

router = APIRouter()

@router.get("/listas", response_model=List[schemas.ListaVuelosResponse])
def get_all_lists(db: Session = Depends(get_db)):
    """
    OBTIENE TODAS LAS LISTAS DE VUELOS.
    """
    from app.models import ListaVuelos
    listas = db.query(ListaVuelos).all()
    return listas

@router.post("/listas", response_model=schemas.ListaVuelosResponse)
def create_list(nombre: str = "Lista de vuelos", db: Session = Depends(get_db)):
    """
    CREA UNA NUEVA LISTA DE VUELOS.
    """
    from app.models import ListaVuelos
    lista = ListaVuelos(nombre=nombre)
    db.add(lista)
    db.commit()
    db.refresh(lista)
    return lista

@router.post("/listas/{lista_id}/vuelos/{vuelo_id}/inicio", status_code=status.HTTP_200_OK)
def add_vuelo_inicio(lista_id: int, vuelo_id: int, db: Session = Depends(get_db)):
    """
    AÑADE UN VUELO EXISTENTE AL PRINCIPIO DE UNA LISTA.
    """
    try:
        lista = flight_service.get_list_by_id(db, lista_id)
        if not lista:
            raise HTTPException(status_code=404, detail="Lista no encontrada")
        
        vuelo = flight_service.get_flight(db, vuelo_id)
        if not vuelo:
            raise HTTPException(status_code=404, detail="Vuelo no encontrado")
        
        nodo = linked_list.add_first(db, lista, vuelo)
        db.commit()
        return {"mensaje": f"Vuelo {vuelo.codigo} añadido al inicio de la lista"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al añadir vuelo al inicio: {str(e)}"
        )

@router.post("/listas/{lista_id}/vuelos/{vuelo_id}/final", status_code=status.HTTP_200_OK)
def add_vuelo_final(lista_id: int, vuelo_id: int, db: Session = Depends(get_db)):
    """
    AÑADE UN VUELO EXISTENTE AL FINAL DE UNA LISTA.
    """
    try:
        lista = flight_service.get_list_by_id(db, lista_id)
        if not lista:
            raise HTTPException(status_code=404, detail="Lista no encontrada")
        
        vuelo = flight_service.get_flight(db, vuelo_id)
        if not vuelo:
            raise HTTPException(status_code=404, detail="Vuelo no encontrado")
        
        nodo = linked_list.add_last(db, lista, vuelo)
        db.commit()
        return {"mensaje": f"Vuelo {vuelo.codigo} añadido al final de la lista"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al añadir vuelo al final: {str(e)}"
        )

@router.post("/listas/{lista_id}/priorizar")
def priorizar_vuelos(lista_id: int, db: Session = Depends(get_db)):
    """
    PRIORIZA LOS VUELOS EN LA LISTA SEGÚN SU ESTADO.
    (EMERGENCIA → EMBARQUE → PROGRAMADO → OTROS)
    """
    try:
        # Asegurarse de que la lista existe
        lista = flight_service.get_list_by_id(db, lista_id)
        if not lista:
            raise HTTPException(status_code=404, detail=f"Lista con ID {lista_id} no encontrada")
        
        # Priorizar vuelos
        resultado = linked_list.prioritize_flights(db, lista)
        db.commit()
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al priorizar vuelos: {str(e)}"
        )
