from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from Base import Base

class Nodo(Base):
    __tablename__ = "nodo"
    id = Column(Integer, primary_key=True, index=True)
    vuelo_id = Column(Integer, ForeignKey("vuelos.id"))
    vuelo = relationship("Vuelo")
    siguiente_id = Column(Integer, ForeignKey("nodo.id"), nullable=True)
    anterior_id = Column(Integer, ForeignKey("nodo.id"), nullable=True)
    
    siguiente = relationship("Nodo", foreign_keys=[siguiente_id], remote_side=[id], post_update=True, uselist=False)
    anterior = relationship("Nodo", foreign_keys=[anterior_id], remote_side=[id], post_update=True, uselist=False)
    
    def __init__(self, vuelo=None):
        self.vuelo = vuelo