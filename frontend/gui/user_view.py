# frontend/gui/user_view.py

import streamlit as st

def build_user_frame(user):
    st.title("👤 Perfil de usuario")

    with st.container():
        st.markdown(
            """
            <div style='background-color: #f0f2f6; padding: 2em; border-radius: 12px; margin-bottom: 2em;'>
                <span style='font-size: 1.2em; font-weight: bold;'>Correo:</span>
                <span style='font-size: 1.1em;'> {email} </span><br>
                <span style='font-size: 1.2em; font-weight: bold;'>Rol:</span>
                <span style='font-size: 1.1em;'> {role} </span>
            </div>
            """.format(email=user['email'], role=user['role']),
            unsafe_allow_html=True
        )
