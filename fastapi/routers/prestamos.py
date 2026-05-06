import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from database import get_db
from models import Libro, Usuario, Prestamo
from schemas import PrestamoSchema, PrestamoCreate
from exceptions import LibroNoEncontrado, LibroNoDisponible, UsuarioNoEncontrado
from decorators import log_tiempo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/prestamos", tags=["préstamos"])


@router.get("/", response_model=List[PrestamoSchema])
@log_tiempo
def get_prestamos(db: Session = Depends(get_db)):
    logger.info("Obteniendo el listado completo de préstamos...")
    prestamos = db.query(Prestamo).all()
    logger.info(f"Se han encontrado {len(prestamos)} préstamos en total.")
    return prestamos


@router.post("/", response_model=PrestamoSchema, status_code=201)
@log_tiempo
def create_prestamo(payload: PrestamoCreate, db: Session = Depends(get_db)):
    logger.info(f"Intentando crear préstamo: libro {payload.libro_id}, usuario {payload.usuario_id}")

    libro = db.query(Libro).filter(Libro.id == payload.libro_id).first()
    if not libro:
        logger.error(f"Libro no encontrado: id {payload.libro_id}")
        raise LibroNoEncontrado(payload.libro_id)
    if not libro.disponible:
        logger.warning(f"Libro no disponible: id {payload.libro_id}")
        raise LibroNoDisponible(payload.libro_id)

    usuario = db.query(Usuario).filter(Usuario.id == payload.usuario_id).first()
    if not usuario:
        logger.error(f"Usuario no encontrado: id {payload.usuario_id}")
        raise UsuarioNoEncontrado(payload.usuario_id)

    libro.disponible = False
    db.commit()

    prestamo = Prestamo(
        libro_id=payload.libro_id,
        usuario_id=payload.usuario_id,
        fecha=str(date.today()),
    )
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    logger.info(f"Préstamo creado con id: {prestamo.id}")
    return prestamo


@router.put("/{prestamo_id}/devolver/", response_model=PrestamoSchema)
@log_tiempo
def devolver_libro(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not prestamo:
        logger.error(f"Préstamo no encontrado: id {prestamo_id}")
        raise HTTPException(status_code=404, detail="Préstamo no encontrado.")

    if prestamo.estado == "Devuelto":
        raise HTTPException(status_code=400, detail="Este préstamo ya fue devuelto.")

    prestamo.estado = "Devuelto"
    libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
    if libro:
        libro.disponible = True
        logger.info(f"Libro '{libro.titulo}' marcado como disponible de nuevo.")
    db.commit()
    db.refresh(prestamo)
    logger.info(f"Devolución registrada correctamente. Préstamo id: {prestamo_id}")
    return prestamo