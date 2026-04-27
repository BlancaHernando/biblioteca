# Gestor de Bibliotecas 📚

Sistema de gestión de bibliotecas desarrollado con FastAPI y Streamlit.

---

## ¿Cómo ejecutarlo?

### Sin Docker

**Terminal 1 — Backend:**
```bash
cd fastapi
pip install -r requirements.txt
uvicorn server:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd streamlit
pip install -r requirements.txt
streamlit run Library_App.py
```

### Ejecutar los tests
```bash
cd fastapi
pytest tests/ -v
```

---

## Estructura del proyecto

```
biblioteca/
├── fastapi/
│   ├── server.py         # Configuración principal de la API
│   ├── database.py       # Conexión a la base de datos SQLite
│   ├── models.py         # Tablas de la base de datos
│   ├── schemas.py        # Validación de datos
│   ├── exceptions.py     # Excepciones personalizadas
│   ├── decorators.py     # Decoradores propios
│   ├── services.py       # Lógica de negocio con @property y generadores
│   └── routers/
│       ├── libros.py     # Endpoints de libros
│       ├── usuarios.py   # Endpoints de usuarios
│       └── prestamos.py  # Endpoints de préstamos
└── streamlit/
    ├── Library_App.py    # Página principal
    └── pages/
        ├── 1_List_Books.py     # Catálogo de libros con buscador
        ├── 2_Register_Loan.py  # Registro de préstamos
        ├── 3_Usuarios.py       # Gestión de usuarios
        ├── 4_Loan_History.py   # Historial de préstamos
        └── 5_Loan_Calendar.py  # Calendario de préstamos
```

---

## Principios SOLID

### SRP — Single Responsibility Principle
> Cada fichero tiene una sola responsabilidad.

- `database.py` → solo gestiona la conexión a la BD
- `models.py` → solo define las tablas
- `schemas.py` → solo valida los datos de entrada y salida
- `exceptions.py` → solo define los errores personalizados
- Cada router solo gestiona sus propios endpoints

### OCP — Open/Closed Principle
> Abierto a extensión, cerrado a modificación.

- Para añadir un nuevo recurso (ej: reservas), creamos un nuevo fichero en `routers/` sin tocar los existentes
- Para añadir una nueva excepción, la añadimos en `exceptions.py` sin modificar los routers

### LSP — Liskov Substitution Principle
> Las clases hijas se comportan igual que la clase padre.

- `LibroNoEncontrado`, `UsuarioNoEncontrado` y `LibroNoDisponible` heredan de `HTTPException` y se pueden usar exactamente igual que ella en cualquier parte del código

### ISP — Interface Segregation Principle
> Mejor varios schemas pequeños que uno grande.

- `UsuarioCreate` solo tiene `nombre` y `email` — solo lo necesario para crear
- `UsuarioSchema` tiene además el `id` — para la respuesta
- `PrestamoCreate` solo tiene `libro_id` y `usuario_id`

### DIP — Dependency Inversion Principle
> Los módulos dependen de abstracciones, no de implementaciones concretas.

- Los endpoints reciben la sesión de BD mediante `Depends(get_db)` — FastAPI la inyecta automáticamente
- En los tests, sustituimos `get_db` por una BD en memoria sin cambiar el código de los endpoints

---

## Tecnologías usadas

| Tecnología | Para qué |
|-----------|----------|
| FastAPI | Backend y API REST |
| SQLAlchemy | ORM para la base de datos |
| SQLite | Base de datos local |
| Streamlit | Interfaz gráfica |
| Pytest | Tests unitarios |
| Docker | Despliegue con contenedores |

---

## Commits semánticos

- `feat:` nueva funcionalidad
- `fix:` corrección de errores
- `test:` añadir o modificar tests
- `refactor:` mejorar el código sin cambiar su comportamiento
