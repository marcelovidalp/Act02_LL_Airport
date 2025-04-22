from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey

from models.base import Base

class Vuelo(Base):
    __tablename__ = 'vuelos'

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), unique=True, nullable=False)  # Código único del vuelo
    estado = Column(Enum('programado', 'emergencia', 'retrasado'), nullable=False)
    hora = Column(DateTime, nullable=False)  # Hora del vuelo
    origen = Column(String(50), nullable=False)
    destino = Column(String(50), nullable=False)