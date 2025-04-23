import uvicorn
from fastapi import FastAPI
from app.api import router
from app.db import create_tables, get_db, SessionLocal
from app.models import ListaVuelos, Vuelo

app = FastAPI(
    title="Sistema de Gestión de Aeropuerto",
    description="API para gestionar vuelos utilizando una lista doblemente enlazada",
    version="1.0.0"
)

# Crear tablas al iniciar la aplicación
create_tables()

# Incluir rutas
app.include_router(router, prefix="/api")

@app.on_event("startup")
def init_db():
    """Inicializa la base de datos con datos de ejemplo si está vacía"""
    db = SessionLocal()
    
    # Verificar si ya hay datos
    if db.query(Vuelo).count() == 0:
        try:
            # Crear una lista de vuelos
            lista_vuelos = ListaVuelos(nombre="Vuelos programados")
            db.add(lista_vuelos)
            db.flush()
            
            # Crear vuelos de ejemplo
            vuelos = [
                Vuelo(codigo="IB3456", origen="Madrid", destino="Barcelona"),
                Vuelo(codigo="FR1234", origen="París", destino="Madrid", estado="embarque"),
                Vuelo(codigo="BA7890", origen="Londres", destino="Madrid", estado="emergencia")
            ]
            
            db.add_all(vuelos)
            db.flush()
            
            # Añadir vuelos a la lista
            from app.crud import ListaOperations
            ListaOperations.insertar_final(db, lista_vuelos, vuelos[0])
            ListaOperations.insertar_final(db, lista_vuelos, vuelos[1])
            ListaOperations.insertar_inicio(db, lista_vuelos, vuelos[2])  # Emergencia al inicio
            
            db.commit()
            print("Base de datos inicializada con datos de ejemplo")
        except Exception as e:
            db.rollback()
            print(f"Error al inicializar la base de datos: {e}")
        finally:
            db.close()

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gestión de Aeropuerto"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
