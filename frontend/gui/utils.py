import streamlit as st
import io

def show_message_from_state():
    """Muestra mensajes guardados en el estado de Streamlit."""
    if "message" in st.session_state:
        msg = st.session_state.pop("message")
        st.info(msg)

def confirm_action(label, key):
    """Botón de confirmación simple con Streamlit."""
    return st.button(label, key=key)

def df_to_csv_bytes(df):
    """Convierte un DataFrame en bytes CSV descargables."""
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue().encode("utf-8")
