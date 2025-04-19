from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

# Enumeraciones para los esquemas
class TipoVueloSchema(str, Enum):
    DESPEGUE = "despegue"
    ATERRIZAJE = "aterrizaje"

class PrioridadVueloSchema(str, Enum):
    EMERGENCIA = "emergencia"
    URGENTE = "urgente"
    REGULAR = "regular"

class TipoEmergenciaSchema(str, Enum):
    FALLA_TECNICA = "falla_tecnica"
    COMBUSTIBLE_BAJO = "combustible_bajo"
    EMERGENCIA_MEDICA = "emergencia_medica"
    CLIMA_ADVERSO = "clima_adverso"
    NINGUNA = "ninguna"

# Esquema base para vuelos
class VueloBase(BaseModel):
    numero_vuelo: str = Field(..., example="AA123")
    aerolinea: str = Field(..., example="American Airlines")
    origen: str = Field(..., example="Nueva York")
    destino: str = Field(..., example="Miami")
    hora_programada: datetime
    tipo_vuelo: TipoVueloSchema
    prioridad: PrioridadVueloSchema = PrioridadVueloSchema.REGULAR
    tipo_emergencia: TipoEmergenciaSchema = TipoEmergenciaSchema.NINGUNA
    
# Esquema para crear un vuelo
class VueloCreate(VueloBase):
    pass

# Esquema para actualizar un vuelo
class VueloUpdate(BaseModel):
    aerolinea: Optional[str] = None
    origen: Optional[str] = None
    destino: Optional[str] = None
    hora_programada: Optional[datetime] = None
    estado: Optional[str] = None
    demora_minutos: Optional[int] = None

# Esquema para declarar emergencia
class EmergenciaDeclaracion(BaseModel):
    tipo_emergencia: TipoEmergenciaSchema
    
# Esquema para aplicar demora
class DemoraAplicacion(BaseModel):
    minutos: int = Field(..., gt=0, example=30)

# Esquema para respuesta con vuelo completo
class Vuelo(VueloBase):
    id: int
    estado: str
    demora_minutos: int
    
    class Config:
        orm_mode = True
