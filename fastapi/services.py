from sqlalchemy.orm import Session
from models import Libro


class LibroService:

    def __init__(self, db: Session):
        self._db = db

    @property
    def disponibles(self):
        return self._db.query(Libro).filter(Libro.disponible == True).all()

    @property
    def no_disponibles(self):
        return self._db.query(Libro).filter(Libro.disponible == False).all()

    def todos(self):
        return self._db.query(Libro).all()

    def por_id(self, libro_id: int):
        return self._db.query(Libro).filter(Libro.id == libro_id).first()

    def en_lotes(self, lote: int = 2):
        libros = self.todos()
        for i in range(0, len(libros), lote):
            yield libros[i:i + lote]
