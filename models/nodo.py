from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base 

class Nodo(Base):
    __tablename__ = 'nodos'

    id = Column(Integer, primary_key=True, index=True)
    vuelo_id = Column(Integer, ForeignKey('vuelos.id'), nullable=False)  # Relación con Vuelo
    anterior = Column(Integer, ForeignKey('nodos.id'), nullable=True)  # Nodo anterior
    siguiente = Column(Integer, ForeignKey('nodos.id'), nullable=True)  # Nodo siguiente

    vuelo = relationship('Vuelo', backref='nodo')  # Relación con el modelo Vuelo
