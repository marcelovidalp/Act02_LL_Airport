from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional, List

class EstadoVuelo(str, Enum):
    PROGRAMADO = "programado"
    EMERGENCIA = "emergencia"
    RETRASADO = "retrasado"

class VueloBase(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora: datetime
    origen: str
    destino: str

class VueloCreate(VueloBase):
    pass

class Vuelo(VueloBase):
    id: int

    class Config:
        orm_mode = True

class VueloResponse(BaseModel):
    vuelo: Vuelo

class VuelosResponse(BaseModel):
    vuelos: List[Vuelo]
    total: int
