# frontend/gui/admin_view.py
import streamlit as st
import pandas as pd
from backend.controllers.user_controller import get_all_users, create_user, update_user, delete_user
from backend.services import product_service, category_service

# -------------------------
# Utilidades internas UI
# -------------------------
def show_message_from_state():
    if "msg" in st.session_state:
        msg, msg_type = st.session_state.pop("msg")
        if msg_type == "success":
            st.success(msg)
        elif msg_type == "error":
            st.error(msg)
        else:
            st.info(msg)

def confirm_action(prompt: str, key: str):
    c1, c2 = st.columns([3, 1])
    c1.write(prompt)
    if c2.button("Sí", key=key + "_yes"):
        return True
    if c2.button("No", key=key + "_no"):
        return False
    return None

def df_to_csv_bytes(df: pd.DataFrame):
    return df.to_csv(index=False).encode('utf-8')

# -------------------------
# BUILD FRAME
# -------------------------
def build_admin_frame():
    st.set_page_config(page_title="Panel de administración", layout="wide")
    st.title("⚙️ Panel de administración")
    st.caption("Interfaz HCI: affordance, evaluación, diálogo y manipulación directa aplicados al CRUD.")

    with st.expander("ℹ️ Sobre esta interfaz (clic para abrir)"):
        st.markdown(
            """
            Esta interfaz aplica principios de **Interacción Humano-Computadora**:
            - **Affordance:** elementos autoexplicativos con íconos y textos de ayuda.
            - **Diálogo:** preguntas confirmatorias y feedback inmediato.
            - **Manipulación directa:** expanders, botones de acción por item.
            - **Evaluación:** mensajes y estados claros después de cada operación.
            - **Analytics (ML):** sección de análisis con placeholder para modelos.
            """
        )

    seccion = st.radio(
        "¿Qué deseas administrar?",
        ["👤 Usuarios", "📦 Productos", "📁 Categorías", "📊 Analytics"],
        horizontal=True,
        help="Selecciona la entidad que deseas administrar o la sección de análisis."
    )

    # ---------------------------------------
    # ---------- ADMINISTRAR USUARIOS -------
    # ---------------------------------------
    if seccion == "👤 Usuarios":
        st.subheader("👤 Administración de usuarios")
        st.caption("Crea, edita, lista o elimina usuarios. Cada acción incluye ayuda y confirmaciones.")

        show_message_from_state()

        menu = st.radio(
            "Acción",
            ["📄 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"],
            horizontal=True,
            help="Elige la acción que quieres realizar sobre los usuarios."
        )

        # LISTAR
        if menu == "📄 Listar":
            st.info("🗂️ Lista de usuarios (usa el buscador para filtrar)")
            try:
                users = get_all_users() or []
                users_df = pd.DataFrame(users)
                search = st.text_input("🔎 Buscar por email o rol", "")
                if search:
                    users_df = users_df[users_df.apply(lambda r: search.lower() in str(r.get("email","")).lower() or search.lower() in str(r.get("role","")).lower(), axis=1)]
                if users_df.empty:
                    st.warning("⚠️ No se encontraron usuarios.")
                else:
                    st.write(f"**Total de usuarios:** {len(users_df)}")
                    # mostrar tabla y opción de exportar
                    st.dataframe(users_df[["email", "role"]].rename(columns={"email":"Email","role":"Rol"}))
                    csv_bytes = df_to_csv_bytes(users_df)
                    st.download_button("⬇️ Exportar CSV", csv_bytes, file_name="usuarios.csv", mime="text/csv")

                    # manipulación directa: expanders por usuario
                    for u in users:
                        with st.expander(f"👤 {u.get('email', 'sin email')}"):
                            st.markdown(f"**Rol:** `{u.get('role','')}`  \n**ID:** `{u.get('_id','N/A')}`")
                            c1, c2 = st.columns(2)
                            if c1.button("✏️ Editar", key=f"edit_{u.get('email')}"):
                                # abrir formulario de edición en modal-like (sección en la página)
                                st.session_state["edit_target_user"] = u.get("email")
                                st.experimental_rerun()
                            if c2.button("🗑️ Eliminar", key=f"del_{u.get('email')}"):
                                st.session_state["delete_target_user"] = u.get("email")
                                st.experimental_rerun()

            except Exception as e:
                st.error(f"❌ Error al cargar usuarios: {str(e)}")

        # CREAR
        elif menu == "➕ Crear":
            st.markdown("🧩 **Crear nuevo usuario** — sigue las indicaciones (affordances mostradas).")
            with st.form("create_user", clear_on_submit=True):
                email = st.text_input("📧 Email", help="Correo único que identificará al usuario.")
                role = st.selectbox("🛠️ Rol", ["user", "admin"], help="Nivel de permisos del usuario.")
                password = st.text_input("🔐 Contraseña", type="password", help="Mínimo 6 caracteres recomendado.")
                confirm_password = st.text_input("🔐 Confirmar contraseña", type="password")
                submitted = st.form_submit_button("💾 Guardar")

                if submitted:
                    if not email or not password:
                        st.error("❌ Email y contraseña son obligatorios.")
                    elif password != confirm_password:
                        st.warning("⚠️ Las contraseñas no coinciden.")
                    else:
                        try:
                            new_user = {"email": email, "role": role, "password": password}
                            result = create_user(new_user)
                            if result:
                                st.success(f"✅ Usuario '{email}' creado correctamente.")
                                st.session_state["msg"] = (f"Usuario '{email}' creado correctamente", "success")
                                st.rerun()
                            else:
                                st.error("❌ Error al crear el usuario.")
                        except Exception as e:
                            st.error(f"❌ Error al crear usuario: {str(e)}")

        # EDITAR
        elif menu == "✏️ Editar":
            # If user was selected via manipulación directa, open selected email
            selected_email = st.session_state.get("edit_target_user", None)
            try:
                users = get_all_users() or []
                if not users:
                    st.warning("⚠️ No hay usuarios para editar.")
                else:
                    user_emails = [u["email"] for u in users]
                    selected = st.selectbox("Selecciona un usuario", ["-- seleccionar --"] + user_emails, index=0 if not selected_email else (user_emails.index(selected_email)+1))
                    if selected and selected != "-- seleccionar --":
                        user = next(u for u in users if u["email"] == selected)
                        with st.form("edit_user_form"):
                            email = st.text_input("📧 Email", user["email"])
                            role = st.selectbox("🛠️ Rol", ["user", "admin"], index=0 if user["role"] == "user" else 1)
                            submitted = st.form_submit_button("🔁 Actualizar")
                            if submitted:
                                if not email:
                                    st.error("❌ El email es obligatorio.")
                                else:
                                    try:
                                        update_data = {"email": email, "role": role}
                                        result = update_user(user["email"], update_data)
                                        if result:
                                            st.success(f"✅ Usuario '{email}' actualizado correctamente.")
                                            st.session_state["msg"] = (f"Usuario '{email}' actualizado", "success")
                                            # cleanup
                                            st.session_state.pop("edit_target_user", None)
                                            st.rerun()
                                        else:
                                            st.error("❌ Error al actualizar el usuario.")
                                    except Exception as e:
                                        st.error(f"❌ Error al actualizar usuario: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error al cargar usuarios: {str(e)}")

        # ELIMINAR
        elif menu == "🗑️ Eliminar":
            target_email = st.session_state.get("delete_target_user", None)
            try:
                users = get_all_users() or []
                if not users:
                    st.warning("⚠️ No hay usuarios para eliminar.")
                else:
                    user_emails = [u["email"] for u in users]
                    selected = st.selectbox("Selecciona un usuario", ["-- seleccionar --"] + user_emails, index=0 if not target_email else (user_emails.index(target_email)+1))
                    if selected and selected != "-- seleccionar --":
                        st.warning(f"⚠️ Estás a punto de eliminar al usuario: **{selected}**")
                        confirm = confirm_action("¿Confirmas eliminar este usuario? Esta acción no se puede deshacer.", key=f"confirm_del_user_{selected}")
                        if confirm is True:
                            try:
                                result = delete_user(selected)
                                if result:
                                    st.success(f"✅ Usuario '{selected}' eliminado correctamente.")
                                    st.session_state.pop("delete_target_user", None)
                                    st.rerun()
                                else:
                                    st.error("❌ Error al eliminar el usuario.")
                            except Exception as e:
                                st.error(f"❌ Error al eliminar usuario: {str(e)}")
                        elif confirm is False:
                            st.info("Operación cancelada por el usuario.")
            except Exception as e:
                st.error(f"❌ Error al cargar usuarios: {str(e)}")

    # ---------------------------------------
    # ---------- ADMINISTRAR PRODUCTOS -------
    # ---------------------------------------
    elif seccion == "📦 Productos":
        st.subheader("📦 Administración de productos")
        st.caption("Operaciones CRUD para productos. Incluye buscador, export y análisis rápido.")

        show_message_from_state()

        menu = st.radio("Acción", ["📄 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"], horizontal=True)

        # LISTAR
        if menu == "📄 Listar":
            st.info("🗃️ Lista de productos (usa filtros para encontrar rápido).")
            try:
                products = product_service.get_all_products(limit=200) or []
                products_df = pd.DataFrame(products)
                # filtros basicos
                cols = st.columns([2,2,1])
                q_name = cols[0].text_input("🔎 Buscar nombre")
                q_cat = cols[1].text_input("🔎 Filtrar por categoría")
                if q_name:
                    products_df = products_df[products_df["name"].str.contains(q_name, case=False, na=False)]
                if q_cat:
                    products_df = products_df[products_df.get("category","").str.contains(q_cat, case=False, na=False)]
                if products_df.empty:
                    st.warning("⚠️ No hay productos que coincidan.")
                else:
                    st.write(f"**Total de productos:** {len(products_df)}")
                    st.dataframe(products_df[["name","price","stock","category"]].rename(columns={"name":"Nombre","price":"Precio","stock":"Stock","category":"Categoría"}))
                    st.download_button("⬇️ Exportar productos CSV", df_to_csv_bytes(products_df), file_name="productos.csv", mime="text/csv")
                    # manipulacion directa
                    for p in products:
                        with st.expander(f"📦 {p.get('name','sin nombre')} - ${p.get('price','0')}"):
                            st.markdown(f"**Stock:** `{p.get('stock','0')}`  \n**Categoría:** `{p.get('category','N/A')}`  \n**ID:** `{p.get('_id','')}`")
                            c1, c2 = st.columns([1,1])
                            if c1.button("✏️ Editar", key=f"edit_prod_{str(p.get('_id'))}"):
                                st.session_state["edit_product_id"] = str(p.get("_id"))
                                st.experimental_rerun()
                            if c2.button("🗑️ Eliminar", key=f"del_prod_{str(p.get('_id'))}"):
                                st.session_state["delete_product_id"] = str(p.get("_id"))
                                st.experimental_rerun()

            except Exception as e:
                st.error(f"❌ Error al cargar productos: {str(e)}")

        # CREAR
        elif menu == "➕ Crear":
            st.markdown("➕ **Crear producto nuevo** — completa los campos obligatorios.")
            with st.form("create_product", clear_on_submit=True):
                name = st.text_input("📛 Nombre", help="Nombre visible del producto.")
                description = st.text_area("📝 Descripción", help="Descripción breve que verá el usuario.")
                price = st.number_input("💲 Precio", min_value=0.0, step=0.1)
                stock = st.number_input("📦 Stock", min_value=0)
                category = st.text_input("📂 Categoría")
                submitted = st.form_submit_button("💾 Guardar")

                if submitted:
                    if not name or price <= 0:
                        st.error("❌ Nombre y precio válido son obligatorios.")
                    else:
                        try:
                            new_product = {"name": name, "description": description, "price": price, "stock": stock, "category": category}
                            result = product_service.create_product(new_product)
                            if result:
                                st.session_state["msg"] = (f"✅ Producto '{name}' creado correctamente", "success")
                                st.rerun()
                            else:
                                st.error("❌ Error al crear el producto.")
                        except Exception as e:
                            st.error(f"❌ Error al crear producto: {str(e)}")

        # EDITAR
        elif menu == "✏️ Editar":
            try:
                products = product_service.get_all_products(limit=200) or []
                if not products:
                    st.warning("⚠️ No hay productos para editar.")
                else:
                    options = [f"{p['name']} (ID:{str(p['_id'])[:8]})" for p in products]
                    selected = st.selectbox("Selecciona un producto", ["-- seleccionar --"] + options)
                    if selected and selected != "-- seleccionar --":
                        idx = options.index(selected)
                        product = products[idx]
                        with st.form("edit_product_form"):
                            st.write(f"**Editando:** {product['name']}")
                            name = st.text_input("📛 Nombre", product["name"])
                            description = st.text_area("📝 Descripción", product.get("description",""))
                            price = st.number_input("💲 Precio", min_value=0.0, step=0.1, value=float(product.get("price",0.0)))
                            stock = st.number_input("📦 Stock", min_value=0, value=int(product.get("stock",0)))
                            category = st.text_input("📂 Categoría", product.get("category",""))
                            submitted = st.form_submit_button("🔁 Actualizar")
                            if submitted:
                                if not name or price <= 0:
                                    st.error("❌ Nombre y precio válido son obligatorios.")
                                else:
                                    try:
                                        update_data = {"name": name, "description": description, "price": price, "stock": stock, "category": category}
                                        result = product_service.update_product(str(product["_id"]), update_data)
                                        if result:
                                            st.session_state["msg"] = (f"✅ Producto '{name}' actualizado correctamente", "success")
                                            st.rerun()
                                        else:
                                            st.error("❌ Error al actualizar el producto.")
                                    except Exception as e:
                                        st.error(f"❌ Error al actualizar producto: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error al cargar productos: {str(e)}")

        # ELIMINAR
        elif menu == "🗑️ Eliminar":
            try:
                products = product_service.get_all_products(limit=200) or []
                if not products:
                    st.warning("⚠️ No hay productos para eliminar.")
                else:
                    options = [f"{p['name']} (ID:{str(p['_id'])[:8]})" for p in products]
                    selected = st.selectbox("Selecciona un producto", ["-- seleccionar --"] + options)
                    if selected and selected != "-- seleccionar --":
                        idx = options.index(selected)
                        product = products[idx]
                        st.warning(f"⚠️ Estás a punto de eliminar el producto: **{product['name']}**")
                        confirm = confirm_action("¿Confirmas eliminar este producto?", key=f"confirm_del_prod_{product['_id']}")
                        if confirm is True:
                            try:
                                result = product_service.delete_product(str(product["_id"]))
                                if result:
                                    st.session_state["msg"] = (f"✅ Producto '{product['name']}' eliminado correctamente", "success")
                                    st.rerun()
                                else:
                                    st.error("❌ Error al eliminar el producto.")
                            except Exception as e:
                                st.error(f"❌ Error al eliminar producto: {str(e)}")
                        elif confirm is False:
                            st.info("Operación cancelada por el usuario.")
            except Exception as e:
                st.error(f"❌ Error al cargar productos: {str(e)}")

    # ---------------------------------------
    # ---------- ADMINISTRAR CATEGORÍAS ------
    # ---------------------------------------
    elif seccion == "📁 Categorías":
        st.subheader("📁 Administración de categorías")
        st.caption("Crea, edita, lista o elimina categorías. Útiles para agrupar productos.")

        menu = st.radio("Acción", ["📄 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"], horizontal=True)

        # LISTAR
        if menu == "📄 Listar":
            try:
                categorias = category_service.get_all_categories() or []
                if not categorias:
                    st.warning("⚠️ No hay categorías registradas todavía.")
                else:
                    st.write(f"**Total de categorías:** {len(categorias)}")
                    for c in categorias:
                        with st.expander(f"📁 {c['name']}"):
                            st.markdown(f"**Descripción:** {c.get('description','Sin descripción')}  \n**ID:** `{c.get('_id','')}`")
            except Exception as e:
                st.error(f"❌ Error al cargar categorías: {str(e)}")

        # CREAR
        elif menu == "➕ Crear":
            with st.form("create_category", clear_on_submit=True):
                name = st.text_input("📛 Nombre de la categoría")
                description = st.text_area("📝 Descripción (opcional)")
                submitted = st.form_submit_button("💾 Guardar")
                if submitted:
                    if not name:
                        st.error("❌ El nombre es obligatorio.")
                    else:
                        try:
                            new_category = {"name": name, "description": description}
                            result = category_service.create_category(new_category)
                            if result:
                                st.success(f"✅ Categoría '{name}' creada correctamente")
                                st.rerun()
                            else:
                                st.error("❌ Error al crear la categoría")
                        except Exception as e:
                            st.error(f"❌ Error al crear categoría: {str(e)}")

        # EDITAR
        elif menu == "✏️ Editar":
            try:
                categorias = category_service.get_all_categories() or []
                if not categorias:
                    st.warning("⚠️ No hay categorías para editar.")
                else:
                    names = [c["name"] for c in categorias]
                    selected = st.selectbox("Selecciona una categoría", ["-- seleccionar --"] + names)
                    if selected and selected != "-- seleccionar --":
                        categoria = next(c for c in categorias if c["name"] == selected)
                        with st.form("edit_category_form"):
                            name = st.text_input("📛 Nombre", categoria["name"])
                            description = st.text_area("📝 Descripción", categoria.get("description",""))
                            submitted = st.form_submit_button("🔁 Actualizar")
                            if submitted:
                                if not name:
                                    st.error("❌ El nombre es obligatorio.")
                                else:
                                    try:
                                        update_data = {"name": name, "description": description}
                                        result = category_service.update_category(str(categoria["_id"]), update_data)
                                        if result:
                                            st.success(f"✅ Categoría '{name}' actualizada correctamente")
                                            st.rerun()
                                        else:
                                            st.error("❌ Error al actualizar la categoría")
                                    except Exception as e:
                                        st.error(f"❌ Error al actualizar categoría: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error al cargar categorías: {str(e)}")

        # ELIMINAR
        elif menu == "🗑️ Eliminar":
            try:
                categorias = category_service.get_all_categories() or []
                if not categorias:
                    st.warning("⚠️ No hay categorías para eliminar.")
                else:
                    names = [c["name"] for c in categorias]
                    selected = st.selectbox("Selecciona una categoría", ["-- seleccionar --"] + names)
                    if selected and selected != "-- seleccionar --":
                        categoria = next(c for c in categorias if c["name"] == selected)
                        st.warning(f"⚠️ Estás a punto de eliminar la categoría: **{categoria['name']}**")
                        confirm = confirm_action("¿Confirmas eliminar esta categoría?", key=f"confirm_del_cat_{categoria['_id']}")
                        if confirm is True:
                            try:
                                result = category_service.delete_category(str(categoria["_id"]))
                                if result:
                                    st.success(f"✅ Categoría '{categoria['name']}' eliminada correctamente")
                                    st.rerun()
                                else:
                                    st.error("❌ Error al eliminar la categoría")
                            except Exception as e:
                                st.error(f"❌ Error al eliminar categoría: {str(e)}")
                        elif confirm is False:
                            st.info("Operación cancelada por el usuario.")
            except Exception as e:
                st.error(f"❌ Error al cargar categorías: {str(e)}")

    # ---------------------------------------
    # --------------- ANALYTICS -------------
    # ---------------------------------------
    elif seccion == "📊 Analytics":
        st.subheader("📊 Analytics y ML (placeholder)")
        st.caption("Sección para análisis básicos y para integrar regresión lineal / ML sobre datos del CRUD.")

        st.markdown(
            """
            Aquí puedes:
            - Descargar datos para analizarlos localmente.
            - Ejecutar análisis rápidos (promedios, distribución de precios, etc.).
            - Conectar un modelo de ML para predicción (ej: regresión lineal sobre precios).
            """
        )

        try:
            products = product_service.get_all_products(limit=500) or []
            if not products:
                st.warning("⚠️ No hay datos de productos para analizar.")
            else:
                df = pd.DataFrame(products)
                st.metric("Total productos", len(df))
                st.metric("Precio promedio", f"${df['price'].astype(float).mean():.2f}")
                st.write("Distribución de precios (tabla):")
                st.dataframe(df[["name","price","stock","category"]].rename(columns={"name":"Nombre","price":"Precio","stock":"Stock","category":"Categoría"}))

                with st.expander("🔎 Ejecutar regresión lineal (precio ~ stock) — quick test"):
                    run_reg = st.button("Ejecutar regresión simple")
                    if run_reg:
                        try:
                            import numpy as np
                            from numpy.linalg import lstsq
                            df_clean = df.dropna(subset=["price","stock"])
                            X = df_clean["stock"].astype(float).values.reshape(-1,1)
                            y = df_clean["price"].astype(float).values
                            if len(X) < 2:
                                st.warning("Insuficientes datos para regresión.")
                            else:
                                # añadir bias
                                A = np.hstack([X, np.ones_like(X)])
                                params, *_ = lstsq(A, y, rcond=None)
                                slope, intercept = params[0], params[1]
                                st.success(f"Modelo encontrado: price ≈ {slope:.4f} * stock + {intercept:.4f}")
                                st.info("Nota: esto es un ejemplo rápido; para producción usa scikit-learn y validación.")
                        except Exception as e:
                            st.error(f"❌ Error al ejecutar regresión: {e}")

                # export data
                st.download_button("⬇️ Descargar productos para análisis", df_to_csv_bytes(df), file_name="productos_analytics.csv", mime="text/csv")
        except Exception as e:
            st.error(f"❌ Error al obtener datos para analytics: {str(e)}")

    # Fin build frame
    # ----------------
