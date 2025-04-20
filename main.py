import uvicorn
import argparse
from fastapi import FastAPI
from api.routes import vuelo_routes
from models.vuelo import Base, Vuelo, TipoVuelo, PrioridadVuelo, TipoEmergencia
from config.database import engine, SessionLocal
import datetime

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

def load_sample_data():
    """Carga datos de ejemplo en la base de datos"""
    from sqlalchemy.orm import Session
    
    print("Cargando datos de ejemplo...")
    
    # Crear una sesión
    with Session(engine) as session:
        # Verificar si ya existen datos
        if session.query(Vuelo).count() > 0:
            print("La base de datos ya contiene datos. Omitiendo carga de ejemplos.")
            return
            
        # Crear algunos vuelos de ejemplo
        vuelos = [
            Vuelo(
                numero_vuelo="AA101",
                aerolinea="American Airlines",
                origen="Miami",
                destino="Nueva York",
                hora_programada=datetime.datetime.now() + datetime.timedelta(hours=1),
                tipo_vuelo=TipoVuelo.DESPEGUE
            ),
            Vuelo(
                numero_vuelo="DL202",
                aerolinea="Delta",
                origen="Los Angeles",
                destino="Chicago",
                hora_programada=datetime.datetime.now() + datetime.timedelta(hours=2),
                tipo_vuelo=TipoVuelo.DESPEGUE,
                prioridad=PrioridadVuelo.URGENTE
            ),
            Vuelo(
                numero_vuelo="UA303",
                aerolinea="United",
                origen="Londres",
                destino="Miami",
                hora_programada=datetime.datetime.now() + datetime.timedelta(minutes=30),
                tipo_vuelo=TipoVuelo.ATERRIZAJE
            )
        ]
        
        # Agregar todos los vuelos
        for vuelo in vuelos:
            session.add(vuelo)
            
        # Guardar cambios
        session.commit()
        print(f"Se cargaron {len(vuelos)} vuelos de ejemplo.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sistema de Gestión de Aeropuerto')
    parser.add_argument('--init-db', action='store_true', help='Inicializar la base de datos con datos de ejemplo')
    args = parser.parse_args()
    
    if args.init_db:
        load_sample_data()
        print("Base de datos inicializada con datos de ejemplo.")
        exit(0)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
