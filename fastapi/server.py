import logging
import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import engine, get_db_context, Base
import models
from routers import libros, usuarios, prestamos

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

def cargar_libros_csv(db: Session):
    if db.query(models.Libro).count() == 0:
        logger.info("Cargando libros desde CSV...")
        df = pd.read_csv('./books.csv', sep=';')
        for _, row in df.iterrows():
            libro = models.Libro(
                id=int(row['id']),
                titulo=row['titulo'],
                autor=row['autor'],
                genero=row['genero'],
                disponible=bool(row['disponible']),
            )
            db.add(libro)
        db.commit()
        logger.info("Libros cargados correctamente.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Arrancando la aplicación...")
    with get_db_context() as db:
        cargar_libros_csv(db)
    yield
    logger.info("Apagando la aplicación.")


app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestión de bibliotecas.",
    version="2.0.0",
    lifespan=lifespan,
)
app.include_router(libros.router)
app.include_router(usuarios.router)
app.include_router(prestamos.router)
