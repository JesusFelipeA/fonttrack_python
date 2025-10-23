import streamlit as st
from backend.controllers.auth_controller import login, register

def build_auth_frame(on_success):
    st.markdown("""
        <style>
            /* Fondo general */
            .main {
                background: radial-gradient(circle at top left, #111428, #0c0c14);
                color: #f5f6fa;
                font-family: 'Poppins', sans-serif;
            }

            h1 {
                text-align: center;
                color: #00e0ff;
                font-weight: 700;
                letter-spacing: 1px;
                text-shadow: 0 0 8px rgba(0, 224, 255, 0.8);
            }

            /* Contenedor central con sombra y efecto de vidrio */
            .auth-card {
                background: rgba(30, 30, 45, 0.6);
                border: 1px solid rgba(0, 224, 255, 0.3);
                border-radius: 20px;
                padding: 2rem 2.5rem;
                box-shadow: 0 8px 25px rgba(0, 224, 255, 0.15);
                backdrop-filter: blur(12px);
                max-width: 420px;
                margin: 3rem auto;
                transition: all 0.3s ease;
            }

            .auth-card:hover {
                box-shadow: 0 8px 30px rgba(0, 224, 255, 0.25);
                transform: translateY(-2px);
            }

            /* Inputs */
            .stTextInput > div > input {
                background-color: rgba(20, 20, 35, 0.8);
                color: #fff;
                border: 1px solid #00e0ff33;
                border-radius: 8px;
                padding: 0.6em;
            }

            .stTextInput > div > input:focus {
                border-color: #00e0ff;
                box-shadow: 0 0 6px #00e0ff88;
            }

            /* Botones */
            .stButton button {
                background: linear-gradient(135deg, #00e0ff, #0077ff);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.6em 1.2em;
                font-weight: 600;
                font-size: 1rem;
                transition: all 0.3s ease;
                box-shadow: 0 0 10px rgba(0, 224, 255, 0.4);
            }

            .stButton button:hover {
                background: linear-gradient(135deg, #00b4ff, #0055ff);
                box-shadow: 0 0 20px rgba(0, 224, 255, 0.6);
                transform: scale(1.03);
            }

            /* Texto secundario */
            .note {
                text-align: center;
                color: #aaa;
                font-size: 0.9rem;
                margin-top: 1.5rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    st.title("🛒 FontTrack Store")
    st.markdown("<p style='text-align:center;color:#9fa3b0;'>Gestión inteligente de materiales y productos</p>", unsafe_allow_html=True)

    email = st.text_input("📧 Correo electrónico", placeholder="ejemplo@correo.com")
    password = st.text_input("🔒 Contraseña", type="password", placeholder="••••••••")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔑 Ingresar", use_container_width=True):
            user = login(email, password)
            if user:
                st.success("✅ Bienvenido de nuevo 👋")
                on_success(user)
            else:
                st.error("❌ Credenciales inválidas")

    with col2:
        if st.button("📝 Registrarse", use_container_width=True):
            user = register(email, password)
            if user:
                st.success("✅ Usuario creado correctamente 🎉")
            else:
                st.error("⚠️ El correo ya está registrado")

    st.markdown('<p class="note">© 2025 FontTrack | Tecnología para tu inventario</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
