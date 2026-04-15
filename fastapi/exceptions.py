from fastapi import HTTPException


class LibroNoEncontrado(HTTPException):
    def __init__(self, libro_id: int):
        super().__init__(status_code=404, detail=f"Libro con id {libro_id} no encontrado.")


class LibroNoDisponible(HTTPException):
    def __init__(self, libro_id: int):
        super().__init__(status_code=400, detail=f"El libro con id {libro_id} no está disponible.")


class UsuarioNoEncontrado(HTTPException):
    def __init__(self, usuario_id: int):
        super().__init__(status_code=404, detail=f"Usuario con id {usuario_id} no encontrado.")


class EmailDuplicado(HTTPException):
    def __init__(self, email: str):
        super().__init__(status_code=400, detail=f"Ya existe un usuario con el email {email}.")
