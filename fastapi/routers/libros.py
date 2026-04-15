import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import LibroSchema
from services import LibroService
from decorators import log_tiempo

logger = logging.getLogger(_name_)

router = APIRouter(prefix="/libros", tags=["libros"])


@router.get("/", response_model=List[LibroSchema])
@log_tiempo
def get_libros(db: Session = Depends(get_db)):
    logger.info("Obteniendo el listado completo de libros...")
    servicio = LibroService(db)
    return servicio.todos()


@router.get("/disponibles/", response_model=List[LibroSchema])
@log_tiempo
def get_libros_disponibles(db: Session = Depends(get_db)):
    logger.info("Obteniendo los libros disponibles para préstamo...")
    servicio = LibroService(db)
    return servicio.disponibles