import uvicorn
from fastapi import FastAPI
from api.routes import vuelo_routes
from models.vuelo import Base
from config.database import engine

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Aeropuerto",
    description="API para gestionar la secuencia de vuelos utilizando una cola doblemente enlazada",
    version="1.0.0"
)

# Incluir routers
app.include_router(vuelo_routes.router)

# Ruta raíz
@app.get("/")
def read_root():
    return {
        "mensaje": "Bienvenido al Sistema de Gestión de Aeropuerto",
        "documentacion": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
