import streamlit as st
import pandas as pd
import time
from datetime import datetime


# CONTROLADORES
from backend.controllers.user_controller import (
    get_all_users, create_user, update_user, delete_user
)

# Vista del perfil de usuario
from frontend.gui.user_view import build_user_frame

# CONFIGURACIÓN DE ESTILOS MODERNOS
def apply_admin_styles():
    st.markdown("""
        <style>
        /* Variables de colores */
        :root {
            --admin-primary: #6366F1;
            --admin-secondary: #8B5CF6;
            --admin-success: #10B981;
            --admin-warning: #F59E0B;
            --admin-error: #EF4444;
            --admin-dark: #1F2937;
            --admin-light: #F9FAFB;
        }
        
        /* Animaciones */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .fade-in { animation: fadeIn 0.6s ease-out; }
        .slide-in { animation: slideIn 0.4s ease-out; }
        
        /* Tarjetas modernas */
        .admin-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border-left: 4px solid var(--admin-primary);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .admin-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        /* Botones modernos */
        .stButton > button {
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        .btn-primary { 
            background: linear-gradient(135deg, var(--admin-primary), var(--admin-secondary)) !important; 
            color: white !important; 
        }
        .btn-success { 
            background: linear-gradient(135deg, var(--admin-success), #059669) !important; 
            color: white !important; 
        }
        .btn-danger { 
            background: linear-gradient(135deg, var(--admin-error), #DC2626) !important; 
            color: white !important; 
        }
        
        /* Mejoras en formularios */
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea {
            border-radius: 8px;
            border: 2px solid #E5E7EB;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus, 
        .stTextArea > div > div > textarea:focus {
            border-color: var(--admin-primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        /* Radio buttons mejorados */
        .stRadio > div {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        /* Tooltips */
        .tooltip-icon {
            display: inline-block;
            width: 18px;
            height: 18px;
            background: var(--admin-primary);
            color: white;
            border-radius: 50%;
            text-align: center;
            font-size: 12px;
            font-weight: bold;
            margin-left: 5px;
            cursor: pointer;
            line-height: 18px;
        }
        
        .required-field::after {
            content: " *";
            color: var(--admin-error);
        }
        
        /* Métricas destacadas */
        .metric-highlight {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
        }
        
        /* Estados de usuario */
        .user-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid var(--admin-success);
            margin-bottom: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .user-card.admin {
            border-left-color: var(--admin-primary);
        }
        
        .user-card.inactive {
            border-left-color: var(--admin-warning);
            opacity: 0.7;
        }
        </style>
    """, unsafe_allow_html=True)

# UTILIDADES INTERNAS 
def show_message_from_state():
    if "msg" in st.session_state:
        msg, msg_type = st.session_state.pop("msg")
        if msg_type == "success":
            st.success(f"✅ {msg}")
        elif msg_type == "error":
            st.error(f"❌ {msg}")
        elif msg_type == "warning":
            st.warning(f"⚠️ {msg}")
        else:
            st.info(f"💡 {msg}")

def confirm_action(prompt: str, key: str):
    st.markdown("""
        <div class="admin-card slide-in" style="border-left-color: var(--admin-warning);">
            <h4 style="color: var(--admin-warning); margin-bottom: 1rem;">⚠️ Confirmación Requerida</h4>
            <p style="margin-bottom: 1rem;">{}</p>
        </div>
    """.format(prompt), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        confirm_btn = st.button("✅ Confirmar", key=key + "_yes", use_container_width=True)
    with col2:
        cancel_btn = st.button("❌ Cancelar", key=key + "_no", use_container_width=True)
    
    if confirm_btn:
        return True
    if cancel_btn:
        return False
    return None

def df_to_csv_bytes(df: pd.DataFrame):
    return df.to_csv(index=False).encode('utf-8')

def help_icon(tooltip_text, tooltip_id):
    st.markdown(f"""
        <div style="position: relative; display: inline-block;">
            <span class="tooltip-icon" onclick="document.getElementById('{tooltip_id}').style.display='block'">?</span>
            <div class="tooltip-content" id="{tooltip_id}" style="display: none; position: absolute; background: var(--admin-dark); color: white; padding: 0.8rem; border-radius: 8px; font-size: 0.85rem; z-index: 1000; width: 250px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                {tooltip_text}
            </div>
        </div>
    """, unsafe_allow_html=True)

def validate_user_data(correo, password, confirm_password):
    errors = []
    
    if not correo or "@" not in correo:
        errors.append("❌ Debe proporcionar un correo electrónico válido")
    
    if not password or len(password) < 6:
        errors.append("❌ La contraseña debe tener al menos 6 caracteres")
    
    if password != confirm_password:
        errors.append("❌ Las contraseñas no coinciden")
    
    # Validar  contraseña
    if password and len(password) >= 6:
        if not any(c.isupper() for c in password):
            errors.append("🔒 La contraseña debe contener al menos una mayúscula")
        if not any(c.isdigit() for c in password):
            errors.append("🔒 La contraseña debe contener al menos un número")
    
    return errors


# COMPONENTES REUTILIZABLES
def create_management_menu(options, key="menu"):
    """Menú de navegación moderno"""
    return st.radio(
        "Selecciona una acción:",
        options,
        horizontal=True,
        key=key
    )

def display_user_card(user):
    role = user.get('role', 'user')
    status_class = "admin" if role == "admin" else "user"
    
    st.markdown(f"""
        <div class="user-card {status_class} fade-in">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0 0 0.25rem 0; color: var(--admin-dark);">
                        👤 {user.get('correo', 'Sin correo')}
                    </h4>
                    <p style="margin: 0; color: #6B7280;">
                        🎭 Rol: <strong>{role.upper()}</strong> | 
                        📅 Creado: {user.get('fecha_creacion', 'N/A')}
                    </p>
                </div>
                <div style="font-size: 1.5rem;">
                    {"👑" if role == "admin" else "👤"}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ADMINISTRACIÓN DE USUARIOS MEJORADA
def administrar_usuarios():
    st.subheader("👤 Administración de Usuarios")
    show_message_from_state()

    menu_options = ["📄 Listar Usuarios", "➕ Crear Usuario", "✏️ Editar Usuario", "🗑️ Eliminar Usuario", "👁️ Ver Perfil"]
    menu = create_management_menu(menu_options, "user_menu")

    # VER PERFIL
    if "Ver Perfil" in menu:
        build_user_frame()

    # LISTAR
    elif "Listar" in menu:
        try:
            users = get_all_users() or []
            
            if not users:
                st.markdown("""
                    <div class="admin-card fade-in">
                        <div style="text-align: center; padding: 2rem;">
                            <h3 style="color: #6B7280;">👥 No hay usuarios registrados</h3>
                            <p>Comienza creando el primer usuario en la pestaña "Crear Usuario"</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Estadísticas
                total_users = len(users)
                admin_count = sum(1 for u in users if u.get('role') == 'admin')
                user_count = total_users - admin_count
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("👥 Total Usuarios", total_users)
                with col2:
                    st.metric("👑 Administradores", admin_count)
                with col3:
                    st.metric("👤 Usuarios Normales", user_count)
                
                st.markdown("---")
                
                # Filtros
                col_filter, col_search = st.columns(2)
                with col_filter:
                    filter_role = st.selectbox("Filtrar por rol:", ["Todos", "Administrador", "Usuario"])
                with col_search:
                    search_term = st.text_input("🔍 Buscar por correo:")
                
                # Aplicar filtros
                filtered_users = users
                if filter_role == "Administrador":
                    filtered_users = [u for u in filtered_users if u.get('role') == 'admin']
                elif filter_role == "Usuario":
                    filtered_users = [u for u in filtered_users if u.get('role') == 'user']
                
                if search_term:
                    filtered_users = [u for u in filtered_users if search_term.lower() in u.get('correo', '').lower()]
                
                st.write(f"**Mostrando {len(filtered_users)} de {total_users} usuarios**")
                
                # Mostrar usuarios
                for user in filtered_users:
                    display_user_card(user)
                
                # Exportar datos
                st.markdown("---")
                df = pd.DataFrame(filtered_users)
                col_export, col_info = st.columns([1, 3])
                with col_export:
                    st.download_button(
                        "📊 Exportar CSV",
                        df_to_csv_bytes(df),
                        "usuarios.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
        except Exception as e:
            st.error(f"❌ Error al cargar usuarios: {str(e)}")

    # CREAR
    elif "Crear" in menu:
        st.markdown("""
            <div class="admin-card fade-in">
                <h3 style="color: var(--admin-primary); margin-bottom: 1rem;">➕ Crear Nuevo Usuario</h3>
                <p style="color: #6B7280;">Complete todos los campos obligatorios para crear un nuevo usuario.</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("form_user", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<span class='required-field'>Correo electrónico</span>", unsafe_allow_html=True)
                correo = st.text_input(
                    "Correo electrónico",
                    placeholder="usuario@empresa.com",
                    label_visibility="collapsed"
                )
                
                st.markdown("<span class='required-field'>Rol del usuario</span>", unsafe_allow_html=True)
                role = st.selectbox(
                    "Rol del usuario",
                    ["user", "admin"],
                    format_func=lambda x: "👤 Usuario Normal" if x == "user" else "👑 Administrador",
                    label_visibility="collapsed"
                )
            
            with col2:
                st.markdown("<span class='required-field'>Contraseña</span>", unsafe_allow_html=True)
                password = st.text_input(
                    "Contraseña",
                    type="password",
                    placeholder="Mínimo 6 caracteres",
                    label_visibility="collapsed"
                )
                
                st.markdown("<span class='required-field'>Confirmar contraseña</span>", unsafe_allow_html=True)
                confirm = st.text_input(
                    "Confirmar contraseña", 
                    type="password",
                    placeholder="Repite la contraseña",
                    label_visibility="collapsed"
                )
            
            with st.expander("💡 Recomendaciones de seguridad"):
                st.write("""
                - **Contraseña segura**: Use al menos 6 caracteres con mayúsculas, minúsculas y números
                - **Correo único**: Cada usuario debe tener un correo electrónico único
                - **Roles**: Asigne rol de administrador solo a usuarios de confianza
                """)
            
            submitted = st.form_submit_button("💾 Crear Usuario", use_container_width=True)
            
            if submitted:
                errors = validate_user_data(correo, password, confirm)
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    try:
                        with st.spinner("🔄 Creando usuario..."):
                            time.sleep(1)  # Simular proceso
                            user_data = {
                                "correo": correo.strip(),
                                "role": role,
                                "password": password,
                                "fecha_creacion": datetime.now().isoformat()
                            }
                            create_user(user_data)
                        
                        st.success(f"🎉 Usuario '{correo}' creado exitosamente!")
                        time.sleep(2)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error al crear usuario: {str(e)}")

    # EDITAR
    elif "Editar" in menu:
        try:
            users = get_all_users() or []
            
            if not users:
                st.warning("⚠️ No hay usuarios disponibles para editar.")
            else:
                st.markdown("""
                    <div class="admin-card fade-in">
                        <h3 style="color: var(--admin-primary); margin-bottom: 1rem;">✏️ Editar Usuario Existente</h3>
                        <p style="color: #6B7280;">Selecciona un usuario y actualiza su información.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                user_options = ["-- Selecciona un usuario --"] + [u["correo"] for u in users]
                selected = st.selectbox("👤 Selecciona usuario a editar", user_options)
                
                if selected != "-- Selecciona un usuario --":
                    user = next(u for u in users if u["correo"] == selected)
                    
                    # Mostrar información actual
                    st.markdown("### 📋 Información Actual")
                    display_user_card(user)
                    
                    st.markdown("---")
                    st.markdown("### ✨ Editar Información")
                    
                    with st.form("edit_user_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nuevo_correo = st.text_input(
                                "📧 Nuevo correo electrónico",
                                value=user["correo"],
                                placeholder="nuevo@correo.com"
                            )
                        
                        with col2:
                            nuevo_role = st.selectbox(
                                "🎭 Nuevo rol",
                                ["user", "admin"],
                                index=0 if user["role"] == "user" else 1,
                                format_func=lambda x: "👤 Usuario" if x == "user" else "👑 Administrador"
                            )
                        
                        submitted = st.form_submit_button("🔄 Actualizar Usuario", use_container_width=True)
                        
                        if submitted:
                            if not nuevo_correo or "@" not in nuevo_correo:
                                st.error("❌ Debe proporcionar un correo electrónico válido")
                            else:
                                try:
                                    with st.spinner("🔄 Actualizando usuario..."):
                                        update_user(user["correo"], {
                                            "correo": nuevo_correo.strip(),
                                            "role": nuevo_role,
                                            "fecha_actualizacion": datetime.now().isoformat()
                                        })
                                    
                                    st.success(f"✅ Usuario '{nuevo_correo}' actualizado exitosamente!")
                                    time.sleep(2)
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Error al actualizar usuario: {str(e)}")
                                    
        except Exception as e:
            st.error(f"❌ Error al editar usuario: {str(e)}")

    # ELIMINAR
    elif "Eliminar" in menu:
        try:
            users = get_all_users() or []
            
            if not users:
                st.warning("⚠️ No hay usuarios disponibles para eliminar.")
            else:
                st.markdown("""
                    <div class="admin-card fade-in" style="border-left-color: var(--admin-error);">
                        <h3 style="color: var(--admin-error); margin-bottom: 1rem;">🗑️ Eliminar Usuario</h3>
                        <p style="color: #6B7280;">Selecciona un usuario para eliminar permanentemente.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                user_options = ["-- Selecciona un usuario --"] + [u["correo"] for u in users]
                selected = st.selectbox("👤 Selecciona usuario a eliminar", user_options)
                
                if selected != "-- Selecciona un usuario --":
                    user = next(u for u in users if u["correo"] == selected)
                    
                    st.error("🚨 **ACCIÓN IRREVERSIBLE**")
                    st.markdown(f"""
                        <div class="admin-card" style="background: #FEF2F2; border-left-color: var(--admin-error);">
                            <h4 style="color: var(--admin-error);">Estás a punto de eliminar al usuario:</h4>
                            <h3 style="color: var(--admin-dark); text-align: center;">{selected}</h3>
                            <p style="color: #6B7280; text-align: center;">
                                Esta acción no se puede deshacer y todos los datos asociados se perderán permanentemente.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.warning("**Paso 1:** Confirma que entiendes las consecuencias")
                    confirm_understanding = st.checkbox("✅ Comprendo que esta acción es permanente e irreversible")
                    
                    if confirm_understanding:
                        st.error("**Paso 2:** Verificación final")
                        st.write(f"Escribe el correo del usuario para confirmar: **{selected}**")
                        confirm_email = st.text_input("Escribe el correo exacto:")
                        
                        final_confirmation = confirm_email.strip() == selected
                    else:
                        final_confirmation = False
                    
                    col_delete, col_cancel = st.columns(2)
                    
                    with col_delete:
                        delete_disabled = not final_confirmation
                        delete_clicked = st.button(
                            "🗑️ ELIMINAR DEFINITIVAMENTE",
                            disabled=delete_disabled,
                            use_container_width=True,
                            type="primary"
                        )
                    
                    with col_cancel:
                        if st.button("❌ Cancelar Eliminación", use_container_width=True):
                            st.success("✅ Eliminación cancelada")
                            time.sleep(1)
                            st.rerun()
                    
                    if delete_clicked and final_confirmation:
                        try:
                            with st.spinner("🔄 Eliminando usuario..."):
                                time.sleep(1)
                                delete_user(selected)
                            
                            st.success(f"✅ Usuario '{selected}' eliminado exitosamente!")
                            time.sleep(2)
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error al eliminar usuario: {str(e)}")
                            
        except Exception as e:
            st.error(f"❌ Error al procesar eliminación: {str(e)}")

def mostrar_analytics():
    st.subheader("📊 Graficas — Vista Preliminar")
    st.info("Esta sección se actualizará con análisis sobre usuarios y actividades.")

# PANEL DE ADMINISTRACIÓN PRINCIPAL
def build_admin_frame():
    # Configuración de página
    st.set_page_config(
        page_title="Panel de Administración", 
        layout="wide",
        page_icon="⚙️"
    )
    
    # Aplicar estilos
    apply_admin_styles()
    
    # Header principal
    st.markdown("""
        <div class="fade-in">
            <h1 style="text-align: center; color: var(--admin-primary); margin-bottom: 0;">
                ⚙️ Panel de Administración
            </h1>
            <p style="text-align: center; color: #6B7280; margin-top: 0.5rem;">
                Gestiona usuarios y configuración del sistema
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    seccion = st.radio(
        "¿Qué deseas administrar?",
        ["👤 Usuarios", "📊 Analytics"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if seccion == "👤 Usuarios":
        administrar_usuarios()
    elif seccion == "📊 Graficos":
        mostrar_analytics()

if __name__ == "__main__":
    build_admin_frame()