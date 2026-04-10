
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from server import app
import models

TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine_test)

Base.metadata.create_all(bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    """Limpia los datos antes de cada test."""
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield


@pytest.fixture
def client():
    return TestClient(app)

class TestLibros:
    def test_listar_libros_vacio(self, client):
        response = client.get("/libros/")
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_libros_con_datos(self, client):
        db = TestingSessionLocal()
        db.add(models.Libro(id=1, titulo="1984", autor="Orwell", genero="Distopía", disponible=True))
        db.commit()
        db.close()

        response = client.get("/libros/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["titulo"] == "1984"

class TestUsuarios:
    def test_crear_usuario(self, client):
        response = client.post("/usuarios/", json={"nombre": "Ana", "email": "ana@test.com"})
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Ana"
        assert data["email"] == "ana@test.com"
        assert "id" in data

    def test_email_duplicado_devuelve_400(self, client):
        client.post("/usuarios/", json={"nombre": "Ana", "email": "ana@test.com"})
        response = client.post("/usuarios/", json={"nombre": "Ana2", "email": "ana@test.com"})
        assert response.status_code == 400

    def test_listar_usuarios_vacio(self, client):
        response = client.get("/usuarios/")
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_usuarios_con_datos(self, client):
        client.post("/usuarios/", json={"nombre": "Ana", "email": "ana@test.com"})
        response = client.get("/usuarios/")
        assert len(response.json()) == 1

class TestPrestamos:
    def _insertar_libro(self, disponible=True):
        db = TestingSessionLocal()
        db.add(models.Libro(id=1, titulo="1984", autor="Orwell", genero="Distopía", disponible=disponible))
        db.commit()
        db.close()

    def _crear_usuario(self, client):
        r = client.post("/usuarios/", json={"nombre": "Carlos", "email": "carlos@test.com"})
        return r.json()["id"]

    def test_crear_prestamo_correcto(self, client):
        self._insertar_libro()
        usuario_id = self._crear_usuario(client)
        response = client.post("/prestamos/", json={"libro_id": 1, "usuario_id": usuario_id})
        assert response.status_code == 201
        assert response.json()["libro_id"] == 1

    def test_prestamo_marca_libro_no_disponible(self, client):
        self._insertar_libro()
        usuario_id = self._crear_usuario(client)
        client.post("/prestamos/", json={"libro_id": 1, "usuario_id": usuario_id})
        libros = client.get("/libros/").json()
        assert libros[0]["disponible"] is False

    def test_prestamo_libro_no_disponible_devuelve_400(self, client):
        self._insertar_libro(disponible=False)
        usuario_id = self._crear_usuario(client)
        response = client.post("/prestamos/", json={"libro_id": 1, "usuario_id": usuario_id})
        assert response.status_code == 400

    def test_prestamo_libro_inexistente_devuelve_404(self, client):
        usuario_id = self._crear_usuario(client)
        response = client.post("/prestamos/", json={"libro_id": 999, "usuario_id": usuario_id})
        assert response.status_code == 404

    def test_prestamo_usuario_inexistente_devuelve_404(self, client):
        self._insertar_libro()
        response = client.post("/prestamos/", json={"libro_id": 1, "usuario_id": 999})
        assert response.status_code == 404

    def test_listar_prestamos(self, client):
        self._insertar_libro()
        usuario_id = self._crear_usuario(client)
        client.post("/prestamos/", json={"libro_id": 1, "usuario_id": usuario_id})
        response = client.get("/prestamos/")
        assert response.status_code == 200
        assert len(response.json()) == 1
