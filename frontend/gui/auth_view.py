import streamlit as st
from backend.controllers.auth_controller import login, register

def build_auth_frame(on_success):
    st.markdown("""
        <style>
            .main {
                background-color: #1e1e2f;
                color: #f0f0f0;
                font-family: 'Segoe UI', sans-serif;
            }
            h1 {
                text-align: center;
                color: #00c8ff;
            }
            .stTextInput > div > input {
                background-color: #2e2e3e;
                color: #ffffff;
                border: 1px solid #444;
            }
            .stButton button {
                background-color: #00c8ff;
                color: white;
                border: none;
                padding: 0.5em 1em;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🛒 Bienvenido a FontTrack Store")

    email = st.text_input("📧 Correo electrónico")
    password = st.text_input("🔒 Contraseña", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔑 Ingresar", use_container_width=True):
            user = login(email, password)
            if user:
                on_success(user)
            else:
                st.error("❌ Credenciales inválidas")

    with col2:
        if st.button("📝 Registrarse", use_container_width=True):
            user = register(email, password)
            if user:
                st.success("✅ Usuario creado correctamente")
            else:
                st.error("⚠️ Correo ya registrado")
