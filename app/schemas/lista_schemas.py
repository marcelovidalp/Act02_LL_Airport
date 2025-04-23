from pydantic import BaseModel
from typing import List
from app.schemas.vuelo_schemas import VueloResponse

class ListaVuelosBase(BaseModel):
    nombre: str = "Lista de vuelos"

class ListaVuelosResponse(ListaVuelosBase):
    id: int
    vuelos: List[VueloResponse] = []

    class Config:
        orm_mode = True
