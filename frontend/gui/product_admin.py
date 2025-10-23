import streamlit as st
from backend.services import product_service
from bson import ObjectId

def build_product_admin_frame():
    st.title("⚙️ Administración de Productos")

    action = st.radio("Acción", ["Ver todos", "Agregar nuevo", "Buscar y editar/eliminar"])

    # 🔹 Ver productos
    if action == "Ver todos":
        products = product_service.get_all_products(limit=50)
        for p in products:
            st.subheader(p.get("name", "Sin nombre"))
            st.write(f"💲 {p.get('price', 0):,.2f} | Stock: {p.get('stock', 0)}")
            st.write(f"Categoría: {p.get('category', '')}")
            st.divider()

    # 🔹 Agregar producto
    elif action == "Agregar nuevo":
        with st.form("new_product"):
            name = st.text_input("Nombre")
            description = st.text_area("Descripción")
            price = st.number_input("Precio", min_value=0.0, step=0.1)
            stock = st.number_input("Stock", min_value=0, step=1)
            category = st.text_input("Categoría")
            submitted = st.form_submit_button("Guardar")

            if submitted:
                product_data = {
                    "name": name,
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "category": category
                }
                inserted_id = product_service.create_product(product_data)
                st.success(f"✅ Producto creado con ID: {inserted_id}")

    # 🔹 Buscar, editar y eliminar
    elif action == "Buscar y editar/eliminar":
        keyword = st.text_input("Palabra clave")
        if keyword:
            results = product_service.collection.find({"name": {"$regex": keyword, "$options": "i"}})
            for p in results:
                st.subheader(p["name"])
                st.write(f"Precio: ${p['price']:,.2f} | Stock: {p['stock']}")
                st.write(f"Categoría: {p['category']}")

                col1, col2 = st.columns(2)
                if col1.button(f"✏️ Editar {p['_id']}", key=f"edit_{p['_id']}"):
                    _edit_product(p)
                if col2.button(f"🗑️ Eliminar {p['_id']}", key=f"delete_{p['_id']}"):
                    deleted = product_service.delete_product(ObjectId(p["_id"]))
                    if deleted:
                        st.warning(f"Producto {p['name']} eliminado")
                        st.experimental_rerun()


def _edit_product(product):
    """Subformulario para editar un producto"""
    with st.form(f"edit_product_{product['_id']}"):
        name = st.text_input("Nombre", value=product["name"])
        description = st.text_area("Descripción", value=product.get("description", ""))
        price = st.number_input("Precio", min_value=0.0, step=0.1, value=float(product["price"]))
        stock = st.number_input("Stock", min_value=0, step=1, value=int(product["stock"]))
        category = st.text_input("Categoría", value=product.get("category", ""))
        submitted = st.form_submit_button("Actualizar")

        if submitted:
            updated = {
                "name": name,
                "description": description,
                "price": price,
                "stock": stock,
                "category": category
            }
            ok = product_service.update_product(ObjectId(product["_id"]), updated)
            if ok:
                st.success("✅ Producto actualizado")
                st.experimental_rerun()
