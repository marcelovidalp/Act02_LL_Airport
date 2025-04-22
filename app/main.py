import sys
import os

# Agregar la raíz del proyecto al PYTHONPATH para resolver problemas de importación
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from app.database import engine
from models.base import Base
from routes.vuelo_routes import router as vuelo_router

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Vuelos de Aeropuerto",
    description="API para gestionar una lista de vuelos utilizando una estructura de datos de lista doblemente enlazada",
    version="1.0.0"
)

# Incluir rutas
app.include_router(vuelo_router)

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido al sistema de gestión de vuelos de aeropuerto"}

