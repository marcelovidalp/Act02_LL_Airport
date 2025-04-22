from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.vuelo import Vuelo
from models.listavuelos import ListaVuelos
from schemas.vuelo_schema import VueloCreate, VueloResponse, VuelosResponse, Vuelo as VueloSchema
from app.database import get_db
from models.nodo import Nodo

router = APIRouter(prefix="/vuelos", tags=["vuelos"])

# Variable global para mantener la instancia de ListaVuelos
lista_vuelos_instance = None

def get_lista_vuelos(db: Session = Depends(get_db)):
    global lista_vuelos_instance
    if lista_vuelos_instance is None:
        lista_vuelos_instance = ListaVuelos(session=db)
    return lista_vuelos_instance

@router.post("/", response_model=VueloResponse, status_code=status.HTTP_201_CREATED)
def crear_vuelo(vuelo: VueloCreate, db: Session = Depends(get_db), lista_vuelos: ListaVuelos = Depends(get_lista_vuelos)):
    db_vuelo = Vuelo(**vuelo.dict())
    db.add(db_vuelo)
    db.commit()
    db.refresh(db_vuelo)
    
    # Añadir a la lista según su estado
    if vuelo.estado == "emergencia":
        lista_vuelos.insertar_al_frente(db_vuelo)
    else:
        lista_vuelos.insertar_al_final(db_vuelo)
    
    return {"vuelo": db_vuelo}

@router.get("/total", response_model=int)
def obtener_total_vuelos(lista_vuelos: ListaVuelos = Depends(get_lista_vuelos)):
    return lista_vuelos.longitud()

@router.get("/proximo", response_model=VueloResponse)
def obtener_proximo_vuelo(lista_vuelos: ListaVuelos = Depends(get_lista_vuelos)):
    vuelo = lista_vuelos.obtener_primero()
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos en espera")
    return {"vuelo": vuelo}

@router.get("/ultimo", response_model=VueloResponse)
def obtener_ultimo_vuelo(lista_vuelos: ListaVuelos = Depends(get_lista_vuelos)):
    vuelo = lista_vuelos.obtener_ultimo()
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos en la lista")
    return {"vuelo": vuelo}

@router.post("/insertar", response_model=VueloResponse)
def insertar_vuelo_en_posicion(posicion: int, vuelo_id: int, db: Session = Depends(get_db), lista_vuelos: ListaVuelos = Depends(get_lista_vuelos)):
    vuelo = db.query(Vuelo).get(vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail=f"Vuelo con ID {vuelo_id} no encontrado")
    
    try:
        lista_vuelos.insertar_en_posicion(vuelo, posicion)
        return {"vuelo": vuelo}
    except IndexError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/extraer/{posicion}", response_model=VueloResponse)
def extraer_vuelo_de_posicion(posicion: int, lista_vuelos: ListaVuelos = Depends(get_lista_vuelos)):
    try:
        vuelo = lista_vuelos.extraer_de_posicion(posicion)
        if not vuelo:
            raise HTTPException(status_code=404, detail=f"No se pudo extraer vuelo en la posición {posicion}")
        return {"vuelo": vuelo}
    except IndexError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/lista", response_model=VuelosResponse)
def listar_todos_vuelos(db: Session = Depends(get_db), lista_vuelos: ListaVuelos = Depends(get_lista_vuelos)):
    if lista_vuelos.cabeza is None:
        return {"vuelos": [], "total": 0}
    
    vuelos = []
    actual_id = lista_vuelos.cabeza
    
    while actual_id:
        nodo = db.query(Nodo).get(actual_id)
        if not nodo:
            break
        
        vuelo = db.query(Vuelo).get(nodo.vuelo_id)
        if vuelo:
            vuelos.append(vuelo)
        
        actual_id = nodo.siguiente
    
    return {"vuelos": vuelos, "total": len(vuelos)}

@router.patch("/reordenar")
def reordenar_vuelos(db: Session = Depends(get_db), lista_vuelos: ListaVuelos = Depends(get_lista_vuelos)):
    # Obtener todos los vuelos
    vuelos = []
    actual_id = lista_vuelos.cabeza
    
    while actual_id:
        nodo = db.query(Nodo).get(actual_id)
        if not nodo:
            break
        
        vuelo = db.query(Vuelo).get(nodo.vuelo_id)
        if vuelo:
            vuelos.append(vuelo)
        
        actual_id = nodo.siguiente
    
    # Vaciar la lista
    while lista_vuelos.cabeza:
        lista_vuelos.extraer_de_posicion(0)
    
    # Reordenar según prioridad
    emergencias = [v for v in vuelos if v.estado == "emergencia"]
    normales = [v for v in vuelos if v.estado != "emergencia"]
    
    # Primero las emergencias
    for vuelo in emergencias:
        lista_vuelos.insertar_al_frente(vuelo)
    
    # Luego los normales
    for vuelo in normales:
        lista_vuelos.insertar_al_final(vuelo)
    
    return {"mensaje": "Vuelos reordenados correctamente", "emergencias": len(emergencias), "normales": len(normales)}
