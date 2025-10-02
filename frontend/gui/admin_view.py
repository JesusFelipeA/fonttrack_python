<<<<<<< HEAD
# frontend/gui/admin_view.py

import streamlit as st
from backend.controllers.user_controller import get_all_users, delete_user

def build_admin_frame():
    st.title("👤 Usuarios registrados")

    users = get_all_users()
    for user in users:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{user['email']} ({user['role']})")
        with col2:
            if st.button("Eliminar", key=user['email']):
                delete_user(user['email'])
                st.success(f"Usuario {user['email']} eliminado")
                st.experimental_rerun()
=======
import streamlit as st
from backend.services import product_service

def build_admin_frame():
    st.title("⚙️ Administración de productos")

    if "msg" in st.session_state:
        msg, msg_type = st.session_state.pop("msg")
        if msg_type == "success":
            st.success(msg)
        elif msg_type == "error":
            st.error(msg)
        elif msg_type == "info":
            st.info(msg)

    menu = st.radio("Acción", ["📄 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"], horizontal=True)

    # --- LISTAR ---
    if menu == "📄 Listar":
        products = product_service.get_all_products(limit=50)
        st.subheader("Listado de productos")
        if not products:
            st.info("⚠️ No hay productos todavía.")
        for p in products:
            st.markdown(f"- **{p['name']}** | ${p['price']} | Stock: {p['stock']} | Cat: {p['category']}")

    # --- CREAR ---
    elif menu == "➕ Crear":
        st.subheader("Crear producto")
        with st.form("create_product"):
            name = st.text_input("Nombre")
            description = st.text_area("Descripción")
            price = st.number_input("Precio", min_value=0.0)
            stock = st.number_input("Stock", min_value=0)
            category = st.text_input("Categoría")

            submitted = st.form_submit_button("Guardar")
            if submitted:
                new_product = {
                    "name": name,
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "category": category,
                }
                product_service.create_product(new_product)
                st.session_state["msg"] = (f"✅ Producto '{name}' creado correctamente", "success")
                st.rerun()

    # --- EDITAR ---
    elif menu == "✏️ Editar":
        st.subheader("Editar producto")
        products = product_service.get_all_products(limit=50)
        if not products:
            st.info("⚠️ No hay productos para editar.")
            return

        product_names = [f"{p['name']} ({str(p['_id'])})" for p in products]
        selected = st.selectbox("Selecciona un producto", product_names)

        if selected:
            product = next(p for p in products if str(p["_id"]) in selected)
            with st.form("edit_product"):
                name = st.text_input("Nombre", product["name"])
                description = st.text_area("Descripción", product.get("description", ""))
                price = st.number_input("Precio", value=float(product["price"]))
                stock = st.number_input("Stock", value=int(product["stock"]))
                category = st.text_input("Categoría", product.get("category", ""))

                submitted = st.form_submit_button("Actualizar")
                if submitted:
                    update_data = {
                        "name": name,
                        "description": description,
                        "price": price,
                        "stock": stock,
                        "category": category,
                    }
                    product_service.update_product(str(product["_id"]), update_data)
                    st.session_state["msg"] = (f"✅ Producto '{name}' actualizado correctamente", "success")
                    st.rerun()

    # --- ELIMINAR ---
    elif menu == "🗑️ Eliminar":
        st.subheader("Eliminar producto")
        products = product_service.get_all_products(limit=50)
        if not products:
            st.info("⚠️ No hay productos para eliminar.")
            return

        product_names = [f"{p['name']} ({str(p['_id'])})" for p in products]
        selected = st.selectbox("Selecciona un producto", product_names)

        if selected:
            product = next(p for p in products if str(p["_id"]) in selected)
            if st.button("Eliminar definitivamente"):
                product_service.delete_product(str(product["_id"]))
                st.session_state["msg"] = (f"❌ Producto '{product['name']}' eliminado correctamente", "error")
                st.rerun()
>>>>>>> 09544df (Crud de productos)
