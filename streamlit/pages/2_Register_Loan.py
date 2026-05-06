import streamlit as st
import requests

st.set_page_config(page_title="Préstamo de Libros", page_icon="✍️")

st.markdown("# Gestionar Préstamo")
st.write("Formulario para realizar un préstamo.")

API_URL = "http://fastapi:8000"

with st.form("loan_form"):
    libro_id = st.number_input("ID del Libro", min_value=1, step=1)
    usuario_id = st.number_input("ID de Usuario", min_value=1, step=1)
    submitted = st.form_submit_button("Realizar Préstamo")

    if submitted:
        try:
            response = requests.post(
                f"{API_URL}/prestamos/",
                json={"libro_id": int(libro_id), "usuario_id": int(usuario_id)}
            )
            if response.status_code == 201:
                st.success("¡Préstamo registrado correctamente!")
                st.json(response.json())
            elif response.status_code == 400:
                st.error("Error: el libro no está disponible.")
            elif response.status_code == 404:
                st.error("Error: el libro o el usuario no existe.")
            else:
                st.error(f"Error al registrar el préstamo: {response.status_code}")
        except Exception as e:
            st.error(f"Error de conexión con el servidor: {e}")