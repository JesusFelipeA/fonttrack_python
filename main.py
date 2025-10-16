import streamlit as st
from frontend.gui.auth_view import build_auth_frame
from frontend.gui.user_view import build_user_frame
from frontend.gui.material_window import build_material_frame
from frontend.gui.admin_view import build_admin_frame
from frontend.gui.lugares_window import build_lugar_frame  # 🆕 Nuevo import


def main():
    # Configuración inicial de la app
    st.set_page_config(
        page_title="Inventario de Materiales",
        page_icon="🧱",
        layout="wide"
    )

    # Si no hay usuario en sesión -> mostrar login
    if "user" not in st.session_state:
        def on_success(user):
            st.session_state.user = user  # Guardar usuario en la sesión
            #  Forzar recarga de la app tras iniciar sesión
            if hasattr(st, "rerun"):
                st.rerun()
            else:
                st.experimental_rerun()

        build_auth_frame(on_success)

    else:
        user = st.session_state.user

        # Opciones base del menú
        opciones = ["Catálogo de Materiales", "Lugares", "Perfil","Administración"]  # 🆕 Añadido "Lugares"

        # Solo los administradores ven el panel de administración
        if user.get("role") == "admin":
            opciones.append("Administración")

        # Menú lateral
        menu = st.sidebar.selectbox("Menú", opciones)

        # Rutas de navegación según menú
        if menu == "Catálogo de Materiales":
            build_material_frame()
        elif menu == "Lugares":
            build_lugar_frame()  # 🆕 Nuevo módulo
        elif menu == "Perfil":
            build_user_frame(user)
        elif menu == "Administración":
            build_admin_frame()

        # Botón para cerrar sesión
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.clear()
            if hasattr(st, "rerun"):
                st.rerun()
            else:
                st.experimental_rerun()


if __name__ == "__main__":
    main()
