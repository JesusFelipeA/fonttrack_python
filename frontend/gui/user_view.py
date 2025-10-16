import streamlit as st

def build_user_frame(user=None):
    """
    Muestra el perfil del usuario autenticado en una tarjeta visual.
    Si no se recibe un usuario válido, muestra un mensaje de error amigable.
    """

    # --- Validación de datos ---
    if not isinstance(user, dict) or not user:
        st.warning("⚠️ No hay información del usuario en sesión.")
        if st.button("🔄 Volver al inicio"):
            st.session_state.clear()
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()
        return

    # --- Mapeo flexible de claves ---
    nombre = user.get("nombre") or user.get("name") or "Sin nombre"
    correo = user.get("correo") or user.get("email") or "Sin correo"
    rol = user.get("rol") or user.get("role") or "Sin rol"

    # --- Estilos personalizados ---
    st.markdown("""
        <style>
            .user-card {
                background: linear-gradient(145deg, #1c1f26, #222633);
                padding: 2rem;
                border-radius: 18px;
                box-shadow: 0 6px 15px rgba(0,0,0,0.3);
                color: #f0f0f0;
                text-align: center;
                max-width: 600px;
                margin: 2rem auto;
                font-family: 'Segoe UI', sans-serif;
            }
            .user-card h2 {
                color: #00c8ff;
                font-size: 1.8rem;
                margin-bottom: 1rem;
            }
            .user-card .info {
                font-size: 1.1rem;
                line-height: 1.8;
            }
            .user-card strong {
                color: #00ffd9;
            }
            .logout-btn button {
                background-color: #00c8ff !important;
                color: white !important;
                font-weight: bold !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 0.6rem 1.2rem !important;
                transition: 0.2s ease-in-out;
            }
            .logout-btn button:hover {
                background-color: #008fcc !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Tarjeta del perfil ---
    st.markdown(f"""
        <div class="user-card">
            <h2>👤 {nombre}</h2>
            <div class="info">
                <p><strong>📧 Correo:</strong> {correo}</p>
                <p><strong>🧩 Rol:</strong> {rol.capitalize()}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- Botón de cierre de sesión ---
    st.markdown("<div class='logout-btn' style='text-align:center;'>", unsafe_allow_html=True)

    if st.button("🚪 Cerrar sesión"):
        st.success("✅ Sesión cerrada correctamente.")
        st.session_state.clear()
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)
