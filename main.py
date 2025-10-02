# main.py

import streamlit as st
from frontend.gui.auth_view import build_auth_frame
from frontend.gui.user_view import build_user_frame
from frontend.gui.product_window import build_product_frame
from frontend.gui.admin_view import build_admin_frame

<<<<<<< HEAD
def main():
    st.set_page_config(page_title="Tienda Python", page_icon="🛒", layout="wide")
    if "user" not in st.session_state:
        def on_success(user):
            st.session_state.user = user
        build_auth_frame(on_success)
    else:
        user = st.session_state.user
        menu = st.sidebar.selectbox(
            "Menú",
            ("Catálogo", "Perfil", "Administración" if user.get("role") == "admin" else None)
        )
=======

def main():
    # Configuración inicial de la app
    st.set_page_config(
        page_title="Tienda Python",
        page_icon="🛒",
        layout="wide"
    )

    # Si no hay usuario en sesión -> mostrar login
    if "user" not in st.session_state:
        def on_success(user):
            st.session_state.user = user  # Guardar usuario en la sesión

        build_auth_frame(on_success)

    else:
        user = st.session_state.user

        # Opciones base del menú
        opciones = ["Catálogo", "Perfil"]

        # Solo los administradores ven el panel de administración
        if user.get("role") == "admin":
            opciones.append("Administración")

        # Menú lateral
        menu = st.sidebar.selectbox("Menú", opciones)

        # Rutas de navegación según menú
>>>>>>> 09544df (Crud de productos)
        if menu == "Catálogo":
            build_product_frame()
        elif menu == "Perfil":
            build_user_frame(user)
        elif menu == "Administración":
            build_admin_frame()

<<<<<<< HEAD
=======
        # Botón para cerrar sesión
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.clear()
            st.rerun()


>>>>>>> 09544df (Crud de productos)
if __name__ == "__main__":
    main()
