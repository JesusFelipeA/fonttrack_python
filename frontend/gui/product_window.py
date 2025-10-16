import streamlit as st
from backend.controllers.material_controller import get_all_materiales
from frontend.gui.cart_view import build_cart_frame

def build_material_frame(on_cart_view=None):
    st.title("🧱 Catálogo de Materiales")

    # Inicializar el carrito en el estado de sesión
    if "cart" not in st.session_state:
        st.session_state.cart = []

    materiales = get_all_materiales(limit=20)

    for material in materiales:
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        with col1:
            st.markdown(f"**{material.get('descripcion', 'Sin descripción')}**")
            st.caption(f"Clasificación: {material.get('clasificacion', 'N/A')}")
        with col2:
            st.markdown(f"💰 **${material.get('costo_promedio', 0):.2f}**")
        with col3:
            st.markdown(f"📦 {material.get('existencia', 0)} en stock")
        with col4:
            if st.button("Agregar", key=str(material["_id"])):
                # Buscar si ya está en el carrito
                for item in st.session_state.cart:
                    if item["_id"] == material["_id"]:
                        item["quantity"] += 1
                        break
                else:
                    st.session_state.cart.append({
                        **material,
                        "quantity": 1
                    })
                st.success(f"{material.get('descripcion', 'Material')} agregado al carrito")

    st.markdown("---")
    if st.button("🛒 Ver carrito"):
        if on_cart_view:
            on_cart_view(st.session_state.cart)
        else:
            build_cart_frame(st.session_state.cart)
