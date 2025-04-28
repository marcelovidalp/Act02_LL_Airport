import sys
import os
# Añadir el directorio del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.db import create_tables, get_db, SessionLocal
from app.models import ListaVuelos, Vuelo
from app.services import flight_service, linked_list
from app.services.linked_list_manager import LinkedListManager

app = FastAPI(
    title="Sistema de Gestión de Aeropuerto",
    description="API para gestionar vuelos utilizando una lista doblemente enlazada",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir acceso desde aplicaciones web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las orígenes (ajustar en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todas las cabeceras
)

# Crear tablas al iniciar la aplicación
create_tables()

# Incluir rutas
app.include_router(router, prefix="/api")

@app.on_event("startup")
def init_db():
    """Inicializa la base de datos con datos de ejemplo si está vacía"""
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        if db.query(Vuelo).count() == 0:
            # Crear una lista de vuelos
            lista_vuelos = ListaVuelos(nombre="Vuelos programados")
            db.add(lista_vuelos)
            db.flush()
            
            # Crear vuelos de ejemplo con diferentes estados
            vuelos = [
                Vuelo(codigo="IB3456", origen="Madrid", destino="Barcelona", estado="programado"),
                Vuelo(codigo="FR1234", origen="París", destino="Madrid", estado="embarque"),
                Vuelo(codigo="BA7890", origen="Londres", destino="Madrid", estado="emergencia")
            ]
            
            db.add_all(vuelos)
            db.flush()
            
            # Establecer explícitamente la relación entre vuelos y lista
            for vuelo in vuelos:
                vuelo.lista_vuelos_id = lista_vuelos.id
            
            db.flush()
            
            # Añadir vuelos a la lista según prioridad automática
            # Primero emergencias, luego embarques, luego programados
            # Usar el nuevo LinkedListManager
            LinkedListManager.add_first(db, lista_vuelos.id, vuelos[2])  # Emergencia primero
            LinkedListManager.add_last(db, lista_vuelos.id, vuelos[1])   # Embarque segundo
            LinkedListManager.add_last(db, lista_vuelos.id, vuelos[0])   # Programado último
            
            db.commit()
            print("Base de datos inicializada con datos de ejemplo")
        
        # Siempre sincronizar las listas al inicio
        listas = db.query(ListaVuelos).all()
        for lista in listas:
            # Asegurarse de que todos los vuelos estén relacionados con la lista
            vuelos_sin_lista = db.query(Vuelo).filter(Vuelo.lista_vuelos_id == None).all()
            for vuelo in vuelos_sin_lista:
                vuelo.lista_vuelos_id = lista.id
            db.commit()
            
            # Forzar la reconstrucción del caché
            LinkedListManager.clear_cache(lista.id)
            lista_en_memoria = LinkedListManager.get_list_instance(db, lista.id)
            
            # Verificar que todos los vuelos estén en la lista
            vuelos_en_lista = linked_list.get_all_flights(lista)
            vuelos_en_db = db.query(Vuelo).filter(Vuelo.lista_vuelos_id == lista.id).all()
            
            print(f"Lista {lista.id} sincronizada: {len(vuelos_en_lista)} vuelos en lista, {len(vuelos_en_db)} vuelos en DB")
        
    except Exception as e:
        db.rollback()
        print(f"Error en inicialización: {e}")
    finally:
        db.close()

@app.get("/")
def read_root():
    """
    Punto de entrada raíz con instrucciones para acceder a la documentación.
    """
    return {
        "message": "Bienvenido al Sistema de Gestión de Aeropuerto (Refactorizado)",
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "instrucciones": "Accede a http://localhost:8000/docs o http://127.0.0.1:8000/docs para ver la documentación Swagger"
    }

if __name__ == "__main__":
    host = "0.0.0.0"  # Escucha en todas las interfaces
    port = 8000
    
    print(f"\n🚀 Servidor iniciado correctamente!")
    print(f"📝 Documentación disponible en: http://localhost:{port}/docs")
    print(f"📘 Documentación alternativa: http://localhost:{port}/redoc")
    print(f"🔗 Para acceder desde otras máquinas: http://<IP-DE-TU-MÁQUINA>:{port}/docs\n")
    
    uvicorn.run("main:app", host=host, port=port, reload=True)
