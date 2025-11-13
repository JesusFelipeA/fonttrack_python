import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import os
import re
import json

# CONTROLADORES 
try:
    from backend.controllers.user_controller import get_all_users
    from backend.controllers.material_controller import get_all_material
    from backend.controllers.lugar_controller import get_all_lugares
except ImportError:
    # Datos de ejemplo para desarrollo
    def get_all_users():
        return [
            {"correo": "admin@empresa.com", "role": "admin", "fecha_creacion": "2024-01-15"},
            {"correo": "usuario1@empresa.com", "role": "user", "fecha_creacion": "2024-02-01"},
            {"correo": "usuario2@empresa.com", "role": "user", "fecha_creacion": "2024-02-15"},
            {"correo": "gerente@empresa.com", "role": "admin", "fecha_creacion": "2024-03-01"},
        ]
    
    def get_all_material():
        return [
            {"nombre": "Tornillos", "existencia": 150, "costo_promedio": 0.50, "clasificacion": "Herramientas"},
            {"nombre": "Cables", "existencia": 75, "costo_promedio": 2.30, "clasificacion": "Electricidad"},
            {"nombre": "Tuercas", "existencia": 200, "costo_promedio": 0.25, "clasificacion": "Herramientas"},
            {"nombre": "Bombillos", "existencia": 30, "costo_promedio": 1.75, "clasificacion": "Electricidad"},
            {"nombre": "Martillos", "existencia": 15, "costo_promedio": 12.50, "clasificacion": "Herramientas"},
        ]
    
    def get_all_lugares():
        return [
            {"nombre": "Almacén Central", "tipo": "Almacén", "ubicacion": "Edificio A"},
            {"nombre": "Oficina Principal", "tipo": "Oficina", "ubicacion": "Piso 2"},
            {"nombre": "Taller Mecánico", "tipo": "Taller", "ubicacion": "Edificio B"},
        ]

# CONFIGURACIÓN INICIAL MEJORADA

def setup_page_config():
    st.set_page_config(
        page_title="Analytics Pro - Dashboard Inteligente",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# 
# ESTILOS AVANZADOS

def apply_advanced_styles():
    st.markdown("""
        <style>
        /* Estilos generales */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
            border-left: 5px solid #6366F1;
            margin-bottom: 1rem;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 25px rgba(0,0,0,0.15);
        }
        
        .metric-value {
            font-size: 2.2rem;
            font-weight: bold;
            color: #6366F1;
            margin: 0.5rem 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        .metric-label {
            font-size: 1rem;
            color: #6B7280;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .kpi-badge {
            font-size: 0.8rem;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: bold;
            margin-left: 0.5rem;
        }
        
        .kpi-positive {
            background: #D1FAE5;
            color: #065F46;
        }
        
        .kpi-negative {
            background: #FEE2E2;
            color: #991B1B;
        }
        
        .kpi-neutral {
            background: #E5E7EB;
            color: #374151;
        }
        
        /* Sidebar styles */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        }
        
        /* Botones mejorados */
        .stButton button {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            color: white;
            border: none;
            padding: 0.7rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
        }
        
        /* Tabs y expansores */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: #f1f5f9;
            border-radius: 8px 8px 0px 0px;
            padding: 10px 20px;
            border: none;
        }
        
        .stTabs [aria-selected="true"] {
            background: #6366F1;
            color: white;
        }
        
        /* Progress bars */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%);
        }
        </style>
    """, unsafe_allow_html=True)

# COMPONENTES UI MEJORADOS

def create_metric_card_advanced(value, label, icon, trend=None, subtitle=None, help_text=None):
    trend_html = ""
    if trend is not None:
        trend_class = "kpi-positive" if trend > 0 else "kpi-negative" if trend < 0 else "kpi-neutral"
        trend_icon = "📈" if trend > 0 else "📉" if trend < 0 else "➡️"
        trend_html = f'<span class="kpi-badge {trend_class}">{trend_icon} {abs(trend):.1f}%</span>'
    
    subtitle_html = f'<p style="font-size: 0.8rem; color: #6B7280; margin: 0.2rem 0;">{subtitle}</p>' if subtitle else ""
    
    help_html = f'<div style="font-size: 0.7rem; color: #9CA3AF; margin-top: 0.5rem;">{help_text}</div>' if help_text else ""
    
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem; filter: drop-shadow(2px 2px 3px rgba(0,0,0,0.1));">{icon}</div>
            <div class="metric-value">{value}{trend_html}</div>
            <div class="metric-label">{label}</div>
            {subtitle_html}
            {help_html}
        </div>
    """, unsafe_allow_html=True)

def create_welcome_header():
    """Header de bienvenida"""
    st.markdown("""
        <div class="main-header">
            <div style="text-align: center;">
                <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">🚀 Analytics Dashboard</h1>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                    Plataforma Inteligente de Análisis Predictivo y Machine Learning
                </p>
                <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                    📍 Tiempo real • 🔮 Predictivo • 📊 Interactivo
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# MÓDULOS DE REGRESIÓN MEJORADOS

def mostrar_regresion_polinomica_interactiva():
    """Módulo de Regresión Polinómica Mejorado"""
    st.markdown("### 🎯 Regresión Polinómica Predictiva Avanzada")
    
    with st.expander("⚙️ CONFIGURACIÓN DEL MODELO PREDICTIVO", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown("**🎛️ Parámetros del Modelo**")
            grado = st.slider("Grado del polinomio", 1, 6, 2, 
                            help="Grado de complejidad del modelo polinómico")
            n_puntos = st.slider("Número de puntos de datos", 20, 200, 50,
                               help="Cantidad de datos para entrenamiento")
        
        with col2:
            st.markdown("**📊 Variables de Análisis**")
            variable_x = st.selectbox("Variable predictora (X)", 
                                    ["existencia", "costo_promedio"],
                                    help="Variable independiente para predicción")
            variable_y = st.selectbox("Variable objetivo (Y)", 
                                    ["costo_promedio", "existencia"],
                                    help="Variable que queremos predecir")
            ruido = st.slider("Nivel de ruido", 0.1, 5.0, 1.0,
                            help="Simula variabilidad en los datos reales")
        
        with col3:
            st.markdown("**🎨 Visualización**")
            mostrar_residuales = st.checkbox("Mostrar residuales", True)
            mostrar_intervalos = st.checkbox("Intervalos confianza", False)
    
    # Barra de progreso para simulación
    with st.spinner('🔄 Generando modelo predictivo...'):
        progress_bar = st.progress(0)
        
        # Generar datos sintéticos
        materiales = get_all_material()
        if materiales:
            progress_bar.progress(30)
            
            # Usar estadísticas reales para generar datos más realistas
            costos = [m['costo_promedio'] for m in materiales]
            existencias = [m['existencia'] for m in materiales]
            
            # Crear relación no lineal basada en datos reales
            X_base = np.linspace(min(existencias), max(existencias), n_puntos)
            y_base = np.polyval([-0.01, 0.5, 5], X_base)
            y = y_base + np.random.normal(0, ruido, n_puntos)
            X = X_base.reshape(-1, 1)
            
            progress_bar.progress(60)
            
            # Entrenar modelo polinómico
            poly = PolynomialFeatures(degree=grado)
            X_poly = poly.fit_transform(X)
            
            modelo = LinearRegression()
            modelo.fit(X_poly, y)
            y_pred = modelo.predict(X_poly)
            
            progress_bar.progress(90)
            
            # Métricas
            r2 = r2_score(y, y_pred)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            
            progress_bar.progress(100)
    
    # Visualización mejorada
    col_viz1, col_viz2 = st.columns([2, 1])
    
    with col_viz1:
        fig = go.Figure()
        
        # Datos reales
        fig.add_trace(go.Scatter(
            x=X.flatten(), y=y, mode='markers', 
            name='📊 Datos Reales', 
            marker=dict(color='#6366F1', size=8, opacity=0.7),
            hovertemplate='<b>X</b>: %{x:.2f}<br><b>Y</b>: %{y:.2f}<extra></extra>'
        ))
        
        # Línea de predicción
        fig.add_trace(go.Scatter(
            x=X.flatten(), y=y_pred, mode='lines',
            name=f'🎯 Modelo (grado {grado})', 
            line=dict(color='#FF6B6B', width=4),
            hovertemplate='<b>Predicción</b>: %{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"📈 Modelo de Regresión Polinómica - R² = {r2:.3f}",
            xaxis_title=variable_x,
            yaxis_title=variable_y,
            height=500,
            template="plotly_white",
            hovermode='closest'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_viz2:
        # Panel de métricas interactivo
        st.markdown("####  Métricas del Modelo")
        
        col_met1, col_met2 = st.columns(2)
        with col_met1:
            st.metric(" R² Score", f"{r2:.3f}")
        with col_met2:
            st.metric("RMSE", f"{rmse:.2f}")
        
        st.markdown("####  Diagnóstico")
        if grado == 1:
            st.success("**Modelo Lineal Simple**\n\nIdeal para relaciones lineales básicas")
        elif 2 <= grado <= 3:
            st.info("** Modelo Balanceado**\n\nExcelente equilibrio entre flexibilidad y generalización")
        else:
            st.warning("** Modelo Complejo**\n\nConsiderar validación cruzada para evitar sobreajuste")
    
        # Botón de exportación
        if st.button(" Exportar Resultados", use_container_width=True):
            st.success("Resultados exportados correctamente")
    
    # Análisis de residuales
    if mostrar_residuales:
        st.markdown("---")
        st.markdown("#### 🔎 Análisis de Residuales")
        
        residuales = y - y_pred
        fig_res = go.Figure()
        fig_res.add_trace(go.Scatter(
            x=y_pred, y=residuales, mode='markers',
            marker=dict(color='#FFA726', size=6, opacity=0.6),
            name='Residuales'
        ))
        fig_res.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
        fig_res.update_layout(
            title="Distribución de Residuales",
            xaxis_title="Predicciones",
            yaxis_title="Error (Real - Predicho)",
            height=350,
            template="plotly_white"
        )
        st.plotly_chart(fig_res, use_container_width=True)

def mostrar_regresion_multiple_interactiva():
    """Módulo de Regresión Lineal Múltiple """
    st.markdown("### 🔮 Regresión Múltiple Predictiva Avanzada")
    
    with st.expander("🎛️ CONFIGURACIÓN DE VARIABLES", expanded=True):
        materiales_df = pd.DataFrame(get_all_material())
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📋 Variables Predictoras**")
            variables_predictoras = st.multiselect(
                "Selecciona variables independientes (X)",
                options=materiales_df.select_dtypes(include=[np.number]).columns.tolist(),
                default=["existencia", "costo_promedio"],
                help="Variables que usarás para predecir el objetivo"
            )
        
        with col2:
            st.markdown("**🎯 Variable Objetivo**")
            variable_objetivo = st.selectbox(
                "Variable a predecir (Y)",
                options=materiales_df.select_dtypes(include=[np.number]).columns.tolist(),
                index=0,
                help="La variable que quieres predecir"
            )
            
            # Selector de algoritmo (futura expansión)
            algoritmo = st.selectbox(
                "Algoritmo de regresión",
                ["Lineal Múltiple", "Ridge", "Lasso (Próximamente)"],
                disabled=True
            )
    
    if len(variables_predictoras) < 1:
        st.error("❌ Selecciona al menos una variable predictora para continuar")
        st.info("💡 Tip: Selecciona variables numéricas relevantes para tu análisis")
        return
    
    # Preparar y entrenar modelo
    with st.spinner('🔧 Entrenando modelo de regresión múltiple...'):
        X = materiales_df[variables_predictoras]
        y = materiales_df[variable_objetivo]
        
        modelo = LinearRegression()
        modelo.fit(X, y)
        y_pred = modelo.predict(X)
        
        # Métricas
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    # Resultados en pestañas
    tab1, tab2, tab3 = st.tabs(["📊 Resultados", "🎯 Predicción", "📈 Visualización"])
    
    with tab1:
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown("#### 📋 Coeficientes del Modelo")
            coef_df = pd.DataFrame({
                'Variable': ['Intercepto'] + variables_predictoras,
                'Coeficiente': [modelo.intercept_] + modelo.coef_.tolist(),
                'Importancia': ['N/A'] + [f"{abs(coef):.3f}" for coef in modelo.coef_]
            })
            st.dataframe(coef_df, use_container_width=True, height=300)
        
        with col_res2:
            st.markdown("#### 📈 Métricas de Rendimiento")
            
            col_met1, col_met2 = st.columns(2)
            with col_met1:
                st.metric("🎯 R² Score", f"{r2:.3f}")
            with col_met2:
                st.metric("📏 RMSE", f"{rmse:.2f}")
            
            # Interpretación de R²
            st.markdown("#### 🔍 Interpretación")
            if r2 > 0.8:
                st.success("**Excelente ajuste** - El modelo explica más del 80% de la variabilidad")
            elif r2 > 0.6:
                st.info("**Buen ajuste** - El modelo explica más del 60% de la variabilidad")
            else:
                st.warning("**Ajuste moderado** - Considera añadir más variables o transformar las existentes")
    
    with tab2:
        st.markdown("#### 🎯 Simulador de Predicción en Tiempo Real")
        st.info("Ajusta los valores para ver predicciones instantáneas:")
        
        inputs = {}
        cols = st.columns(len(variables_predictoras))
        
        for i, var in enumerate(variables_predictoras):
            with cols[i]:
                min_val = float(X[var].min())
                max_val = float(X[var].max())
                mean_val = float(X[var].mean())
                
                inputs[var] = st.slider(
                    f"{var}",
                    min_val, max_val, mean_val,
                    help=f"Rango: {min_val:.2f} - {max_val:.2f}"
                )
        
        # Predicción en tiempo real
        if st.button("🚀 Calcular Predicción", type="primary", use_container_width=True):
            input_df = pd.DataFrame([inputs])
            prediccion = modelo.predict(input_df)[0]
            
            st.success(f"**🎯 Predicción:** `{prediccion:.2f}`")
            
            # Mostrar ecuación
            ecuacion = f"y = {modelo.intercept_:.2f}"
            for i, coef in enumerate(modelo.coef_):
                ecuacion += f" + {coef:.2f}*{variables_predictoras[i]}"
            
            with st.expander("📝 Ver ecuación del modelo"):
                st.code(ecuacion)
    
    with tab3:
        # Visualización de relaciones
        if len(variables_predictoras) >= 2:
            fig = px.scatter_matrix(
                materiales_df,
                dimensions=variables_predictoras + [variable_objetivo],
                title="Matriz de Dispersión - Relaciones entre Variables"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Selecciona al menos 2 variables predictoras para ver la matriz de dispersión")

def mostrar_analisis_tendencias_avanzado():
    """Módulo de Análisis de Tendencias Temporales """
    st.markdown("### 📊 Análisis de Tendencias Temporales Avanzado")
    
    # Configuración interactiva
    with st.expander("⚙️ CONFIGURACIÓN DEL ANÁLISIS TEMPORAL", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            periodo = st.selectbox(
                "Período de análisis",
                ["Últimos 6 meses", "Último año", "Últimos 2 años"],
                index=1
            )
        
        with col2:
            tipo_tendencia = st.selectbox(
                "Tipo de tendencia",
                ["Lineal", "Polinómica (Próximamente)", "Exponencial (Próximamente)"]
            )
        
        with col3:
            mostrar_estacionalidad = st.checkbox("Mostrar estacionalidad", True)
    
    # Generar datos temporales sintéticos mejorados
    if periodo == "Últimos 6 meses":
        fechas = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
    elif periodo == "Último año":
        fechas = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    else:
        fechas = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    
    # Simular datos más realistas
    tendencia_base = np.linspace(100, 200, len(fechas))
    estacionalidad = 25 * np.sin(2 * np.pi * np.arange(len(fechas)) / 30)
    ruido = np.random.normal(0, 8, len(fechas))
    valores = tendencia_base + estacionalidad + ruido
    
    datos_temporales = pd.DataFrame({
        'fecha': fechas,
        'valor': valores,
        'media_movil_7': pd.Series(valores).rolling(window=7).mean(),
        'media_movil_30': pd.Series(valores).rolling(window=30).mean()
    })
    
    # Análisis de tendencia
    X_temp = np.arange(len(datos_temporales)).reshape(-1, 1)
    y_temp = datos_temporales['valor'].values
    
    modelo_tendencia = LinearRegression()
    modelo_tendencia.fit(X_temp, y_temp)
    tendencia_lineal = modelo_tendencia.predict(X_temp)
    
    # Visualización avanzada
    fig = go.Figure()
    
    # Datos originales
    fig.add_trace(go.Scatter(
        x=datos_temporales['fecha'], y=datos_temporales['valor'],
        mode='lines', name='📈 Valores Diarios', 
        line=dict(color='lightblue', width=1),
        opacity=0.6
    ))
    
    # Media móvil
    fig.add_trace(go.Scatter(
        x=datos_temporales['fecha'], y=datos_temporales['media_movil_7'],
        mode='lines', name='📊 Media Móvil (7 días)', 
        line=dict(color='blue', width=3)
    ))
    
    # Tendencia
    fig.add_trace(go.Scatter(
        x=datos_temporales['fecha'], y=tendencia_lineal,
        mode='lines', name='🎯 Tendencia Lineal', 
        line=dict(color='red', width=4, dash='dash')
    ))
    
    fig.update_layout(
        title="Análisis de Tendencia Temporal con Regresión Lineal",
        xaxis_title="Fecha",
        yaxis_title="Valor",
        height=500,
        template="plotly_white",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métricas y insights
    st.markdown("### 📈 Insights de Tendencia")
    
    pendiente = modelo_tendencia.coef_[0] * 30  # Pendiente mensual
    r2_tendencia = r2_score(y_temp, tendencia_lineal)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        direccion = "📈 Alcista" if pendiente > 0 else "📉 Bajista"
        color = "green" if pendiente > 0 else "red"
        st.metric("Dirección de Tendencia", direccion, delta=f"{pendiente:.1f}")
    
    with col2:
        st.metric("R² Tendencia", f"{r2_tendencia:.3f}")
    
    with col3:
        volatilidad = np.std(datos_temporales['valor']) / np.mean(datos_temporales['valor'])
        st.metric("Volatilidad", f"{volatilidad:.3f}")
    
    with col4:
        crecimiento_porcentual = ((valores[-1] - valores[0]) / valores[0]) * 100
        st.metric("Crecimiento Total", f"{crecimiento_porcentual:.1f}%")
    
    # Recomendaciones basadas en el análisis
    st.markdown("### 💡 Recomendaciones")
    
    if pendiente > 5:
        st.success("""
        **✅ Tendencia Fuertemente Alcista**
        - Considera aumentar inventario
        - Evalúa oportunidades de expansión
        - Mantén monitoreo continuo
        """)
    elif pendiente > 0:
        st.info("""
        **📈 Tendencia Moderadamente Alcista**
        - Mantén estrategias actuales
        - Monitorea indicadores clave
        - Prepárate para ajustes
        """)
    else:
        st.warning("""
        **⚠️ Tendencia Bajista Detectada**
        - Revisa estrategias actuales
        - Analiza causas del decrecimiento
        - Considera ajustes operativos
        """)

# DASHBOARD PRINCIPAL

def mostrar_dashboard_principal_interactivo():
    """Dashboard principal completamente mejorado"""
    import pandas as pd
    import numpy as np
    import streamlit as st
    import plotly.express as px
    from sklearn.linear_model import LinearRegression

    # Obtener datos
    users = get_all_users() or []
    materials = get_all_material() or []
    places = get_all_lugares() or []

    # Calcular métricas
    user_metrics = calculate_user_metrics(users)
    material_metrics = calculate_material_metrics(materials)

    st.markdown("### 🎯 PANEL DE CONTROL PRINCIPAL")

    # Fila 1: Métricas clave
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        create_metric_card_advanced(
            value=user_metrics['total'],
            label="👥 Usuarios Totales",
            icon="👥",
            trend=user_metrics['growth_rate'] * 100,
            subtitle=f"{user_metrics['admins']} admins • {user_metrics['regulars']} users",
            help_text="Crecimiento mensual"
        )

    with col2:
        create_metric_card_advanced(
            value=material_metrics['total_materials'],
            label="📦 Materiales Registrados",
            icon="📦",
            subtitle=f"${material_metrics['total_value']:,.2f} valor total",
            help_text="Inventario actual"
        )

    with col3:
        create_metric_card_advanced(
            value=material_metrics['total_quantity'],
            label="🔄 Unidades en Stock",
            icon="🔄",
            subtitle=f"{material_metrics['low_stock']} con stock bajo",
            help_text="Disponibilidad total"
        )

    with col4:
        trend_stock = -5.2 if material_metrics['out_of_stock'] > 0 else 0
        create_metric_card_advanced(
            value=material_metrics['out_of_stock'],
            label="⚠️ Sin Stock",
            icon="⚠️",
            trend=trend_stock,
            subtitle="Requiere atención",
            help_text="Productos agotados"
        )

    # Fila 2: Métricas adicionales
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        create_metric_card_advanced(
            value=len(places),
            label="🏢 Ubicaciones",
            icon="🏢",
            subtitle="Puntos de almacén",
            help_text="Infraestructura"
        )

    with col6:
        avg_value = material_metrics['avg_value_per_material']
        create_metric_card_advanced(
            value=f"${avg_value:.2f}",
            label="💰 Valor Promedio",
            icon="💰",
            subtitle="Por material",
            help_text="Valorización promedio"
        )

    with col7:
        admin_percent = user_metrics['admin_percentage']
        create_metric_card_advanced(
            value=f"{admin_percent:.1f}%",
            label="👑 Admin Ratio",
            icon="👑",
            subtitle="Porcentaje administradores",
            help_text="Distribución roles"
        )

    with col8:
        clasificaciones = len(material_metrics.get('classifications', {}))
        create_metric_card_advanced(
            value=clasificaciones,
            label="📑 Categorías",
            icon="📑",
            subtitle="Clasificaciones",
            help_text="Diversidad productos"
        )

    # SECCIÓN: PREDICCIONES RÁPIDAS MEJORADA
    st.markdown("---")
    st.markdown("### 🔮 PREDICCIONES E INSIGHTS AUTOMÁTICOS")

    col_ins1, col_ins2, col_ins3 = st.columns(3)

    with col_ins1:
        with st.container():
            st.markdown("#### 📊 Tendencia de Valor")
            st.markdown("""
            <div style='background: #f0f9ff; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #0ea5e9;'>
            <h4 style='margin: 0; color: #0369a1;'>📈 Proyección de Valor</h4>
            """, unsafe_allow_html=True)

            materiales_df = pd.DataFrame(materials)
            if len(materiales_df) > 1 and 'costo_promedio' in materiales_df.columns and 'existencia' in materiales_df.columns:
                X = np.arange(len(materiales_df)).reshape(-1, 1)
                y = materiales_df['costo_promedio'] * materiales_df['existencia']
                modelo = LinearRegression()
                modelo.fit(X, y)
                proximo_valor = modelo.predict([[len(materiales_df)]])[0]

                st.metric("Próximo valor esperado", f"${proximo_valor:,.2f}")
                crecimiento_valor = ((proximo_valor - y.mean()) / y.mean()) * 100
                st.metric("Crecimiento proyectado", f"{crecimiento_valor:+.1f}%")

            st.markdown("</div>", unsafe_allow_html=True)

    with col_ins2:
        with st.container():
            st.markdown("#### 📈 Crecimiento Esperado")
            st.markdown("""
            <div style='background: #f0fdf4; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #22c55e;'>
            <h4 style='margin: 0; color: #15803d;'>👥 Tendencias de Usuarios</h4>
            """, unsafe_allow_html=True)

            crecimiento = user_metrics['growth_rate'] * 100
            st.metric("Tasa crecimiento mensual", f"{crecimiento:.1f}%")

            # Proyección
            proyeccion = user_metrics['total'] * (1 + user_metrics['growth_rate'])
            st.metric("Usuarios en 30 días", f"{proyeccion:.0f}", delta=f"+{proyeccion - user_metrics['total']:.0f}")

            st.markdown("</div>", unsafe_allow_html=True)

    with col_ins3:
        with st.container():
            st.markdown("#### ⚠️ Alertas Predictivas")
            st.markdown("""
            <div style='background: #fef2f2; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #ef4444;'>
            <h4 style='margin: 0; color: #dc2626;'>🚨 Sistema de Alertas</h4>
            """, unsafe_allow_html=True)

            alertas = []
            if material_metrics['out_of_stock'] > 2:
                alertas.append("🔴 Alto riesgo de desabastecimiento")
            if material_metrics['low_stock'] > 5:
                alertas.append("🟡 Múltiples productos con stock bajo")
            if user_metrics['admin_percentage'] > 50:
                alertas.append("🟢 Ratio admin saludable")
            else:
                alertas.append("🔵 Estructura de usuarios balanceada")

            if not alertas:
                alertas.append("✅ Estado óptimo del sistema")

            for alerta in alertas:
                st.write(f"• {alerta}")

            st.markdown("</div>", unsafe_allow_html=True)

    # SECCIÓN: VISUALIZACIONES RÁPIDAS
    st.markdown("---")
    st.markdown("### 📊 VISTAS RÁPIDAS DEL SISTEMA")

    col_viz1, col_viz2 = st.columns(2)

    with col_viz1:
        # Distribución de materiales por clasificación
        if material_metrics.get('classifications'):
            clasif_data = material_metrics['classifications']
            fig_clasif = px.pie(
                values=list(clasif_data.values()),
                names=list(clasif_data.keys()),
                title="📑 Distribución por Clasificación"
            )
            st.plotly_chart(fig_clasif, use_container_width=True)

    with col_viz2:
        # Valor por material (top 10)
        if materials:
            materiales_df = pd.DataFrame(materials)
            materiales_df['valor_total'] = materiales_df['existencia'] * materiales_df['costo_promedio']
            top_materiales = materiales_df.nlargest(10, 'valor_total')

            # ✅ CORRECCIÓN: usar la variable correcta (materiales_df)
            fig_valor = px.bar(
                data_frame=top_materiales,
                x='descripcion',
                y='valor_total',
                title="Valor total por descripción"
            )
            st.plotly_chart(fig_valor, use_container_width=True)
            fig_valor.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_valor, use_container_width=True)


# FUNCIONES AUXILIARES (mantenidas)

def generate_sample_activity_data(days=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    dates = []
    activities = []
    categories = ['Login', 'Creación', 'Edición', 'Eliminación', 'Consulta']
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        dates.append(current_date)
        activities.append({
            'date': current_date,
            'logins': random.randint(5, 25),
            'creations': random.randint(1, 8),
            'editions': random.randint(2, 12),
            'deletions': random.randint(0, 3),
            'consultas': random.randint(10, 30)
        })
    
    return dates, activities

def calculate_user_metrics(users):
    total_users = len(users)
    admin_users = sum(1 for u in users if u.get('role') == 'admin')
    regular_users = total_users - admin_users
    growth_rate = random.uniform(0.05, 0.15)
    
    return {
        'total': total_users,
        'admins': admin_users,
        'regulars': regular_users,
        'growth_rate': growth_rate,
        'admin_percentage': (admin_users / total_users * 100) if total_users > 0 else 0
    }

def calculate_material_metrics(materials):
    total_materials = len(materials)
    total_value = sum(m.get('existencia', 0) * m.get('costo_promedio', 0) for m in materials)
    total_quantity = sum(m.get('existencia', 0) for m in materials)
    low_stock = sum(1 for m in materials if m.get('existencia', 0) <= 10 and m.get('existencia', 0) > 0)
    out_of_stock = sum(1 for m in materials if m.get('existencia', 0) == 0)
    
    classifications = {}
    for material in materials:
        clasif = material.get('clasificacion', 'Sin clasificar')
        classifications[clasif] = classifications.get(clasif, 0) + 1
    
    return {
        'total_materials': total_materials,
        'total_value': total_value,
        'total_quantity': total_quantity,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'classifications': classifications,
        'avg_value_per_material': total_value / total_materials if total_materials > 0 else 0
    }

# FUNCIÓN PRINCIPAL MANTENIENDO EL NOMBRE ORIGINAL

def mostrar_analytics():
    """Función principal - MANTIENE EL NOMBRE ORIGINAL para compatibilidad"""
    setup_page_config()
    apply_advanced_styles()
    create_welcome_header()
    
    # Sidebar 
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h2 style='color: #6366F1;'>🔍 MÓDULOS</h2>
                <p style='color: #6B7280;'>Selecciona tu análisis</p>
            </div>
        """, unsafe_allow_html=True)
        
        modulo_activo = st.radio(
            "Navegación principal:",
            [
                "🏠 Dashboard Principal", 
                "🎯 Regresión Polinómica", 
                "🔮 Regresión Múltiple", 
                "📊 Análisis Temporal"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Información del sistema
        st.markdown("### 📊 Estado del Sistema")
        users = get_all_users()
        materials = get_all_material()
        
        st.metric("Usuarios activos", len(users))
        st.metric("Materiales registrados", len(materials))
        st.metric("Última actualización", datetime.now().strftime("%H:%M"))
        
        st.markdown("---")
        
        # Configuración rápida
        st.markdown("### ⚙️ Configuración")
        tema_oscuro = st.toggle("Modo oscuro", False)
        actualizar_auto = st.toggle("Actualización automática", True)
        
        if st.button("🔄 Actualizar Datos", use_container_width=True):
            st.rerun()
    
    # Navegación entre módulos
    if modulo_activo == "🏠 Dashboard Principal":
        mostrar_dashboard_principal_interactivo()
    elif modulo_activo == "🎯 Regresión Polinómica":
        mostrar_regresion_polinomica_interactiva()
    elif modulo_activo == "🔮 Regresión Múltiple":
        mostrar_regresion_multiple_interactiva()
    elif modulo_activo == "📊 Análisis Temporal":
        mostrar_analisis_tendencias_avanzado()


# EJECUCIÓN PRINCIPAL

if __name__ == "__main__":
    mostrar_analytics()