# Práctica Final: Gestor de Bibliotecas 📚

¡Bienvenidos a la práctica final de Programación II!

Este proyecto es un esqueleto inicial para un sistema de **Gestión de Bibliotecas**. Vuestro objetivo es transformar este código base (que intencionadamente tiene ineficiencias y partes incompletas) en una aplicación robusta, mantenible y profesional, aplicando todas las buenas prácticas vistas durante el curso.

## Objetivo

Desarrollar un sistema completo para gestionar el catálogo y préstamos de una biblioteca. Debéis demostrar vuestra capacidad para:

1. **Entender y Refactorizar** código existente.
2. **Diseñar** una arquitectura desacoplada y limpia.
3. **Implementar** soluciones técnicas avanzadas (bases de datos, APIs, interfaces gráficas).
4. **Trabajar en equipo** utilizando metodologías ágiles.

## Tecnologías Obligatorias

- **Python 3.10+**: Lenguaje base.
- **SQLAlchemy 2.x**: ORM para persistencia de datos (SQLite/PostgreSQL).
- **Pytest**: Suite de tests con una cobertura mínima del **80%**.
- **Streamlit**: Interfaz gráfica para usuarios y bibliotecarios.
- **Git + GitHub**: Control de versiones y flujo de trabajo colaborativo.
- **GitHub Actions**: CI/CD básico para ejecutar tests en cada push.

## Principios SOLID (Obligatorio)

### SRP - Single Responsibility Principle

Este principio dice que cada fichero debe tener una sola responsabilidad. En nuestro proyecto lo hemos aplicado separando el código en ficheros según su función:

- `database.py` solo se encarga de crear la conexión con la base de datos. No hace nada más.
- `models.py` solo define cómo son las tablas de la base de datos (Libro, Usuario, Préstamo).
- `schemas.py` solo se encarga de validar que los datos que llegan a la API son correctos.
- `exceptions.py` solo define los errores personalizados como `LibroNoEncontrado` o `EmailDuplicado`.
- Cada router (`libros.py`, `usuarios.py`, `prestamos.py`) solo gestiona los endpoints de su propio recurso.

Así, si hay un problema con los libros, solo tenemos que tocar `libros.py` sin afectar al resto del código.

### OCP - Open/Closed Principle
Este principio dice que si queremos añadir algo nuevo al proyecto, no hace falta tocar el código que ya funciona. En nuestro proyecto lo hemos aplicado así:
- Si quisiéramos añadir una nueva funcionalidad como reservas, solo tendríamos que crear un fichero nuevo routers/reservas.py. No habría que modificar libros.py, usuarios.py ni prestamos.py.
- Si quisiéramos añadir un nuevo error, solo hay que añadirlo en exceptions.py sin tocar nada más.
Esto es muy útil porque si tocamos el código que ya funciona, podemos romper o hacer que algo deje de funcionar sin querer y sin darnos cuenta.

### LSP - Liskov Substitution Principle
Este principio dice que si una clase hereda de otra, tiene que comportarse exactamente igual que ella. Es decir, puedes sustituir la clase madre por la clase hija y todo sigue funcionando igual.
En nuestro proyecto lo hemos aplicado en exceptions.py. Hemos creado tres clases de error propias que heredan de HTTPException que es la clase de error de FastAPI:
- LibroNoEncontrado → se lanza cuando se busca un libro que no existe
- LibroNoDisponible → se lanza cuando se intenta pedir un libro que ya está prestado
- UsuarioNoEncontrado → se lanza cuando se busca un usuario que no existe
Como las tres heredan de HTTPException, FastAPI las reconoce y las maneja igual que cualquier otro error. 

### ISP - Interface Segregation Principle
Este principio dice que es mejor tener varios schemas pequeños con solo lo necesario, que uno grande con todo.

En nuestro proyecto lo hemos aplicado en schemas.py. Por ejemplo con los usuarios tenemos dos schemas separados:

- UsuarioCreate solo tiene nombre y email — es el que se usa cuando se crea un usuario. No tiene id porque en ese momento todavía no existe, lo genera la base de datos automáticamente.
- UsuarioSchema tiene nombre, email e id — es el que se usa cuando la API devuelve un usuario, porque ahí ya sí existe el id.

Así cada schema tiene únicamente los campos que necesita en cada momento, sin campos de más.

### DIP - Dependency Inversion Principle
Este principio dice que el código no debe crear sus propias dependencias, sino recibirlas desde fuera.
En nuestro proyecto lo hemos aplicado con la base de datos. Los endpoints no crean la conexión a la base de datos ellos solos, sino que FastAPI se la pasa automáticamente a través de Depends(get_db):
- En routers/libros.py, el endpoint recibe la base de datos así: def get_libros(db: Session = Depends(get_db))
- El endpoint no sabe cómo se crea la base de datos, solo la usa.
En los tests no queremos usar la base de datos real porque podría llenarse de datos de prueba. Entonces le decimos a FastAPI que use una base de datos de mentira que solo existe mientras se ejecutan los tests. Esto es posible gracias a que usamos Depends, ya que nos permite cambiarla fácilmente sin tocar nada del código.

## Metodología: eXtreme Programming (XP)

Durante los 3 sprints de la práctica, es OBLIGATORIO:

- **Pair Programming**: Evidenciado en los commits (`co-authored-by`).
- **TDD (Test-Driven Development)**: Escribir tests *antes* que el código.
- **Refactoring Continuo**: Mejorar el código sin cambiar su comportamiento externo.
- **Integración Continua**: GitHub Actions activo.
- **Stand-ups Diarios**: Registro en `DAILYS.md` (fecha, asistentes, qué hice, qué haré, bloqueos).

## Sistema de Evaluación Incremental

El peso de la práctica es del **35%** de la nota final. La evaluación es incremental:

### 1. Aprobado (5-6) - "Funcionamiento Básico"

- El sistema permite listar libros, crear usuarios y gestionar préstamos básicos.
- Uso correcto de Git (commits semánticos).
- Tests unitarios básicos definidos y pasando (usando Mocks para aislar dependencias).
- Código limpio y organizado.

### 2. Notable (7-8) - "Nos centramos en robustez y calidad"

**Todo lo del Aprobado, más:**

- **Excepciones Personalizadas**: Gestión de errores robusta y tipada.
- **Logging**: Sistema de logs con al menos 3 niveles (INFO, WARNING, ERROR).
- **Refactorización del Backend**: Uso de `FastAPI` con **Enrutadores (APIRouter)** para organizar los endpoints.
- **Optimización**: "Cachear" datos en Streamlit para mejorar el rendimiento.

### 3. Sobresaliente (9) - "Aplicamos principios de Ingeniería del Software"

**Todo lo del Notable, más:**

- **Decoradores**: Uso justificado de decoradores propios.
- **Properties**: Uso de `@property` para encapsulamiento pythonico.
- **Context Managers**: Uso de `with ...` para gestión eficiente de recursos (sesiones DB, ficheros).
- **Generadores**: Uso de `yield` para procesar grandes volúmenes de datos de forma eficiente.

### 4. Matrícula de Honor (10)

**Todo lo del Sobresaliente, más alguno de:**

- Uso de una tecnología o técnica **no vista en clase**.
  - *Ejemplo*: Tests de Integración/Sistema (probando endpoints con `TestClient` o BD en memoria).
  - *Ejemplo*: Despliegue en la nube.
  - *Ejemplo*: Uso de una base de datos NoSQL auxiliar.
- Incluir un tercer contenedor donde se encuentre la base de datos.
- Sustituir docker compose por manifiestos de k8s.

---

## Arquitectura del Proyecto (Estado Inicial)

El esqueleto actual es intencionadamente ineficiente.

- `fastapi/`: Contiene el servidor API. Actualmente lee de un CSV (`books.csv`) en cada petición (¡Ineficiente!).
- `streamlit/`: Interfaz gráfica básica. Código mezclado y poco modular.
- `data/`: Directorio donde debéis implementar vuestros modelos de datos y conexión a BD.

### Vuestra misión

1. **Eliminar la dependencia del CSV**: Migrar a una base de datos real usando SQLAlchemy.
2. **Separar responsabilidades**: Que la UI no hable directamente con la BD, sino a través de Servicios/API.
3. **Dockerizar**: Mantener/Mejorar el `docker-compose.yml` para que todo arranque con un comando.

¡Mucho ánimo y a programar! 💻🔥
