from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class Libro(Base):
    __tablename__ = "libros"

    id         = Column(Integer, primary_key=True, index=True)
    titulo     = Column(String)
    autor      = Column(String)
    genero     = Column(String)
    disponible = Column(Boolean, default=True)



class Usuario(Base):
    __tablename__ = "usuarios"

    id     = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email  = Column(String, unique=True)


class Prestamo(Base):
    __tablename__ = "prestamos"

    id         = Column(Integer, primary_key=True, index=True)
    libro_id   = Column(Integer, ForeignKey("libros.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha      = Column(String)
    estado     = Column(String, default="Activo")
