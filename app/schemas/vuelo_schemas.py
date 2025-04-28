from pydantic import BaseModel, Field
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
        # Configuración para asegurar la serialización correcta
        schema_extra = {
            "example": {
                "id": 1,
                "codigo": "IB3456",
                "origen": "Madrid",
                "destino": "Barcelona",
                "aerolinea": "Iberia",
                "puerta_embarque": "B12",
                "hora": "2023-10-24T12:30:00",
                "estado": "programado",
                "lista_vuelos_id": 1
            }
        }
