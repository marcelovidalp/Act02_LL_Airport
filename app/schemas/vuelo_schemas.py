from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VueloBase(BaseModel):
    codigo: str
    origen: str
    destino: str
    aerolinea: Optional[str] = None
    puerta_embarque: Optional[str] = None
    hora: Optional[datetime] = None

class VueloCreate(VueloBase):
    estado: str = "programado"

class VueloUpdate(BaseModel):
    estado: str

class VueloResponse(VueloBase):
    id: int
    estado: str
    lista_vuelos_id: Optional[int] = None

    class Config:
        orm_mode = True
