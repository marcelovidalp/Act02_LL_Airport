"""
Models package for the Airport Management System
"""
from app.models.Base import Base
from app.models.EstadoVuelo import EstadoVuelo
from app.models.Nodo import Nodo
from app.models.Vuelo import Vuelo
from app.models.ListaVuelos import ListaVuelos

# Export models for easier importing from app.models
__all__ = ['Base', 'EstadoVuelo', 'Nodo', 'Vuelo', 'ListaVuelos']
