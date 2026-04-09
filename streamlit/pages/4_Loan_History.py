import streamlit as st
import requests

st.set_page_config(page_title="Historial de Préstamos", page_icon="📋")

API_URL = "http://127.0.0.1:8007"

st.markdown("# Historial de préstamos")


@st.cache_data(ttl=60)
def obtener_prestamos():
    response = requests.get(f"{API_URL}/prestamos/")
    if response.status_code == 200:
        return response.json()
    return []


usuario_id = st.text_input("Introduce el usuario (ID)")

if usuario_id:
    try:
        prestamos = obtener_prestamos()
        if prestamos is not None:
            prestamos_usuario = [p for p in prestamos if str(p["usuario_id"]) == usuario_id]

            if prestamos_usuario:
                st.dataframe(prestamos_usuario)
            else:
                st.info("Este usuario no tiene préstamos registrados.")
        else:
            st.error("Error al obtener los préstamos.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")

