import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.EstadoVuelo import EstadoVuelo
from app.models.Base import Base

class Vuelo(Base):
    __tablename__ = "vuelos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), unique=True, index=True)
    origen = Column(String(50))
    destino = Column(String(50))
    hora = Column(DateTime, default=datetime.utcnow)
    aerolinea = Column(String(50), nullable=True)
    puerta_embarque = Column(String(10), nullable=True)
    estado = Column(Enum(EstadoVuelo), default=EstadoVuelo.PROGRAMADO)

    # Relación con la lista de vuelos
    lista_vuelos_id = Column(Integer, ForeignKey("listas_vuelos.id"), nullable=True)
    lista_vuelos = relationship("ListaVuelos", back_populates="vuelos")
    
    def __init__(self, codigo, origen, destino, hora=None, aerolinea=None, 
                 puerta_embarque=None, estado="programado"):
        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.hora = hora or datetime.utcnow()
        self.aerolinea = aerolinea
        self.puerta_embarque = puerta_embarque
        
        if isinstance(estado, str):
            try:
                self.estado = EstadoVuelo[estado.upper()]
            except KeyError:
                self.estado = EstadoVuelo.PROGRAMADO
        else:
            self.estado = estado
    
    def __repr__(self):
        """Representación de cadena para depuración"""
        return f"Vuelo(id={self.id}, codigo='{self.codigo}', estado='{self.estado.name if hasattr(self.estado, 'name') else self.estado}')"