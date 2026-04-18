import streamlit as st
import requests

st.set_page_config(page_title="Catálogo de Libros", page_icon="📖")

API_URL = "http://127.0.0.1:8007"

st.markdown("# Catálogo de Libros")
st.write("Listado de libros disponibles en la biblioteca.")


@st.cache_data(ttl=60)
def obtener_libros():
    response = requests.get(f"{API_URL}/libros/")
    if response.status_code == 200:
        return response.json()
    return []


try:
    libros = obtener_libros()

    busqueda = st.text_input("Buscar por título o autor")
    solo_disponibles = st.checkbox("Mostrar solo disponibles")

    if busqueda:
        libros = [l for l in libros if busqueda.lower() in l["titulo"].lower()
                  or busqueda.lower() in l["autor"].lower()]

    if solo_disponibles:
        libros = [l for l in libros if l["disponible"]]

    st.write(f"Total de libros mostrados: {len(libros)}")

    if libros:
        st.dataframe(libros)
    else:
        st.warning("No hay libros que coincidan con la búsqueda.")

except Exception as e:
    st.error(f"Error de conexión con el servidor: {e}")
    st.info("Asegúrate de que el contenedor 'fastapi' está corriendo.")