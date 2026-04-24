import streamlit as st
import requests

st.set_page_config(page_title="Calendario de Préstamos", page_icon="📅")

API_URL = "http://127.0.0.1:8007"

st.markdown("# Calendario de préstamos")
st.write("Vista de los préstamos registrados.")


@st.cache_data(ttl=60)
def obtener_prestamos():
    response = requests.get(f"{API_URL}/prestamos/")
    if response.status_code == 200:
        return response.json()
    return []


try:
    prestamos = obtener_prestamos()

    if prestamos:
        st.write("Préstamos:")
        for p in prestamos:
            col1, col2, col3 = st.columns(3)
            col1.write(f"Libro ID: {p['libro_id']}")
            col2.write(p["fecha"])
            col3.write(p["estado"])

        st.markdown("---")
        st.write("Estados:")
        st.markdown("- **Activo** → préstamo en curso")
        st.markdown("- **Devuelto** → préstamo finalizado")
    else:
        st.info("No hay préstamos registrados.")

except Exception as e:
    st.error(f"Error de conexión: {e}")
