import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Usuario
from schemas import UsuarioSchema, UsuarioCreate
from exceptions import EmailDuplicado, UsuarioNoEncontrado

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/", response_model=List[UsuarioSchema])
def get_usuarios(db: Session = Depends(get_db)):
    logger.info("Obteniendo el listado de usuarios registrados...")
    return db.query(Usuario).all()


@router.post("/", response_model=UsuarioSchema, status_code=201)
def create_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    logger.info(f"Creando nuevo usuario con email: {payload.email}")

    if db.query(Usuario).filter(Usuario.email == payload.email).first():
        logger.warning(f"No se puede crear el usuario, el email {payload.email} ya está registrado")
        raise EmailDuplicado(payload.email)

    nuevo = Usuario(nombre=payload.nombre, email=payload.email)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    logger.info(f"Nuevo usuario registrado correctamente con id: {nuevo.id}")
    return nuevo