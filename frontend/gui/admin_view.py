# frontend/gui/admin_view.py

import streamlit as st
from backend.controllers.user_controller import get_all_users, delete_user

def build_admin_frame():
    st.title("👤 Usuarios registrados")

    users = get_all_users()
    for user in users:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{user['email']} ({user['role']})")
        with col2:
            if st.button("Eliminar", key=user['email']):
                delete_user(user['email'])
                st.success(f"Usuario {user['email']} eliminado")
                st.experimental_rerun()
