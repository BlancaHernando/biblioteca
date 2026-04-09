import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import engine, get_db_context, Base
import models
from routers import libros, usuarios, prestamos

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando el servidor de la biblioteca...")
    with get_db_context() as db:
        if db.query(models.Libro).count() == 0:
            db.add_all([
                models.Libro(titulo="The Great Gatsby",         autor="F. Scott Fitzgerald", genero="Clásico",  disponible=True),
                models.Libro(titulo="1984",                     autor="George Orwell",        genero="Distopía", disponible=True),
                models.Libro(titulo="Python Crash Course",      autor="Eric Matthes",         genero="Técnico",  disponible=True),
                models.Libro(titulo="Clean Code",               autor="Robert C. Martin",     genero="Técnico",  disponible=False),
                models.Libro(titulo="The Pragmatic Programmer", autor="Andrew Hunt",          genero="Técnico",  disponible=True),
            ])
            db.commit()
            logger.info("Se han cargado los libros en la base de datos.")
    yield
    logger.info("Cerrando el servidor...")


app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestión de bibliotecas.",
    version="2.0.0",
    lifespan=lifespan,
)
app.include_router(libros.router)
app.include_router(usuarios.router)
app.include_router(prestamos.router)

logger.info("Routers registrados: libros, usuarios, préstamos.")