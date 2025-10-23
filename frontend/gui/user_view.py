import streamlit as st
import time

def build_user_frame(user=None):
   

    # --- Validación de datos ---
    if not isinstance(user, dict) or not user:
        st.markdown("""
            <div style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">😕</div>
                <h3 style="color: #6B7280; margin-bottom: 1rem;">Información de usuario no disponible</h3>
                <p style="color: #9CA3AF;">No se pudo cargar la información del perfil. Esto puede deberse a:</p>
                <ul style="color: #9CA3AF; text-align: left; display: inline-block; margin: 1rem auto;">
                    <li>Sesión expirada</li>
                    <li>Problemas de conexión</li>
                    <li>Datos de usuario incompletos</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Intentar de nuevo", use_container_width=True):
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()
        return

    # --- Mapeo flexible de claves ---
    nombre = user.get("nombre") or user.get("name") or "Sin nombre"
    correo = user.get("correo") or user.get("email") or "Sin correo"
    rol = user.get("rol") or user.get("role") or "Sin rol"

    # --- Estilos personalizados modernos ---
    st.markdown("""
        <style>
        @keyframes fadeInUp {
            from {opacity: 0; transform: translateY(30px);}
            to {opacity: 1; transform: translateY(0);}
        }
        @keyframes pulse {
            0%, 100% {transform: scale(1);}
            50% {transform: scale(1.05);}
        }
        @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        .user-card {
            background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
            background-size: 200% 200%;
            animation: gradientShift 8s ease infinite, fadeInUp 0.8s ease-out;
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            color: white;
            text-align: center;
            max-width: 700px;
            margin: 2rem auto;
            font-family: 'Segoe UI', sans-serif;
        }
        .user-avatar {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: linear-gradient(135deg, #FFD700, #FFA500);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            margin: 0 auto 1.5rem;
            border: 4px solid white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            animation: pulse 2s ease-in-out infinite;
        }
        .user-card h2 {
            color: white;
            font-size: 2rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }
        .role-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 0.5rem 1.5rem;
            border-radius: 25px;
            font-weight: 600;
            margin-top: 0.5rem;
            border: 2px solid rgba(255,255,255,0.3);
        }
        .info-line {
            background: rgba(255, 255, 255, 0.1);
            margin: 1rem auto;
            padding: 1rem;
            border-radius: 10px;
            max-width: 500px;
            backdrop-filter: blur(10px);
        }
        .info-line strong {
            color: #FFD700;
        }
        .action-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Avatar basado en iniciales ---
    def get_user_avatar(name):
        if not name or name == "Sin nombre":
            return "👤"
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[-1][0]}".upper()
        return name[0].upper()

    avatar_text = get_user_avatar(nombre)

    # --- Tarjeta del usuario ---
    profile_html = f"""
    <div class="user-card">
        <div class="user-avatar">{avatar_text}</div>
        <h2>{nombre}</h2>
        <div class="role-badge">🧩 {rol.upper()}</div>
        <div class="info-line"><strong>Correo:</strong> {correo}</div>
    </div>
    """
    st.markdown(profile_html, unsafe_allow_html=True)

    # --- Botones de acción ---
    st.markdown("<div class='action-buttons'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Actualizar", use_container_width=True):
            with st.spinner("Actualizando información..."):
                time.sleep(1)
            st.success("✅ Perfil actualizado correctamente")
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()

    with col2:
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            with st.spinner("Cerrando sesión..."):
                time.sleep(1)
            st.session_state.clear()
            st.success("✅ Sesión cerrada correctamente")
            time.sleep(1)
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    example_user = {
        "nombre": "Ana García López",
        "correo": "ana.garcia@empresa.com",
        "rol": "administrador"
    }
    build_user_frame(example_user)
