import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

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

# ESTILOS PARA ANALYTICS
def apply_analytics_styles():
    st.markdown("""
        <style>
        :root {
            --analytics-primary: #6366F1;
            --analytics-secondary: #8B5CF6;
            --analytics-success: #10B981;
            --analytics-warning: #F59E0B;
            --analytics-error: #EF4444;
            --analytics-dark: #1F2937;
        }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border-left: 4px solid var(--analytics-primary);
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: var(--analytics-primary);
            margin: 0.5rem 0;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #6B7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .chart-container {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
        }
        
        .kpi-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-left: 0.5rem;
        }
        
        .kpi-positive { background: #D1FAE5; color: #065F46; }
        .kpi-negative { background: #FEE2E2; color: #991B1B; }
        .kpi-neutral { background: #F3F4F6; color: #6B7280; }
        </style>
    """, unsafe_allow_html=True)

# FUNCIONES DE DATOS Y MÉTRICAS
def generate_sample_activity_data(days=30):
    """Genera datos de actividad de ejemplo"""
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
    """Calcula métricas de usuarios"""
    total_users = len(users)
    admin_users = sum(1 for u in users if u.get('role') == 'admin')
    regular_users = total_users - admin_users
    
    # Calcular crecimiento (ejemplo)
    growth_rate = random.uniform(0.05, 0.15)
    
    return {
        'total': total_users,
        'admins': admin_users,
        'regulars': regular_users,
        'growth_rate': growth_rate,
        'admin_percentage': (admin_users / total_users * 100) if total_users > 0 else 0
    }

def calculate_material_metrics(materials):
    """Calcula métricas de materiales"""
    total_materials = len(materials)
    total_value = sum(m.get('existencia', 0) * m.get('costo_promedio', 0) for m in materials)
    total_quantity = sum(m.get('existencia', 0) for m in materials)
    
    # Materiales con stock bajo
    low_stock = sum(1 for m in materials if m.get('existencia', 0) <= 10 and m.get('existencia', 0) > 0)
    out_of_stock = sum(1 for m in materials if m.get('existencia', 0) == 0)
    
    # Clasificaciones
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

def calculate_place_metrics(places):
    """Calcula métricas de lugares"""
    total_places = len(places)
    
    # Tipos de lugares
    place_types = {}
    for place in places:
        tipo = place.get('tipo', 'Sin tipo')
        place_types[tipo] = place_types.get(tipo, 0) + 1
    
    return {
        'total_places': total_places,
        'place_types': place_types
    }

# COMPONENTES DE VISUALIZACIÓN

def create_metric_card(value, label, icon, trend=None, subtitle=None):
    """Crea una tarjeta de métrica visual"""
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

def create_activity_chart(activities, dates):
    """Crea gráfico de actividad"""
    df = pd.DataFrame(activities)
    df['date'] = dates
    
    fig = go.Figure()
    
    # Agregar trazas para cada tipo de actividad
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['logins'],
        mode='lines+markers',
        name='Logins',
        line=dict(color='#6366F1', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['consultas'],
        mode='lines+markers',
        name='Consultas',
        line=dict(color='#10B981', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['creations'],
        mode='lines+markers',
        name='Creaciones',
        line=dict(color='#F59E0B', width=3)
    ))
    
    fig.update_layout(
        title="Actividad del Sistema (Últimos 30 días)",
        xaxis_title="Fecha",
        yaxis_title="Cantidad de Actividades",
        hovermode='x unified',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_user_distribution_chart(user_metrics):
    """Crea gráfico de distribución de usuarios"""
    labels = ['Administradores', 'Usuarios Regulares']
    values = [user_metrics['admins'], user_metrics['regulars']]
    colors = ['#8B5CF6', '#6366F1']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        hole=.4,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title="Distribución de Usuarios por Rol",
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_material_value_chart(materials):
    """Crea gráfico de valor de materiales (Top 10)"""
    import pandas as pd
    import plotly.express as px

    # Convertir a DataFrame
    df = pd.DataFrame(materials)

    # Validar columnas necesarias
    required_cols = {'existencia', 'costo_promedio'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Faltan columnas requeridas: {required_cols - set(df.columns)}")

    # Calcular valor total
    df['valor_total'] = df['existencia'] * df['costo_promedio']

    # Determinar el campo de nombre/descripcion
    x_col = 'nombre' if 'nombre' in df.columns else 'descripcion'

    # Top 10 materiales por valor total
    top_materials = df.nlargest(10, 'valor_total')

    # Crear gráfico
    fig = px.bar(
        top_materials.sort_values('valor_total', ascending=True),  # Orden ascendente para que la barra más grande esté arriba
        x='valor_total',
        y=x_col,
        orientation='h',  # Gráfico de barras horizontal
        title="🔹 Top 10 Materiales por Valor de Inventario",
        color='valor_total',
        color_continuous_scale='Viridis',
        text='valor_total'  # Mostrar valores encima
    )

    # Mejorar diseño
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        xaxis_title="Valor Total ($)",
        yaxis_title="Material",
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=100, r=20, t=80, b=50)
    )

    return fig

def create_stock_status_chart(material_metrics):
    """Crea gráfico de estado de stock"""
    labels = ['Stock Normal', 'Stock Bajo', 'Sin Stock']
    values = [
        material_metrics['total_materials'] - material_metrics['low_stock'] - material_metrics['out_of_stock'],
        material_metrics['low_stock'],
        material_metrics['out_of_stock']
    ]
    colors = ['#10B981', '#F59E0B', '#EF4444']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title="Estado del Stock de Materiales",
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_classification_chart(material_metrics):
    """Crea gráfico de clasificaciones de materiales"""
    classifications = material_metrics['classifications']
    
    fig = px.bar(
        x=list(classifications.keys()),
        y=list(classifications.values()),
        title="Materiales por Clasificación",
        color=list(classifications.values()),
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis_title="Clasificación",
        yaxis_title="Cantidad de Materiales",
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# VISTA PRINCIPAL DE ANALYTICS
def mostrar_analytics():
    
    # Aplicar estilos
    apply_analytics_styles()
    
    # Header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: var(--analytics-primary); margin-bottom: 0.5rem;">📊 Dashboard de Analytics</h1>
            <p style="color: #6B7280;">Métricas y análisis en tiempo real del sistema</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Obtener datos
    users = get_all_users() or []
    materials = get_all_material() or []
    places = get_all_lugares() or []
    
    # Calcular métricas
    user_metrics = calculate_user_metrics(users)
    material_metrics = calculate_material_metrics(materials)
    place_metrics = calculate_place_metrics(places)
    
    # Generar datos de actividad
    dates, activities = generate_sample_activity_data()
    
    # SECCIÓN: KPI PRINCIPALES
    
    st.markdown("### 📈 Métricas Principales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(
            value=user_metrics['total'],
            label="Total Usuarios",
            icon="👥",
            trend=user_metrics['growth_rate'] * 100,
            subtitle=f"{user_metrics['admins']} administradores"
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
            value=place_metrics['total_places'],
            label="Lugares Activos",
            icon="📍",
            subtitle=f"{len(place_metrics['place_types'])} tipos diferentes"
        )
    
    with col4:
        total_activities = sum(a['logins'] + a['creations'] + a['editions'] + a['deletions'] + a['consultas'] for a in activities)
        create_metric_card(
            value=total_activities,
            label="Actividades (30d)",
            icon="📊",
            trend=8.5,
            subtitle="Actividad del sistema"
        )
    
    # SECCIÓN: GRÁFICOS PRINCIPALES
    
    st.markdown("### 📊 Visualizaciones Principales")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_activity = create_activity_chart(activities, dates)
        st.plotly_chart(fig_activity, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_chart2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_material_value = create_material_value_chart(materials)
        st.plotly_chart(fig_material_value, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # -------------------------
    # SECCIÓN: ANÁLISIS DE MATERIALES
    # -------------------------
    st.markdown("### 🧱 Análisis de Inventario")
    
    col_mat1, col_mat2, col_mat3 = st.columns(3)
    
    with col_mat1:
        create_metric_card(
            value=f"${material_metrics['total_value']:,.2f}",
            label="Valor Total Inventario",
            icon="💰",
            subtitle=f"${material_metrics['avg_value_per_material']:.2f} promedio"
        )
    
    with col_mat2:
        create_metric_card(
            value=material_metrics['total_quantity'],
            label="Unidades en Stock",
            icon="📦",
            subtitle=f"{material_metrics['low_stock']} con stock bajo"
        )
    
    with col_mat3:
        create_metric_card(
            value=material_metrics['out_of_stock'],
            label="Materiales Sin Stock",
            icon="⚠️",
            trend=-5.2 if material_metrics['out_of_stock'] > 0 else 0,
            subtitle="Necesitan reposición"
        )
    
    # Gráficos de materiales
    col_mat_chart1, col_mat_chart2 = st.columns(2)
    
    with col_mat_chart1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_stock = create_stock_status_chart(material_metrics)
        st.plotly_chart(fig_stock, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_mat_chart2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_classification = create_classification_chart(material_metrics)
        st.plotly_chart(fig_classification, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN: ANÁLISIS DE USUARIOS
    st.markdown("### 👥 Análisis de Usuarios")
    
    col_user1, col_user2 = st.columns(2)
    
    with col_user1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_user_dist = create_user_distribution_chart(user_metrics)
        st.plotly_chart(fig_user_dist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_user2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Tabla de usuarios recientes
        st.subheader("👤 Usuarios Recientes")
        
        if users:
            # Ordenar por fecha (si existe)
            sorted_users = sorted(users, key=lambda x: x.get('fecha_creacion', ''), reverse=True)[:5]
            
            for user in sorted_users:
                role_icon = "👑" if user.get('role') == 'admin' else "👤"
                st.write(f"{role_icon} **{user.get('correo', 'N/A')}** - {user.get('role', 'user').upper()}")
        else:
            st.info("No hay usuarios registrados")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN: REPORTES RÁPIDOS
    st.markdown("### 📋 Reportes Rápidos")
    
    col_report1, col_report2 = st.columns(2)
    
    with col_report1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🚨 Alertas del Sistema")
        
        alerts = []
        
        # Verificar stock bajo
        if material_metrics['low_stock'] > 0:
            alerts.append(f"⚠️ {material_metrics['low_stock']} materiales con stock bajo")
        
        # Verificar sin stock
        if material_metrics['out_of_stock'] > 0:
            alerts.append(f"❌ {material_metrics['out_of_stock']} materiales sin stock")
        
        # Verificar actividad reciente
        recent_activity = activities[-1]
        if recent_activity['logins'] < 5:
            alerts.append("📉 Baja actividad de usuarios hoy")
        
        if alerts:
            for alert in alerts:
                st.write(alert)
        else:
            st.success("✅ Todo funciona correctamente")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_report2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🎯 Recomendaciones")
        
        recommendations = []
        
        if material_metrics['out_of_stock'] > 0:
            recommendations.append("**Reponer stock**: Considera reordenar materiales sin existencias")
        
        if material_metrics['low_stock'] > 3:
            recommendations.append("**Revisar inventario**: Múltiples materiales con stock bajo")
        
        if user_metrics['admins'] == 0:
            recommendations.append("**Designar administradores**: No hay usuarios administradores")
        elif user_metrics['admins'] / user_metrics['total'] > 0.5:
            recommendations.append("**Balancear roles**: Demasiados administradores")
        
        if recommendations:
            for rec in recommendations:
                st.write(f"• {rec}")
        else:
            st.info("💡 El sistema está optimizado")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # PIE DE PÁGINA
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
            <p>📅 Última actualización: {}</p>
            <p>📊 Dashboard generado automáticamente • Datos en tiempo real</p>
        </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

# -------------------------
# EJECUCIÓN
# -------------------------
if __name__ == "__main__":
    mostrar_analytics()