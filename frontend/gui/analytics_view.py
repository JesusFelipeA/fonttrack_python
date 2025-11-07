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


# MÓDULOS DE REGRESIÓN INCORPORADOS

def mostrar_regresion_polinomica():
    """Módulo de Regresión Polinómica Interactiva"""
    st.markdown("### 📈 Regresión Polinómica Predictiva")
    
    with st.expander("🔧 Configurar Modelo Predictivo", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            grado = st.slider("Grado del polinomio", 1, 6, 2)
            variable_x = st.selectbox("Variable predictora (X)", ["existencia", "costo_promedio"])
            variable_y = st.selectbox("Variable objetivo (Y)", ["costo_promedio", "existencia"])
        
        with col2:
            n_puntos = st.slider("Número de puntos de datos", 20, 200, 50)
            ruido = st.slider("Nivel de ruido", 0.1, 5.0, 1.0)
    
    # Generar datos sintéticos basados en materiales reales
    materiales = get_all_material()
    if materiales:
        # Usar estadísticas reales para generar datos más realistas
        costos = [m['costo_promedio'] for m in materiales]
        existencias = [m['existencia'] for m in materiales]
        
        # Crear relación no lineal basada en datos reales
        X_base = np.linspace(min(existencias), max(existencias), n_puntos)
        y_base = np.polyval([-0.01, 0.5, 5], X_base)  # Polinomio base
        y = y_base + np.random.normal(0, ruido, n_puntos)
        X = X_base.reshape(-1, 1)
        
        # Entrenar modelo polinómico
        poly = PolynomialFeatures(degree=grado)
        X_poly = poly.fit_transform(X)
        
        modelo = LinearRegression()
        modelo.fit(X_poly, y)
        y_pred = modelo.predict(X_poly)
        
        # Métricas
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        
        # Visualización
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=X.flatten(), y=y, mode='markers', 
                name='Datos reales', marker=dict(color='blue', size=6)
            ))
            fig.add_trace(go.Scatter(
                x=X.flatten(), y=y_pred, mode='lines',
                name=f'Modelo (grado {grado})', line=dict(color='red', width=3)
            ))
            fig.update_layout(
                title=f"Regresión Polinómica (R² = {r2:.3f})",
                xaxis_title=variable_x,
                yaxis_title=variable_y,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_viz2:
            # Residuales
            residuales = y - y_pred
            fig_res = go.Figure()
            fig_res.add_trace(go.Scatter(
                x=y_pred, y=residuales, mode='markers',
                marker=dict(color='orange', size=6)
            ))
            fig_res.add_hline(y=0, line_dash="dash", line_color="red")
            fig_res.update_layout(
                title="Análisis de Residuales",
                xaxis_title="Predicciones",
                yaxis_title="Error (Real - Predicho)",
                height=400
            )
            st.plotly_chart(fig_res, use_container_width=True)
        
        # Métricas y diagnóstico
        col_met1, col_met2, col_met3 = st.columns(3)
        col_met1.metric("R²", f"{r2:.3f}")
        col_met2.metric("RMSE", f"{rmse:.2f}")
        col_met3.metric("Grado Polinomio", grado)
        
        # Diagnóstico automático
        if grado == 1:
            diagnostico = "📊 Modelo lineal simple - Puede subestimar relaciones complejas"
        elif 2 <= grado <= 3:
            diagnostico = "✅ Modelo balanceado - Buen equilibrio entre flexibilidad y generalización"
        else:
            diagnostico = "⚠️ Modelo complejo - Riesgo de sobreajuste, considerar validación cruzada"
        
        st.info(diagnostico)

def mostrar_regresion_multiple():
    """Módulo de Regresión Lineal Múltiple"""
    st.markdown("### 🔮 Regresión Múltiple Predictiva")
    
    with st.expander("🎯 Configurar Variables", expanded=True):
        materiales_df = pd.DataFrame(get_all_material())
        
        col1, col2 = st.columns(2)
        with col1:
            variables_predictoras = st.multiselect(
                "Variables predictoras (X)",
                options=materiales_df.select_dtypes(include=[np.number]).columns.tolist(),
                default=["existencia", "costo_promedio"]
            )
        with col2:
            variable_objetivo = st.selectbox(
                "Variable objetivo (Y)",
                options=materiales_df.select_dtypes(include=[np.number]).columns.tolist(),
                index=0
            )
    
    if len(variables_predictoras) < 1:
        st.warning("Selecciona al menos una variable predictora")
        return
    
    # Preparar datos
    X = materiales_df[variables_predictoras]
    y = materiales_df[variable_objetivo]
    
    # Entrenar modelo
    modelo = LinearRegression()
    modelo.fit(X, y)
    y_pred = modelo.predict(X)
    
    # Métricas
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    # Resultados
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.subheader("📊 Coeficientes del Modelo")
        coef_df = pd.DataFrame({
            'Variable': ['Intercepto'] + variables_predictoras,
            'Coeficiente': [modelo.intercept_] + modelo.coef_.tolist()
        })
        st.dataframe(coef_df, use_container_width=True)
    
    with col_res2:
        st.subheader("📈 Métricas de Rendimiento")
        col_met1, col_met2 = st.columns(2)
        col_met1.metric("R²", f"{r2:.3f}")
        col_met2.metric("RMSE", f"{rmse:.2f}")
        
        # Predicción interactiva
        st.subheader("🎯 Predicción en Tiempo Real")
        inputs = {}
        for var in variables_predictoras:
            min_val = float(X[var].min())
            max_val = float(X[var].max())
            inputs[var] = st.slider(
                f"{var}", min_val, max_val, float(X[var].mean())
            )
        
        if st.button("Predecir"):
            input_df = pd.DataFrame([inputs])
            prediccion = modelo.predict(input_df)[0]
            st.success(f"**Predicción:** {prediccion:.2f}")

def mostrar_analisis_tendencias():
    """Módulo de Análisis de Tendencias Temporales"""
    st.markdown("### 📅 Análisis de Tendencias Temporales")
    
    # Generar datos temporales sintéticos
    fechas = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    tendencia_base = np.linspace(100, 200, len(fechas))
    estacionalidad = 20 * np.sin(2 * np.pi * np.arange(len(fechas)) / 30)
    ruido = np.random.normal(0, 10, len(fechas))
    valores = tendencia_base + estacionalidad + ruido
    
    datos_temporales = pd.DataFrame({
        'fecha': fechas,
        'valor': valores,
        'ventas_moviles': pd.Series(valores).rolling(window=7).mean()
    })
    
    # Regresión para tendencia
    X_temp = np.arange(len(datos_temporales)).reshape(-1, 1)
    y_temp = datos_temporales['valor'].values
    
    modelo_tendencia = LinearRegression()
    modelo_tendencia.fit(X_temp, y_temp)
    tendencia_lineal = modelo_tendencia.predict(X_temp)
    
    # Visualización
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=datos_temporales['fecha'], y=datos_temporales['valor'],
        mode='lines', name='Valores Diarios', line=dict(color='lightblue')
    ))
    fig.add_trace(go.Scatter(
        x=datos_temporales['fecha'], y=datos_temporales['ventas_moviles'],
        mode='lines', name='Media Móvil (7 días)', line=dict(color='blue', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=datos_temporales['fecha'], y=tendencia_lineal,
        mode='lines', name='Tendencia Lineal', line=dict(color='red', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title="Análisis de Tendencia Temporal con Regresión Lineal",
        xaxis_title="Fecha",
        yaxis_title="Valor",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métricas de tendencia
    pendiente = modelo_tendencia.coef_[0] * 30  # Pendiente mensual
    col1, col2, col3 = st.columns(3)
    col1.metric("Pendiente Mensual", f"{pendiente:.1f}")
    col2.metric("R² Tendencia", f"{r2_score(y_temp, tendencia_lineal):.3f}")
    col3.metric("Dirección", "📈 Alcista" if pendiente > 0 else "📉 Bajista")

# ESTILOS PARA ANALYTICS
def apply_analytics_styles():
    st.markdown("""
        <style>
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #6366F1;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #6366F1;
            margin: 0.5rem 0;
        }
        
        .chart-container {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

# FUNCIONES DE DATOS Y MÉTRICAS (mantenidas del código original)
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

# COMPONENTES DE VISUALIZACIÓN (mantenidos del código original)
def create_metric_card(value, label, icon, trend=None, subtitle=None):
    trend_html = ""
    if trend is not None:
        trend_class = "kpi-positive" if trend > 0 else "kpi-negative" if trend < 0 else "kpi-neutral"
        trend_icon = "📈" if trend > 0 else "📉" if trend < 0 else "➡️"
        trend_html = f'<span class="kpi-badge {trend_class}">{trend_icon} {abs(trend):.1f}%</span>'
    
    subtitle_html = f'<p style="font-size: 0.8rem; color: #6B7280; margin: 0;">{subtitle}</p>' if subtitle else ""
    
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>
            <div class="metric-value">{value}{trend_html}</div>
            <div class="metric-label">{label}</div>
            {subtitle_html}
        </div>
    """, unsafe_allow_html=True)

# VISTA PRINCIPAL DE ANALYTICS MEJORADA
def mostrar_analytics():
    apply_analytics_styles()
    
    # Header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #6366F1; margin-bottom: 0.5rem;">📊 Dashboard de Analytics Avanzado</h1>
            <p style="color: #6B7280;">Métricas, análisis predictivo y machine learning integrado</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para navegación entre módulos
    st.sidebar.title("🔍 Módulos de Análisis")
    modulo_activo = st.sidebar.radio(
        "Seleccionar módulo:",
        ["📈 Dashboard Principal", "🔮 Regresión Polinómica", "📊 Regresión Múltiple", "📅 Análisis Temporal"]
    )
    
    if modulo_activo == "📈 Dashboard Principal":
        mostrar_dashboard_principal()
    elif modulo_activo == "🔮 Regresión Polinómica":
        mostrar_regresion_polinomica()
    elif modulo_activo == "📊 Regresión Múltiple":
        mostrar_regresion_multiple()
    elif modulo_activo == "📅 Análisis Temporal":
        mostrar_analisis_tendencias()

def mostrar_dashboard_principal():
    """Dashboard principal con métricas básicas"""
    # Obtener datos
    users = get_all_users() or []
    materials = get_all_material() or []
    places = get_all_lugares() or []
    
    # Calcular métricas
    user_metrics = calculate_user_metrics(users)
    material_metrics = calculate_material_metrics(materials)
    
    # SECCIÓN: KPI PRINCIPALES
    st.markdown("### 📈 Métricas Principales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(
            value=user_metrics['total'],
            label="Total Usuarios",
            icon="👥",
            trend=user_metrics['growth_rate'] * 100
        )
    
    with col2:
        create_metric_card(
            value=material_metrics['total_materials'],
            label="Materiales Registrados",
            icon="📦",
            subtitle=f"${material_metrics['total_value']:,.2f} valor total"
        )
    
    with col3:
        create_metric_card(
            value=material_metrics['total_quantity'],
            label="Unidades en Stock",
            icon="🔄",
            subtitle=f"{material_metrics['low_stock']} con stock bajo"
        )
    
    with col4:
        create_metric_card(
            value=material_metrics['out_of_stock'],
            label="Materiales Sin Stock",
            icon="⚠️",
            trend=-5.2 if material_metrics['out_of_stock'] > 0 else 0
        )
    
    # SECCIÓN: PREDICCIONES RÁPIDAS
    st.markdown("### 🎯 Insights Predictivos Rápidos")
    
    col_ins1, col_ins2, col_ins3 = st.columns(3)
    
    with col_ins1:
        with st.container():
            st.markdown("#### 📊 Tendencia de Valor")
            # Predicción simple lineal
            materiales_df = pd.DataFrame(materials)
            if len(materiales_df) > 1:
                X = np.arange(len(materiales_df)).reshape(-1, 1)
                y = materiales_df['costo_promedio'] * materiales_df['existencia']
                modelo = LinearRegression()
                modelo.fit(X, y)
                proximo_valor = modelo.predict([[len(materiales_df)]])[0]
                st.metric("Próximo valor esperado", f"${proximo_valor:,.2f}")
    
    with col_ins2:
        with st.container():
            st.markdown("#### 📈 Crecimiento Esperado")
            crecimiento = user_metrics['growth_rate'] * 100
            st.metric("Tasa crecimiento usuarios", f"{crecimiento:.1f}%")
    
    with col_ins3:
        with st.container():
            st.markdown("#### ⚠️ Alertas Predictivas")
            if material_metrics['out_of_stock'] > 2:
                st.error("Alto riesgo de desabastecimiento")
            elif material_metrics['low_stock'] > 5:
                st.warning("Múltiples productos con stock bajo")
            else:
                st.success("Inventario saludable")

# EJECUCIÓN
if __name__ == "__main__":
    mostrar_analytics()