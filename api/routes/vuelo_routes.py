from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...config.database import get_db
from ...models.vuelo import TipoVuelo, PrioridadVuelo, TipoEmergencia, Vuelo as VueloModel
from ...repositories.vuelo_repository import VueloRepository
from ...services.vuelo_service import VueloService
from ..schemas.vuelo_schema import Vuelo, VueloCreate, VueloUpdate, EmergenciaDeclaracion, DemoraAplicacion

router = APIRouter(prefix="/vuelos", tags=["vuelos"])

def get_vuelo_service(db: Session = Depends(get_db)):
    repository = VueloRepository(db)
    return VueloService(repository)

@router.post("/", response_model=Vuelo, status_code=status.HTTP_201_CREATED)
def crear_vuelo(vuelo_create: VueloCreate, service: VueloService = Depends(get_vuelo_service)):
    """Crea un nuevo vuelo en el sistema"""
    # Convertir del esquema Pydantic al modelo SQLAlchemy
    vuelo_db = VueloModel(
        numero_vuelo=vuelo_create.numero_vuelo,
        aerolinea=vuelo_create.aerolinea,
        origen=vuelo_create.origen,
        destino=vuelo_create.destino,
        hora_programada=vuelo_create.hora_programada,
        tipo_vuelo=TipoVuelo(vuelo_create.tipo_vuelo.value),
        prioridad=PrioridadVuelo(vuelo_create.prioridad.value),
        tipo_emergencia=TipoEmergencia(vuelo_create.tipo_emergencia.value)
    )
    
    # Agregar el vuelo usando el servicio
    return service.agregar_vuelo(vuelo_db)

@router.post("/{numero_vuelo}/emergencia", response_model=Vuelo)
def declarar_emergencia(numero_vuelo: str, emergencia: EmergenciaDeclaracion, 
                        service: VueloService = Depends(get_vuelo_service)):
    """Declara una emergencia para un vuelo"""
    vuelo = service.declarar_emergencia(numero_vuelo, TipoEmergencia(emergencia.tipo_emergencia.value))
    if not vuelo:
        raise HTTPException(status_code=404, detail=f"Vuelo {numero_vuelo} no encontrado")
    return vuelo

@router.post("/{numero_vuelo}/demora", response_model=Vuelo)
def aplicar_demora(numero_vuelo: str, demora: DemoraAplicacion,
                   service: VueloService = Depends(get_vuelo_service)):
    """Aplica una demora a un vuelo"""
    vuelo = service.aplicar_demora(numero_vuelo, demora.minutos)
    if not vuelo:
        raise HTTPException(status_code=404, detail=f"Vuelo {numero_vuelo} no encontrado")
    return vuelo

@router.get("/proximo/{tipo}", response_model=Vuelo)
def obtener_proximo_vuelo(tipo: str, service: VueloService = Depends(get_vuelo_service)):
    """Obtiene el próximo vuelo en la cola según el tipo (despegue/aterrizaje)"""
    if tipo not in ["despegue", "aterrizaje"]:
        raise HTTPException(status_code=400, detail="Tipo debe ser 'despegue' o 'aterrizaje'")
        
    vuelo = service.obtener_proximo_vuelo(tipo)
    if not vuelo:
        raise HTTPException(status_code=404, detail=f"No hay vuelos pendientes de {tipo}")
    return vuelo
