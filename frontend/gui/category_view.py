import streamlit as st
from backend.controllers.category_controller import (
    get_all_categories,
    create_category,
    update_category,
    delete_category,
)

def build_category_frame():
    st.subheader("📂 Administración de categorías")

    # Mensajes de estado
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
        try:
            categories = get_all_categories(limit=100)
            if not categories:
                st.info("⚠️ No hay categorías todavía.")
            else:
                st.write(f"**Total de categorías:** {len(categories)}")
                for c in categories:
                    with st.expander(f"📂 {c['name']}"):
                        st.write(f"**Descripción:** {c.get('description', 'Sin descripción')}")
                        st.write(f"**ID:** {c['_id']}")
        except Exception as e:
            st.error(f"❌ Error al cargar categorías: {str(e)}")

    # --- CREAR ---
    elif menu == "➕ Crear":
        with st.form("create_category"):
            name = st.text_input("Nombre de la categoría")
            description = st.text_area("Descripción")
            submitted = st.form_submit_button("Guardar")

            if submitted:
                if not name.strip():
                    st.error("❌ El nombre es obligatorio")
                else:
                    try:
                        result = create_category({"name": name, "description": description})
                        if result:
                            st.session_state["msg"] = (f"✅ Categoría '{name}' creada correctamente", "success")
                            st.rerun()
                        else:
                            st.error("❌ No se pudo crear la categoría")
                    except Exception as e:
                        st.error(f"❌ Error al crear categoría: {str(e)}")

    # --- EDITAR ---
    elif menu == "✏️ Editar":
        try:
            categories = get_all_categories(limit=100)
            if not categories:
                st.info("⚠️ No hay categorías para editar.")
            else:
                options = [f"{c['name']} (ID: {c['_id'][:8]}...)" for c in categories]
                selected = st.selectbox("Selecciona una categoría", options)

                if selected:
                    index = options.index(selected)
                    category = categories[index]

                    with st.form("edit_category"):
                        st.write(f"**Editando:** {category['name']}")
                        name = st.text_input("Nombre", category["name"])
                        description = st.text_area("Descripción", category.get("description", ""))

                        submitted = st.form_submit_button("Actualizar")
                        if submitted:
                            if not name.strip():
                                st.error("❌ El nombre es obligatorio")
                            else:
                                try:
                                    result = update_category(category["_id"], {"name": name, "description": description})
                                    if result:
                                        st.session_state["msg"] = (f"✅ Categoría '{name}' actualizada correctamente", "success")
                                        st.rerun()
                                    else:
                                        st.error("❌ No se pudo actualizar la categoría")
                                except Exception as e:
                                    st.error(f"❌ Error al actualizar categoría: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error al cargar categorías: {str(e)}")

    # --- ELIMINAR ---
    elif menu == "🗑️ Eliminar":
        try:
            categories = get_all_categories(limit=100)
            if not categories:
                st.info("⚠️ No hay categorías para eliminar.")
            else:
                options = [f"{c['name']} (ID: {c['_id'][:8]}...)" for c in categories]
                selected = st.selectbox("Selecciona una categoría", options)

                if selected:
                    index = options.index(selected)
                    category = categories[index]

                    st.warning(f"⚠️ Estás a punto de eliminar la categoría: **{category['name']}**")
                    st.write(f"**Descripción:** {category.get('description', 'Sin descripción')}")

                    if st.button("Eliminar definitivamente", type="primary"):
                        try:
                            result = delete_category(category["_id"])
                            if result:
                                st.session_state["msg"] = (f"❌ Categoría '{category['name']}' eliminada correctamente", "success")
                                st.rerun()
                            else:
                                st.error("❌ No se pudo eliminar la categoría")
                        except Exception as e:
                            st.error(f"❌ Error al eliminar categoría: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error al cargar categorías: {str(e)}")
