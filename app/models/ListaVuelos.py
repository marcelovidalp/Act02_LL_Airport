from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.Base import Base  # Corregido: Ruta completa a Base

class ListaVuelos(Base):
    __tablename__ = "listas_vuelos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), default="Lista de vuelos")
    vuelos = relationship("Vuelo", back_populates="lista_vuelos")
    cabeza_id = Column(Integer, ForeignKey("nodo.id"), nullable=True)
    cola_id = Column(Integer, ForeignKey("nodo.id"), nullable=True)
    
    cabeza = relationship("Nodo", foreign_keys=[cabeza_id])
    cola = relationship("Nodo", foreign_keys=[cola_id])
    
    def __init__(self, nombre="Lista de vuelos"):
        self.nombre = nombre
        self.cabeza = None
        self.cola = None