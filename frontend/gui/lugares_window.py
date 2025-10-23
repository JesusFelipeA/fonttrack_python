import streamlit as st
import pandas as pd
import time
from datetime import datetime
from backend.controllers.lugar_controller import (
    get_all_lugares,
    create_lugar,
    update_lugar,
    delete_lugar
)



def apply_modern_styles():
    st.markdown("""
        <style>
        /* Paleta de colores moderna - Principios de Color */
        :root {
            --primary: #6366F1;
            --secondary: #8B5CF6;
            --success: #10B981;
            --warning: #F59E0B;
            --error: #EF4444;
            --dark: #1F2937;
            --light: #F9FAFB;
        }
        
        /* Animaciones suaves - Jerarquía Visual */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }
        
        .slide-in {
            animation: slideIn 0.3s ease-out;
        }
        
        /* Estilos modernos para contenedores */
        .modern-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border-left: 4px solid var(--primary);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .modern-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        /* Botones modernos - Ley de Fitts */
        .stButton > button {
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
            color: white !important;
        }
        
        .btn-danger {
            background: linear-gradient(135deg, var(--error), #DC2626) !important;
            color: white !important;
        }
        
        .btn-success {
            background: linear-gradient(135deg, var(--success), #059669) !important;
            color: white !important;
        }
        
        /* Mejoras en formularios - Eficiencia */
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea {
            border-radius: 8px;
            border: 2px solid #E5E7EB;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus, 
        .stTextArea > div > div > textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        /* Radio buttons modernos */
        .stRadio > div {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .stRadio > div > label {
            font-weight: 600;
            padding: 0.5rem;
            border-radius: 6px;
            transition: all 0.3s ease;
        }
        
        .stRadio > div > label:hover {
            background: #F3F4F6;
        }
        
        /* Mejora en mensajes */
        .stAlert {
            border-radius: 8px;
            border: none;
        }
        
        /* Espacio en blanco mejorado */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Iconos animados */
        .icon-pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        </style>
    """, unsafe_allow_html=True)

# COMPONENTES REUTILIZABLES MODERNOS

def modern_button(text, key, type="primary", icon="", use_container=True):
    """Botón moderno con soporte para formularios"""
    button_class = f"btn-{type}"
    
    # Estilos dinámicos para el tipo de botón
    st.markdown(f"""
        <style>
        .{button_class} {{
            background: linear-gradient(135deg, var(--{type}), var(--secondary)) !important;
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # Intentar usar el botón adecuado según el contexto
    try:
        return st.form_submit_button(f"{icon} {text}", key=key, use_container_width=use_container)
    except Exception:
        return st.button(f"{icon} {text}", key=key, use_container_width=use_container)

def modern_card(content, title="", emoji="🏠"):
    """Tarjeta moderna con animaciones"""
    st.markdown(f"""
        <div class="modern-card fade-in">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem; margin-right: 0.5rem;">{emoji}</span>
                <h4 style="margin: 0; color: var(--dark);">{title}</h4>
            </div>
            {content}
        </div>
    """, unsafe_allow_html=True)

def show_animated_message(message, message_type="success", duration=3):
    if message_type == "success":
        st.success(f"🎉 {message}")
    elif message_type == "error":
        st.error(f"❌ {message}")
    elif message_type == "warning":
        st.warning(f"⚠️ {message}")
    elif message_type == "info":
        st.info(f"💡 {message}")
    
    time.sleep(duration)
    st.rerun()

def validate_lugar_data(nombre, ubicacion, tipo, descripcion):
    """Validación comprehensiva de datos - Error humano"""
    errors = []
    
    if not nombre or len(nombre.strip()) < 2:
        errors.append("❌ El nombre debe tener al menos 2 caracteres")
    
    if not ubicacion or len(ubicacion.strip()) < 5:
        errors.append("❌ La ubicación debe ser más específica (mínimo 5 caracteres)")
    
    if not tipo or len(tipo.strip()) < 3:
        errors.append("❌ El tipo de lugar debe ser más descriptivo")
    
    if len(descripcion or "") > 500:
        errors.append("❌ La descripción no puede exceder 500 caracteres")
    
    return errors

# COMPONENTES ESPECÍFICOS DE LUGARES
def display_lugar_card(lugar):
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
                <div class="modern-card slide-in">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h4 style="margin: 0 0 0.5rem 0; color: var(--dark);">
                                🏠 {lugar.get('nombre', 'Sin nombre')}
                            </h4>
                            <p style="margin: 0.25rem 0; color: #6B7280;">
                                📍 <strong>Ubicación:</strong> {lugar.get('ubicacion', 'No especificada')}
                            </p>
                            <p style="margin: 0.25rem 0; color: #6B7280;">
                                🏷️ <strong>Tipo:</strong> {lugar.get('tipo', 'No especificado')}
                            </p>
                            <p style="margin: 0.25rem 0; color: #6B7280;">
                                📝 <strong>Descripción:</strong> {lugar.get('descripcion', 'Sin descripción')}
                            </p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

def create_lugar_form():
    with st.form("create_lugar_form", clear_on_submit=True):
        st.subheader("➕ Agregar Nuevo Lugar")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input(
                "🏷️ Nombre del lugar *",
                placeholder="Ej: Almacén Central",
                help="Nombre único y descriptivo para el lugar"
            )
            
            ubicacion = st.text_input(
                "📍 Ubicación física *",
                placeholder="Ej: Calle Principal #123, Ciudad",
                help="Dirección exacta o ubicación específica"
            )
        
        with col2:
            tipo = st.selectbox(
                "🏢 Tipo de lugar *",
                ["", "Almacén", "Oficina", "Tienda", "Taller", "Depósito", "Showroom", "Otro"],
                help="Selecciona el tipo de lugar"
            )
            
            if tipo == "Otro":
                tipo = st.text_input("Especifica el tipo de lugar")
        
        descripcion = st.text_area(
            "📝 Descripción",
            placeholder="Describe las características, uso o particularidades de este lugar...",
            max_chars=500,
            help="Máximo 500 caracteres"
        )
        
        # Contador de caracteres en tiempo real
        if descripcion:
            st.caption(f"📊 Caracteres: {len(descripcion)}/500")
        
        submitted = modern_button("Guardar Lugar", "create_submit", "success", "💾")
        
        if submitted:
            errors = validate_lugar_data(nombre, ubicacion, tipo, descripcion)
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                try:
                    # Animación de carga
                    with st.spinner("🔄 Guardando lugar..."):
                        time.sleep(1)  # Simulación de proceso
                        nuevo_lugar = {
                            "nombre": nombre.strip(),
                            "ubicacion": ubicacion.strip(),
                            "tipo": tipo.strip(),
                            "descripcion": descripcion.strip(),
                            "fecha_creacion": datetime.now().isoformat()
                        }
                        create_lugar(nuevo_lugar)
                    
                    show_animated_message("¡Lugar creado exitosamente!", "success")
                    
                except Exception as e:
                    st.error(f"❌ Error al crear el lugar: {str(e)}")

def edit_lugar_form():
    lugares = get_all_lugares()
    
    if not lugares:
        modern_card("No hay lugares disponibles para editar.", "Sin lugares", "😔")
        return
    
    st.subheader("✏️ Editar Lugar Existente")
    
    # Selector moderno
    lugar_options = ["-- Selecciona un lugar --"] + [l.get('nombre', 'Sin nombre') for l in lugares]
    selected_nombre = st.selectbox(
        "🔍 Selecciona el lugar a editar",
        lugar_options,
        key="edit_selector"
    )
    
    if selected_nombre != "-- Selecciona un lugar --":
        lugar = next((l for l in lugares if l.get('nombre') == selected_nombre), None)
        
        if lugar:
            with st.form("edit_lugar_form"):
                modern_card(f"Editando: **{lugar.get('nombre')}**", "Lugar seleccionado", "🎯")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    nuevo_nombre = st.text_input(
                        "🏷️ Nuevo nombre *",
                        value=lugar.get('nombre', ''),
                        placeholder="Nombre del lugar"
                    )
                    
                    nueva_ubicacion = st.text_input(
                        "📍 Nueva ubicación *",
                        value=lugar.get('ubicacion', ''),
                        placeholder="Ubicación física"
                    )
                
                with col2:
                    nuevo_tipo = st.selectbox(
                        "🏢 Tipo de lugar *",
                        ["Almacén", "Oficina", "Tienda", "Taller", "Depósito", "Showroom", "Otro"],
                        index=0 if lugar.get('tipo') == "Almacén" else 
                              1 if lugar.get('tipo') == "Oficina" else
                              2 if lugar.get('tipo') == "Tienda" else
                              3 if lugar.get('tipo') == "Taller" else
                              4 if lugar.get('tipo') == "Depósito" else
                              5 if lugar.get('tipo') == "Showroom" else 6,
                        help="Selecciona el tipo de lugar"
                    )
                    
                    if nuevo_tipo == "Otro":
                        nuevo_tipo = st.text_input("Especifica el tipo", value=lugar.get('tipo', ''))
                
                nueva_descripcion = st.text_area(
                    "📝 Nueva descripción",
                    value=lugar.get('descripcion', ''),
                    max_chars=500,
                    placeholder="Describe el lugar..."
                )
                
                if nueva_descripcion:
                    st.caption(f"📊 Caracteres: {len(nueva_descripcion)}/500")
                
                submitted = modern_button("Actualizar Lugar", "edit_submit", "primary", "🔄")
                
                if submitted:
                    errors = validate_lugar_data(nuevo_nombre, nueva_ubicacion, nuevo_tipo, nueva_descripcion)
                    
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        try:
                            with st.spinner("🔄 Actualizando lugar..."):
                                time.sleep(1)
                                datos_actualizados = {
                                    "nombre": nuevo_nombre.strip(),
                                    "ubicacion": nueva_ubicacion.strip(),
                                    "tipo": nuevo_tipo.strip(),
                                    "descripcion": nueva_descripcion.strip(),
                                    "fecha_actualizacion": datetime.now().isoformat()
                                }
                                update_lugar(lugar["_id"], datos_actualizados)
                            
                            show_animated_message("¡Lugar actualizado exitosamente!", "success")
                            
                        except Exception as e:
                            st.error(f"❌ Error al actualizar: {str(e)}")

def delete_lugar_section():
    lugares = get_all_lugares()
    
    if not lugares:
        modern_card("No hay lugares disponibles para eliminar.", "Sin lugares", "😔")
        return
    
    st.subheader("🗑️ Eliminar Lugar")
    
    lugar_options = ["-- Selecciona un lugar --"] + [l.get('nombre', 'Sin nombre') for l in lugares]
    selected_nombre = st.selectbox(
        "🔍 Selecciona el lugar a eliminar",
        lugar_options,
        key="delete_selector"
    )
    
    if selected_nombre != "-- Selecciona un lugar --":
        lugar = next((l for l in lugares if l.get('nombre') == selected_nombre), None)
        
        if lugar:
            st.markdown("""
                <div class="modern-card" style="border-left-color: var(--error);">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 2rem; margin-right: 1rem;">⚠️</span>
                        <h3 style="margin: 0; color: var(--error);">¡Atención! Acción irreversible</h3>
                    </div>
                    <p style="margin-bottom: 1rem; color: var(--dark);">
                        Estás a punto de eliminar permanentemente este lugar. Esta acción no se puede deshacer.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Mostrar información del lugar a eliminar
            modern_card(
                f"""
                **🏠 Nombre:** {lugar.get('nombre', 'N/A')}  
                **📍 Ubicación:** {lugar.get('ubicacion', 'N/A')}  
                **🏷️ Tipo:** {lugar.get('tipo', 'N/A')}  
                **📝 Descripción:** {lugar.get('descripcion', 'N/A')}
                """,
                "Lugar a eliminar",
                "💔"
            )
            
            # Confirmación en dos pasos
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                confirm_delete = modern_button("✅ Sí, eliminar", "confirm_delete", "danger", "🗑️")
            
            with col2:
                cancel_delete = modern_button("❌ Cancelar", "cancel_delete", "primary", "↩️")
            
            if confirm_delete:
                try:
                    with st.spinner("🔄 Eliminando lugar..."):
                        time.sleep(1)
                        delete_lugar(lugar["_id"])
                    
                    show_animated_message("Lugar eliminado exitosamente", "success")
                    
                except Exception as e:
                    st.error(f"❌ Error al eliminar: {str(e)}")

# VISTA PRINCIPAL 
def build_lugar_frame():
    apply_modern_styles()
    
    st.markdown("""
        <div class="fade-in">
            <h1 style="text-align: center; color: var(--primary); margin-bottom: 0;">
                📍 Gestión de Lugares
            </h1>
            <p style="text-align: center; color: #6B7280; margin-top: 0.5rem;">
                Administra y organiza todos los espacios físicos de Frontrack
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Estadísticas rápidas
    lugares = get_all_lugares() or []
    total_lugares = len(lugares)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total de Lugares", total_lugares, delta=None)
    
    with col2:
        tipos = len(set(l.get('tipo', '') for l in lugares))
        st.metric("🏷️ Tipos Diferentes", tipos)
    
    # Navegación con pestañas
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Lista de Lugares", 
        "➕ Crear Nuevo", 
        "✏️ Editar Existente", 
        "🗑️ Eliminar"
    ])
    
    with tab1:
        st.subheader("📋 Lista Completa de Lugares")
        
        if not lugares:
            modern_card(
                "No hay lugares registrados. ¡Comienza agregando el primero!",
                "Sin datos",
                "📭"
            )
        else:
            # Filtros y búsqueda
            col_search, col_filter, col_sort = st.columns([2, 2, 1])
            
            with col_search:
                search_term = st.text_input("🔍 Buscar por nombre", placeholder="Escribe para filtrar...")
            
            with col_filter:
                filter_type = st.selectbox("🏷️ Filtrar por tipo", ["Todos"] + list(set(l.get('tipo', '') for l in lugares)))
            
            # Aplicar filtros
            filtered_lugares = lugares
            if search_term:
                filtered_lugares = [l for l in filtered_lugares if search_term.lower() in l.get('nombre', '').lower()]
            if filter_type != "Todos":
                filtered_lugares = [l for l in filtered_lugares if l.get('tipo') == filter_type]
            
            st.write(f"**Mostrando {len(filtered_lugares)} de {total_lugares} lugares**")
            
            # Mostrar lugares filtrados
            for lugar in filtered_lugares:
                display_lugar_card(lugar)
    
    with tab2:
        create_lugar_form()
    
    with tab3:
        edit_lugar_form()
    
    with tab4:
        delete_lugar_section()

if __name__ == "__main__":
    build_lugar_frame()