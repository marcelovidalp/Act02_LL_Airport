"""
Endpoints de API relacionados con vuelos
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app import schemas
from app.models import Vuelo, EstadoVuelo
from app.db import get_db
from app.services import flight_service, linked_list

router = APIRouter()

# IMPORTANTE: Endpoints fijos primero para evitar colisiones de rutas
@router.post("/vuelos", response_model=schemas.VueloResponse)
def create_vuelo(vuelo: schemas.VueloCreate, db: Session = Depends(get_db)):
    """
    CREA UN NUEVO VUELO EN LA BASE DE DATOS.
    
    Este endpoint crea un nuevo vuelo y lo añade a la lista de vuelos
    según su estado (emergencia o normal).
    """
    try:
        vuelo_db = flight_service.create_flight(db, vuelo)
        if vuelo.estado == EstadoVuelo.EMERGENCIA:
            linked_list.add_first(db, vuelo_db)
        else:
            linked_list.add_last(db, vuelo_db)
        
        db.commit()
        return vuelo_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear vuelo: {str(e)}"
        )

@router.get("/vuelos/total", response_model=Dict[str, int])
def get_total_flights(lista_id: int = 1, db: Session = Depends(get_db)):
    """
    RETORNA EL NÚMERO TOTAL DE VUELOS EN COLA.
    """
    try:
        lista = flight_service.get_list_by_id(db, lista_id)
        if not lista:
            raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
        
        total = linked_list.get_length(lista)
        return {"total": total}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener total de vuelos: {str(e)}"
        )

@router.get("/vuelos/proximo", response_model=schemas.VueloResponse)
def get_next_flight(lista_id: int = 1, db: Session = Depends(get_db)):
    """
    RETORNA EL PRIMER VUELO SIN REMOVER.
    """
    try:
        lista = flight_service.get_list_by_id(db, lista_id)
        if not lista:
            raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
        
        vuelo = linked_list.get_first(lista)
        if not vuelo:
            raise HTTPException(status_code=404, detail="No hay vuelos en la lista")
        
        return vuelo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener próximo vuelo: {str(e)}"
        )

@router.get("/vuelos/ultimo", response_model=schemas.VueloResponse)
def get_last_flight(lista_id: int = 1, db: Session = Depends(get_db)):
    """
    RETORNA EL ÚLTIMO VUELO SIN REMOVER.
    """
    try:
        lista = flight_service.get_list_by_id(db, lista_id)
        if not lista:
            raise HTTPException(status_code=404, detail="Lista de vuelos no encontrada")
        
        vuelo = linked_list.get_last(lista)
        if not vuelo:
            raise HTTPException(status_code=404, detail="No hay vuelos en la lista")
        
        return vuelo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener último vuelo: {str(e)}"
        )

# Endpoint para obtener todos los vuelos de la base de datos
@router.get("/vuelos", response_model=List[schemas.VueloResponse])
def read_vuelos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    OBTIENE TODOS LOS VUELOS DE LA BASE DE DATOS.
    
    Este endpoint muestra todos los vuelos existentes en la base de datos,
    independientemente de si están asociados a alguna lista o no.
    """
    try:
        vuelos = flight_service.get_all_flights(db, skip, limit)
        return vuelos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener vuelos de la base de datos: {str(e)}"
        )

@router.get("/vuelos/visualizar", response_model=Dict[str, Any])
def visualize_flight_list(lista_id: int = 1, db: Session = Depends(get_db)):
    """
    GENERA UNA REPRESENTACIÓN VISUAL DE LA ESTRUCTURA DE LA LISTA ENLAZADA.
    
    Muestra cómo los vuelos están organizados en los nodos de la lista.
    """
    try:
        from app.services.linked_list_manager import LinkedListManager
        
        # Obtener la lista desde la base de datos
        lista = flight_service.get_list_by_id(db, lista_id)
        if not lista:
            raise HTTPException(status_code=404, detail=f"Lista con ID {lista_id} no encontrada")
        
        # Obtener la instancia en memoria de la lista
        memoria_lista = LinkedListManager.get_list_instance(db, lista_id)
        
        # Crear la visualización
        representacion = memoria_lista.visualize()
        
        # Obtener datos adicionales para mostrar
        vuelos_en_lista = linked_list.get_all_flights(lista)
        
        return {
            "representacion_texto": representacion,
            "total_vuelos": len(vuelos_en_lista),
            "vuelos": [
                {
                    "posicion": idx,
                    "codigo": v.codigo,
                    "estado": str(v.estado.name),
                    "origen": v.origen,
                    "destino": v.destino
                } for idx, v in enumerate(vuelos_en_lista)
            ],
            "estructura": {
                "head": memoria_lista.head.data.codigo if memoria_lista.head else None,
                "tail": memoria_lista.tail.data.codigo if memoria_lista.tail else None,
                "size": memoria_lista.size()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al visualizar lista: {str(e)}"
        )

@router.delete("/vuelos/{vuelo_id}", response_model=Dict[str, str])
def delete_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    """
    ELIMINA UN VUELO DE LA BASE DE DATOS.
    
    Este endpoint elimina un vuelo específico de la base de datos.
    """
    try:
        vuelo = flight_service.get_flight(db, vuelo_id)
        if not vuelo:
            raise HTTPException(status_code=404, detail="Vuelo no encontrado")
        
        flight_service.delete_flight(db, vuelo)
        db.commit()
        
        return {"mensaje": f"Vuelo {vuelo.codigo} eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar vuelo: {str(e)}"
        )