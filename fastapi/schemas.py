from pydantic import BaseModel, ConfigDict


class LibroSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    titulo: str
    autor: str
    genero: str
    disponible: bool


class UsuarioCreate(BaseModel):
    nombre: str
    email: str


class UsuarioSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    email: str


class PrestamoCreate(BaseModel):
    libro_id: int
    usuario_id: int


class PrestamoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    libro_id: int
    usuario_id: int
    fecha: str
    estado: str
