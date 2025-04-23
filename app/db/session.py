from sqlalchemy.orm import sessionmaker
from app.db.config import engine

# Crea una SessionLocal para manejar las sesiones de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
