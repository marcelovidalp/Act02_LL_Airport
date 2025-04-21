from sqlalchemy import Session
from fastapi import FastAPI
from models import vuelo, listaVuelos
from database import engine, SessionLocal, get_db
from models.Base import Base

app = FastAPI()

