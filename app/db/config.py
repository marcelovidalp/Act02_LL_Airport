from sqlalchemy import create_engine
from app.models.Base import Base

# Configura la URL de la base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./airport.db"

# Crea el motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Función para crear todas las tablas
def create_tables():
    Base.metadata.create_all(bind=engine)
