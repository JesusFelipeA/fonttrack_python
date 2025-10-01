import streamlit as st
from backend.controllers.product_controller import get_all_products
from frontend.gui.cart_view import build_cart_frame

def build_product_frame(on_cart_view=None):
    st.title("🛍️ Catálogo de productos")

    # Inicializar el carrito en el estado de sesión
    if "cart" not in st.session_state:
        st.session_state.cart = []

    products = get_all_products(limit=20)

    for product in products:
        col1, col2, col3 = st.columns([4, 2, 2])
        with col1:
            st.markdown(f"**{product['name']}**")
        with col2:
            st.markdown(f"${product['price']}")
        with col3:
            if st.button("Agregar al carrito", key=product['name']):
                # Buscar si ya está en el carrito
                for item in st.session_state.cart:
                    if item["name"] == product["name"]:
                        item["quantity"] += 1
                        break
                else:
                    st.session_state.cart.append({**product, "quantity": 1})
                st.success(f"{product['name']} agregado al carrito")

    st.markdown("---")
    if st.button("Ver carrito"):
        if on_cart_view:
            on_cart_view(st.session_state.cart)
        else:
            build_cart_frame(st.session_state.cart)
