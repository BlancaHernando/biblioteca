import streamlit as st
import requests

st.set_page_config(page_title="Gestión de Usuarios", page_icon="👤")

API_URL = "http://127.0.0.1:8007"

st.markdown("# Gestión de Usuarios")


@st.cache_data(ttl=60)
def obtener_usuarios():
    response = requests.get(f"{API_URL}/usuarios/")
    if response.status_code == 200:
        return response.json()
    return []
st.subheader("Registrar nuevo usuario")

with st.form("user_form"):
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Registrar")

    if submitted:
        if not nombre or not email:
            st.warning("Por favor rellena todos los campos.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/usuarios/",
                    json={"nombre": nombre, "email": email},
                )
                if response.status_code == 201:
                    st.success(f"Usuario '{nombre}' registrado correctamente.")
                    st.cache_data.clear()
                elif response.status_code == 400:
                    st.error(response.json().get("detail", "Error al registrar usuario."))
                else:
                    st.error(f"Error inesperado: {response.status_code}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
st.markdown("---")
st.subheader("Usuarios registrados")

try:
    usuarios = obtener_usuarios()
    if usuarios:
        st.table(usuarios)
    else:
        st.info("No hay usuarios registrados todavía.")
except Exception as e:
    st.error(f"Error de conexión con el servidor: {e}")
