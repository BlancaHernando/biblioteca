import streamlit as st

st.set_page_config(page_title='Gestor de Bibliotecas', layout='wide', page_icon="📚")

st.write("# Gestor de Bibliotecas 📚")

st.markdown(
    """
    Bienvenido al sistema de gestión de bibliotecas.

    ### ¿Qué puedes hacer?
    - 📖 **List Books** — Ver el catálogo de libros, buscar por título o autor y filtrar por disponibilidad.
    - ✍️ **Register Loan** — Registrar un préstamo de un libro.
    - 👤 **Usuarios** — Crear y ver los usuarios del sistema.
    - 📋 **Loan History** — Consultar el historial de préstamos por usuario.
    - 📅 **Loan Calendar** — Ver todos los préstamos con su estado (Activo/Devuelto).

    ### Tecnologías usadas
    - **FastAPI** — Backend con base de datos SQLite y SQLAlchemy.
    - **Streamlit** — Interfaz web.
    - **Docker** — Despliegue con contenedores.

    Selecciona una opción en el menú de la izquierda.
    """
)
