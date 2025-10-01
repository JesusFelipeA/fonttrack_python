# main.py

import streamlit as st
from frontend.gui.auth_view import build_auth_frame
from frontend.gui.user_view import build_user_frame
from frontend.gui.product_window import build_product_frame
from frontend.gui.admin_view import build_admin_frame

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
        if menu == "Catálogo":
            build_product_frame()
        elif menu == "Perfil":
            build_user_frame(user)
        elif menu == "Administración":
            build_admin_frame()

if __name__ == "__main__":
    main()
