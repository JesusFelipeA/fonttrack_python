# frontend/gui/material_window.py

import streamlit as st
import pandas as pd
import time
from datetime import datetime
from backend.controllers.material_controller import (
    get_all_material as get_all_materials,
    create_material,
    update_material,
    delete_material
)

# CONFIGURACIÓN DE ESTILOS MODERNOS CON TOOLTIPS
def apply_material_styles():
    st.markdown("""
        <style>
        /* Paleta de colores para materiales */
        :root {
            --material-primary: #3B82F6;
            --material-secondary: #1D4ED8;
            --material-success: #10B981;
            --material-warning: #F59E0B;
            --material-error: #EF4444;
            --material-dark: #1F2937;
            --material-light: #F9FAFB;
        }
        
        /* Animaciones */
        @keyframes materialFadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .material-fade-in {
            animation: materialFadeIn 0.6s ease-in-out;
        }
        
        /* Tarjetas de materiales */
        .material-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border-left: 5px solid var(--material-primary);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .material-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.15);
        }
        
        .material-card.low-stock {
            border-left-color: var(--material-warning);
            background: linear-gradient(135deg, #FFFBF0, #FFFFFF);
        }
        
        .material-card.out-of-stock {
            border-left-color: var(--material-error);
            background: linear-gradient(135deg, #FEF2F2, #FFFFFF);
        }
        
        /* Botones con tooltips integrados */
        .stButton > button {
            border-radius: 8px;
            border: none;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .btn-material-primary {
            background: linear-gradient(135deg, var(--material-primary), var(--material-secondary)) !important;
            color: white !important;
        }
        
        /* Tooltips personalizados */
        .tooltip-icon {
            display: inline-block;
            width: 18px;
            height: 18px;
            background: var(--material-primary);
            color: white;
            border-radius: 50%;
            text-align: center;
            font-size: 12px;
            font-weight: bold;
            margin-left: 5px;
            cursor: pointer;
            line-height: 18px;
        }
        
        .tooltip-content {
            display: none;
            position: absolute;
            background: var(--material-dark);
            color: white;
            padding: 0.8rem;
            border-radius: 8px;
            font-size: 0.85rem;
            z-index: 1000;
            width: 250px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            animation: materialFadeIn 0.3s ease;
        }
        
        .tooltip-icon:hover + .tooltip-content {
            display: block;
        }
        
        /* Mejoras en formularios */
        .material-form {
            background: #F8FAFC;
            padding: 2rem;
            border-radius: 12px;
            border: 2px dashed #E2E8F0;
        }
        
        .required-field::after {
            content: " *";
            color: var(--material-error);
        }
        
        /* Indicadores de stock */
        .stock-indicator {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-left: 0.5rem;
        }
        
        .stock-high { background: #D1FAE5; color: #065F46; }
        .stock-medium { background: #FEF3C7; color: #92400E; }
        .stock-low { background: #FEE2E2; color: #991B1B; }
        .stock-out { background: #F3F4F6; color: #6B7280; }
        
        /* Métricas destacadas */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
        }
        </style>
        
        <script>
        // Función para mostrar tooltips
        function showTooltip(tooltipId) {
            var tooltip = document.getElementById(tooltipId);
            tooltip.style.display = 'block';
            setTimeout(function() {
                tooltip.style.display = 'none';
            }, 3000);
        }
        </script>
    """, unsafe_allow_html=True)

# COMPONENTES DE AYUDA Y TOOLTIPS
def help_icon(tooltip_text, tooltip_id):
    """Icono de ayuda con tooltip"""
    st.markdown(f"""
        <div style="position: relative; display: inline-block;">
            <span class="tooltip-icon" onclick="showTooltip('{tooltip_id}')">?</span>
            <div class="tooltip-content" id="{tooltip_id}">
                {tooltip_text}
            </div>
        </div>
    """, unsafe_allow_html=True)

def material_tooltip(field_name, help_text):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"<span class='required-field'>{field_name}</span>", unsafe_allow_html=True)
    with col2:
        help_icon(help_text, f"help_{field_name.replace(' ', '_')}")

# COMPONENTES REUTILIZABLES
def modern_material_card(material):
    """Tarjeta moderna para mostrar materiales"""
    existencia = material.get('existencia', 0)
    costo_promedio = material.get('costo_promedio', 0)
    valor_total = existencia * costo_promedio
    
    # Determinar clase de stock
    if existencia == 0:
        stock_class = "out-of-stock"
        stock_indicator = "<span class='stock-indicator stock-out'>SIN STOCK</span>"
    elif existencia <= 10:
        stock_class = "low-stock"
        stock_indicator = f"<span class='stock-indicator stock-low'>{existencia} UNIDADES</span>"
    elif existencia <= 50:
        stock_class = ""
        stock_indicator = f"<span class='stock-indicator stock-medium'>{existencia} UNIDADES</span>"
    else:
        stock_class = ""
        stock_indicator = f"<span class='stock-indicator stock-high'>{existencia} UNIDADES</span>"
    
    st.markdown(f"""
        <div class="material-card {stock_class} material-fade-in">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 0.5rem 0; color: var(--material-dark);">
                        📦 {material.get('descripcion', 'Sin descripción')}
                    </h4>
                    <p style="margin: 0.25rem 0; color: #6B7280;">
                        🔑 <strong>Clave:</strong> {material.get('clave_material', 'N/A')}
                        {stock_indicator}
                    </p>
                    <p style="margin: 0.25rem 0; color: #6B7280;">
                        🏷️ <strong>Clasificación:</strong> {material.get('clasificacion', 'Sin clasificación')}
                    </p>
                    <p style="margin: 0.25rem 0; color: #6B7280;">
                        📊 <strong>Genérico:</strong> {material.get('generico', 'N/A')}
                    </p>
                    <p style="margin: 0.25rem 0; color: #6B7280;">
                        💰 <strong>Costo promedio:</strong> ${costo_promedio:,.2f} | 
                        <strong>Valor total:</strong> ${valor_total:,.2f}
                    </p>
                    <p style="margin: 0.25rem 0; color: #6B7280;">
                        📍 <strong>Lugar ID:</strong> {material.get('lugar_id', 'No asignado')}
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def validate_material_data(clave_material, descripcion, existencia, costo_promedio):
    """Validación comprehensiva de datos del material"""
    errors = []
    
    if not clave_material or len(clave_material.strip()) < 2:
        errors.append("❌ La clave del material debe tener al menos 2 caracteres")
    
    if not descripcion or len(descripcion.strip()) < 5:
        errors.append("❌ La descripción debe ser más específica (mínimo 5 caracteres)")
    
    if existencia < 0:
        errors.append("❌ La existencia no puede ser negativa")
    
    if costo_promedio < 0:
        errors.append("❌ El costo promedio no puede ser negativo")
    
    # Validar formato de clave (puede personalizarse)
    if clave_material and not any(c.isalnum() for c in clave_material):
        errors.append("❌ La clave debe contener letras o números")
    
    return errors

# SECCIONES PRINCIPALES MEJORADAS
def show_material_list():
    materials = get_all_materials()
    
    if not materials:
        st.markdown("""
            <div class="material-card material-fade-in">
                <div style="text-align: center; padding: 2rem;">
                    <h3 style="color: #6B7280;">📭 No hay materiales registrados</h3>
                    <p>Comienza agregando tu primer material usando la pestaña "Crear Nuevo"</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Estadísticas rápidas
    total_materials = len(materials)
    total_value = sum(m.get('existencia', 0) * m.get('costo_promedio', 0) for m in materials)
    low_stock = sum(1 for m in materials if m.get('existencia', 0) <= 10 and m.get('existencia', 0) > 0)
    out_of_stock = sum(1 for m in materials if m.get('existencia', 0) == 0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Total Materiales", total_materials)
    with col2:
        st.metric("💰 Valor Total", f"${total_value:,.2f}")
    with col3:
        st.metric("⚠️ Stock Bajo", low_stock)
    with col4:
        st.metric("🚨 Sin Stock", out_of_stock)
    
    # Filtros y búsqueda
    st.markdown("---")
    col_search, col_filter, col_sort = st.columns([2, 2, 1])
    
    with col_search:
        search_term = st.text_input("🔍 Buscar materiales...", placeholder="Por descripción o clave")
    
    with col_filter:
        clasificaciones = ["Todas"] + list(set(m.get('clasificacion', '') for m in materials if m.get('clasificacion')))
        filter_class = st.selectbox("🏷️ Filtrar por clasificación", clasificaciones)
    
    with col_sort:
        sort_option = st.selectbox("📊 Ordenar por", ["Existencia ↓", "Existencia ↑", "Valor ↓", "Valor ↑", "Nombre A-Z"])
    
    # Aplicar filtros
    filtered_materials = materials
    if search_term:
        filtered_materials = [m for m in filtered_materials 
                            if search_term.lower() in m.get('descripcion', '').lower() 
                            or search_term.lower() in m.get('clave_material', '').lower()]
    
    if filter_class != "Todas":
        filtered_materials = [m for m in filtered_materials if m.get('clasificacion') == filter_class]
    
    # Aplicar ordenamiento
    if sort_option == "Existencia ↓":
        filtered_materials.sort(key=lambda x: x.get('existencia', 0), reverse=True)
    elif sort_option == "Existencia ↑":
        filtered_materials.sort(key=lambda x: x.get('existencia', 0))
    elif sort_option == "Valor ↓":
        filtered_materials.sort(key=lambda x: x.get('existencia', 0) * x.get('costo_promedio', 0), reverse=True)
    elif sort_option == "Valor ↑":
        filtered_materials.sort(key=lambda x: x.get('existencia', 0) * x.get('costo_promedio', 0))
    elif sort_option == "Nombre A-Z":
        filtered_materials.sort(key=lambda x: x.get('descripcion', '').lower())
    
    st.write(f"**Mostrando {len(filtered_materials)} de {total_materials} materiales**")
    
    # Mostrar materiales
    for material in filtered_materials:
        modern_material_card(material)

def create_material_section():
    st.subheader("➕ Crear Nuevo Material")
    
    with st.form("create_material_form", clear_on_submit=True):
        st.markdown('<div class="material-form">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            material_tooltip(
                "Clave del material", 
                "Identificador único del material. Usa un formato consistente como 'MAT-001'"
            )
            clave_material = st.text_input(
                "Clave del material",
                placeholder="Ej: MAT-001, HER-2024",
                label_visibility="collapsed"
            )
            
            material_tooltip(
                "Descripción del material",
                "Nombre completo y descriptivo del material. Sé específico para fácil identificación"
            )
            descripcion = st.text_input(
                "Descripción del material", 
                placeholder="Ej: Tornillo hexagonal acero inoxidable 5mm",
                label_visibility="collapsed"
            )
            
            material_tooltip(
                "Clasificación",
                "Categoría del material para organización (Ej: Herramientas, Electricidad, Fontanería)"
            )
            clasificacion = st.selectbox(
                "Clasificación",
                ["", "Herramientas", "Electricidad", "Fontanería", "Construcción", "Oficina", "Limpieza", "Otro"],
                label_visibility="collapsed"
            )
            
            if clasificacion == "Otro":
                clasificacion = st.text_input("Especifica la clasificación")
        
        with col2:
            material_tooltip(
                "Genérico",
                "Tipo genérico del material (Ej: Tornillo, Cable, Llave)"
            )
            generico = st.text_input(
                "Genérico",
                placeholder="Ej: Tornillo, Cable, Llave inglesa",
                label_visibility="collapsed"
            )
            
            material_tooltip(
                "Existencia inicial",
                "Cantidad disponible al momento de crear el material. Puede ser 0"
            )
            existencia = st.number_input(
                "Existencia inicial", 
                min_value=0, 
                step=1,
                value=0,
                label_visibility="collapsed"
            )
            
            material_tooltip(
                "Costo promedio",
                "Costo unitario promedio del material. Incluye dos decimales para precisión"
            )
            costo_promedio = st.number_input(
                "Costo promedio", 
                min_value=0.0, 
                step=0.01,
                format="%.2f",
                label_visibility="collapsed"
            )
            
            material_tooltip(
                "ID del lugar",
                "Identificador del lugar donde se almacena el material. Debe coincidir con un lugar existente"
            )
            lugar_id = st.text_input(
                "ID del lugar",
                placeholder="Ej: 12345abcde",
                label_visibility="collapsed"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botón de envío
        col_submit, col_help = st.columns([1, 3])
        with col_submit:
                submitted = st.form_submit_button("💾 Guardar Material", use_container_width=True)
        
        with col_help:
            st.caption("💡 Todos los campos marcados con * son obligatorios")
        
        if submitted:
            errors = validate_material_data(clave_material, descripcion, existencia, costo_promedio)
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                try:
                    with st.spinner("🔄 Guardando material..."):
                        time.sleep(1)
                        nuevo_material = {
                            "clave_material": clave_material.strip(),
                            "descripcion": descripcion.strip(),
                            "generico": generico.strip(),
                            "clasificacion": clasificacion.strip(),
                            "existencia": existencia,
                            "costo_promedio": round(costo_promedio, 2),
                            "lugar_id": lugar_id.strip(),
                            "fecha_creacion": datetime.now().isoformat()
                        }
                        create_material(nuevo_material)
                    
                    st.success("🎉 ¡Material creado exitosamente!")
                    time.sleep(2)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error al crear el material: {str(e)}")


def edit_material_section():
    """Sección moderna para editar materiales con tooltips y refresco automático"""
    st.subheader("✏️ Editar Material Existente")

    # Inicializar estado de refresco si no existe
    if "refrescar_edicion" not in st.session_state:
        st.session_state.refrescar_edicion = False

    # Si se activó el refresco, reiniciar estado y detener ejecución para forzar recarga
    if st.session_state.refrescar_edicion:
        st.session_state.refrescar_edicion = False
        st.stop()

    materials = get_all_materials()

    if not materials:
        st.markdown("""
            <div class="material-card material-fade-in">
                <div style="text-align: center; padding: 2rem;">
                    <h3 style="color: #6B7280;">📭 No hay materiales para editar</h3>
                    <p>Primero crea algunos materiales en la pestaña "Crear Nuevo"</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("### 🔍 Seleccionar Material a Editar")
    material_options = ["-- Selecciona un material --"] + [
        m.get('descripcion', 'Sin descripción') for m in materials
    ]

    selected_desc = st.selectbox(
        "Material a editar",
        material_options,
        key="edit_material_selector"
    )

    if selected_desc != "-- Selecciona un material --":
        material = next((m for m in materials if m.get('descripcion') == selected_desc), None)

        if material:
            st.markdown("### 📋 Información Actual del Material")
            modern_material_card(material)

            st.markdown("---")
            st.markdown("### ✨ Editar Información")

            with st.form("edit_material_form"):
                st.markdown('<div class="material-form">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)

                with col1:
                    material_tooltip("Clave del material", "Identificador único.")
                    nueva_clave = st.text_input("Clave del material", value=material.get('clave_material', ''), label_visibility="collapsed")

                    material_tooltip("Descripción del material", "Nombre descriptivo.")
                    nueva_descripcion = st.text_input("Descripción del material", value=material.get('descripcion', ''), label_visibility="collapsed")

                    material_tooltip("Clasificación", "Categoría del material.")
                    clasificacion_actual = material.get('clasificacion', '')
                    opciones_clasificacion = ["Herramientas", "Electricidad", "Fontanería", "Construcción", "Oficina", "Limpieza", "Otro"]
                    index_actual = opciones_clasificacion.index(clasificacion_actual) if clasificacion_actual in opciones_clasificacion else 0
                    nueva_clasificacion = st.selectbox("Clasificación", options=opciones_clasificacion, index=index_actual, label_visibility="collapsed")

                    if nueva_clasificacion == "Otro" and clasificacion_actual not in opciones_clasificacion:
                        nueva_clasificacion = st.text_input("Especifica clasificación", value=clasificacion_actual)

                with col2:
                    material_tooltip("Genérico", "Tipo genérico del material.")
                    nuevo_generico = st.text_input("Genérico", value=material.get('generico', ''), label_visibility="collapsed")

                    material_tooltip("Existencia en stock", "Cantidad disponible.")
                    nueva_existencia = st.number_input("Existencia", min_value=0, step=1, value=int(material.get('existencia', 0)), label_visibility="collapsed")

                    material_tooltip("Costo promedio unitario", "Costo por unidad.")
                    nuevo_costo = st.number_input("Costo promedio", min_value=0.0, step=0.01, value=float(material.get('costo_promedio', 0.0)), format="%.2f", label_visibility="collapsed")

                    material_tooltip("ID del lugar de almacenamiento", "Identificador del lugar.")
                    nuevo_lugar = st.text_input("ID del lugar", value=material.get('lugar_id', ''), label_visibility="collapsed")

                st.markdown('</div>', unsafe_allow_html=True)

                col_submit, col_reset, col_help = st.columns([1, 1, 2])
                submitted = col_submit.form_submit_button("🔄 Actualizar Material", use_container_width=True)
                reset_clicked = col_reset.form_submit_button("↩️ Restablecer", use_container_width=True)
                col_help.caption("💡 Modifica solo los campos necesarios")

            if reset_clicked:
                st.session_state.refrescar_edicion = True
                st.stop()

            if submitted:
                errors = validate_material_data(nueva_clave, nueva_descripcion, nueva_existencia, nuevo_costo)

                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    try:
                        with st.spinner("🔄 Actualizando material..."):
                            time.sleep(1)
                            datos_actualizados = {
                                "clave_material": nueva_clave.strip(),
                                "descripcion": nueva_descripcion.strip(),
                                "generico": nuevo_generico.strip(),
                                "clasificacion": nueva_clasificacion.strip(),
                                "existencia": nueva_existencia,
                                "costo_promedio": round(nuevo_costo, 2),
                                "lugar_id": nuevo_lugar.strip(),
                                "fecha_actualizacion": datetime.now().isoformat(),
                            }
                            update_material(material["_id"], datos_actualizados)

                        st.success("🎉 ¡Material actualizado exitosamente!")
                        with st.expander("📊 Resumen de cambios", expanded=True):
                            col_old, col_new = st.columns(2)
                            with col_old:
                                st.markdown("**Valores anteriores:**")
                                st.write(f"**Clave:** {material.get('clave_material', 'N/A')}")
                                st.write(f"**Descripción:** {material.get('descripcion', 'N/A')}")
                                st.write(f"**Existencia:** {material.get('existencia', 0)}")
                                st.write(f"**Costo:** ${material.get('costo_promedio', 0):.2f}")
                            with col_new:
                                st.markdown("**Nuevos valores:**")
                                st.write(f"**Clave:** {nueva_clave}")
                                st.write(f"**Descripción:** {nueva_descripcion}")
                                st.write(f"**Existencia:** {nueva_existencia}")
                                st.write(f"**Costo:** ${nuevo_costo:.2f}")

                        time.sleep(2)
                        st.session_state.refrescar_edicion = True
                        st.stop()

                    except Exception as e:
                        st.error(f"❌ Error al actualizar material: {str(e)}")
def delete_material_section():
    st.subheader("🗑️ Eliminar Material")
    
    materials = get_all_materials()
    
    if not materials:
        st.markdown("""
            <div class="material-card material-fade-in">
                <div style="text-align: center; padding: 2rem;">
                    <h3 style="color: #6B7280;">📭 No hay materiales para eliminar</h3>
                    <p>No hay materiales registrados en el sistema</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        return

    # Selector de materiales
    st.markdown("### 🔍 Seleccionar Material a Eliminar")
    material_options = ["-- Selecciona un material --"] + [m.get('descripcion', 'Sin descripción') for m in materials]
    selected_desc = st.selectbox(
        "Material a eliminar",
        material_options,
        key="delete_material_selector"
    )
    
    if selected_desc != "-- Selecciona un material --":
        material = next((m for m in materials if m.get('descripcion') == selected_desc), None)
        
        if material:
            # Tarjeta de advertencia con animación
            st.markdown("""
                <div class="material-card material-fade-in" style="border-left-color: var(--material-error); background: linear-gradient(135deg, #FEF2F2, #FFFFFF);">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 2rem; margin-right: 1rem;">⚠️</span>
                        <div>
                            <h3 style="margin: 0; color: var(--material-error);">¡Atención! Acción Crítica</h3>
                            <p style="margin: 0; color: #6B7280;">Esta acción no se puede deshacer</p>
                        </div>
                    </div>
                    <p style="margin: 0; color: var(--material-dark);">
                        Estás a punto de eliminar permanentemente este material del sistema. 
                        Todos los datos asociados se perderán irreversiblemente.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📋 Material Seleccionado para Eliminación")
            modern_material_card(material)
            
            # Mostrar impacto de la eliminación
            existencia = material.get('existencia', 0)
            costo_promedio = material.get('costo_promedio', 0)
            valor_total = existencia * costo_promedio
            
            st.markdown("""
                <div class="material-card" style="background: #FFFBEB; border-left-color: #F59E0B;">
                    <h4 style="color: #92400E; margin-bottom: 1rem;">📊 Impacto de la Eliminación</h4>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🔢 Existencia a Perder", existencia)
            with col2:
                st.metric("💰 Valor Inventario", f"${valor_total:,.2f}")
            with col3:
                st.metric("📅 Última Actualización", "Permanente")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Sistema de confirmación en dos pasos
            st.markdown("### 🔒 Confirmación de Eliminación")
            
            st.warning("**Paso 1:** Marca la casilla para confirmar que entiendes las consecuencias")
            confirm_understanding = st.checkbox(
                "✅ Comprendo que esta acción es permanente e irreversible"
            )
            
            if existencia > 0:
                st.error("**Paso 2:** Este material tiene existencias en inventario")
                confirm_stock_loss = st.checkbox(
                    f"✅ Comprendo que se perderán {existencia} unidades valoradas en ${valor_total:,.2f}"
                )
                confirmation_required = confirm_understanding and confirm_stock_loss
            else:
                confirmation_required = confirm_understanding
            
            if confirmation_required:
                st.error("**Paso 3:** Verificación final")
                st.write(f"Escribe el nombre del material para confirmar: **{selected_desc}**")
                confirm_name = st.text_input(
                    "Escribe el nombre exacto del material:",
                    placeholder="Copie y pegue el nombre mostrado arriba"
                )
                
                final_confirmation = confirm_name.strip() == selected_desc
            else:
                final_confirmation = False
            
            # Botones de acción
            st.markdown("---")
            col_delete, col_cancel, col_spacer = st.columns([1, 1, 2])
            
            with col_delete:
                delete_disabled = not (confirmation_required and final_confirmation)
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
            
            # Ejecutar eliminación si está confirmada
            if delete_clicked and final_confirmation:
                try:
                    with st.spinner("🔄 Eliminando material..."):
                        # Simular proceso de eliminación
                        time.sleep(2)
                        
                        # Guardar información para el mensaje de confirmación
                        material_info = {
                            'nombre': selected_desc,
                            'existencia': existencia,
                            'valor': valor_total
                        }
                        
                        # Ejecutar eliminación
                        delete_material(material["_id"])
                    
                    # Mensaje de confirmación con detalles
                    st.markdown("""
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #D1FAE5, #A7F3D0); border-radius: 12px;">
                            <h2 style="color: #065F46;">🎉 Material Eliminado Exitosamente</h2>
                    """, unsafe_allow_html=True)
                    
                    col_success1, col_success2, col_success3 = st.columns(3)
                    
                    with col_success1:
                        st.metric("📦 Material", selected_desc)
                    with col_success2:
                        st.metric("🔢 Existencia Eliminada", existencia)
                    with col_success3:
                        st.metric("💰 Valor Perdido", f"${valor_total:,.2f}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Recomendación
                    st.info("""
                        **💡 Recomendación:** Considera realizar un backup regular de tu inventario 
                        para prevenir pérdidas accidentales de información importante.
                    """)
                    
                    time.sleep(3)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error al eliminar el material: {str(e)}")
                    st.info("""
                        **🛠️ Solución:** 
                        - Verifica que el material no esté siendo usado en transacciones activas
                        - Revisa la conexión con la base de datos
                        - Contacta al administrador del sistema si el problema persiste
                    """)

# VISTA PRINCIPAL MODERNA
def build_material_frame():
    apply_material_styles()
    
    st.markdown("""
        <div class="material-fade-in">
            <h1 style="text-align: center; color: var(--material-primary); margin-bottom: 0;">
                📦 Gestión de Materiales
            </h1>
            <p style="text-align: center; color: #6B7280; margin-top: 0.5rem;">
                Administra tu inventario de manera eficiente y organizada
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Navegación con pestañas
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Lista de Materiales", 
        "➕ Crear Nuevo", 
        "✏️ Editar Existente", 
        "🗑️ Eliminar"
    ])
    
    with tab1:
        show_material_list()
    
    with tab2:
        create_material_section()
    
    with tab3:
        edit_material_section()

    with tab4:
        delete_material_section()

if __name__ == "__main__":
    build_material_frame()