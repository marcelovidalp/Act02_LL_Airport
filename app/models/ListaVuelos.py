from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.Base import Base  

class ListaVuelos(Base):
    __tablename__ = "listas_vuelos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), default="Lista de vuelos")
    # Relación con vuelos (un vuelo pertenece a una lista)
    vuelos = relationship("Vuelo", back_populates="lista_vuelos")
    
    def __init__(self, nombre="Lista de vuelos"):
        self.nombre = nombre