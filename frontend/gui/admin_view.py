import streamlit as st
import pandas as pd

# -------------------------
# CONTROLADORES

from backend.controllers.user_controller import (
    get_all_users, create_user, update_user, delete_user
)
from backend.controllers.material_controller import (
    get_all_material, create_material, update_material, delete_material
)
from backend.controllers.lugar_controller import (
    get_all_lugares, create_lugar, update_lugar, delete_lugar
)

# Vista del perfil de usuario
from frontend.gui.user_view import build_user_frame


# -------------------------
# UTILIDADES INTERNAS UI
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
# FUNCIONES DE ADMINISTRACIÓN
# -------------------------
def administrar_usuarios():
    """Administración completa de usuarios"""
    st.subheader("👤 Administración de usuarios")
    show_message_from_state()

    menu = st.radio(
        "Acción",
        ["📄 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar", "👁️ Ver perfil"],
        horizontal=True
    )

    # VER PERFIL
    if menu == "👁️ Ver perfil":
        build_user_frame()

    # LISTAR
    elif menu == "📄 Listar":
        try:
            users = get_all_users() or []
            df = pd.DataFrame(users)
            if df.empty:
                st.warning("⚠️ No hay usuarios registrados.")
            else:
                st.dataframe(df)
                st.download_button(
                    "⬇️ Exportar usuarios CSV",
                    df_to_csv_bytes(df),
                    "usuarios.csv",
                    "text/csv"
                )
        except Exception as e:
            st.error(f"❌ Error al listar usuarios: {e}")

    # CREAR
    elif menu == "➕ Crear":
        with st.form("form_user", clear_on_submit=True):
            correo = st.text_input("Correo electrónico")
            role = st.selectbox("Rol", ["user", "admin"])
            password = st.text_input("Contraseña", type="password")
            confirm = st.text_input("Confirmar contraseña", type="password")
            submit = st.form_submit_button("💾 Guardar")

            if submit:
                if not correo or not password:
                    st.error("El correo y la contraseña son obligatorios.")
                elif password != confirm:
                    st.warning("Las contraseñas no coinciden.")
                else:
                    try:
                        create_user({"correo": correo, "role": role, "password": password})
                        st.success(f"Usuario '{correo}' creado correctamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al crear usuario: {e}")

    # EDITAR
    elif menu == "✏️ Editar":
        try:
            users = get_all_users() or []
            if not users:
                st.warning("⚠️ No hay usuarios para editar.")
            else:
                correos = [u["correo"] for u in users]
                selected = st.selectbox("Selecciona usuario", ["-- seleccionar --"] + correos)
                if selected != "-- seleccionar --":
                    user = next(u for u in users if u["correo"] == selected)
                    with st.form("edit_user_form"):
                        correo = st.text_input("Correo", user["correo"])
                        role = st.selectbox("Rol", ["user", "admin"], index=0 if user["role"] == "user" else 1)
                        submit = st.form_submit_button("Actualizar")
                        if submit:
                            update_user(user["correo"], {"correo": correo, "role": role})
                            st.success(f"Usuario '{correo}' actualizado.")
                            st.rerun()
        except Exception as e:
            st.error(f"Error al editar usuario: {e}")

    # ELIMINAR
    elif menu == "🗑️ Eliminar":
        try:
            users = get_all_users() or []
            if not users:
                st.warning("⚠️ No hay usuarios para eliminar.")
            else:
                correos = [u["correo"] for u in users]
                selected = st.selectbox("Selecciona usuario", ["-- seleccionar --"] + correos)
                if selected != "-- seleccionar --":
                    st.warning(f"¿Eliminar usuario '{selected}'?")
                    confirm = confirm_action("Confirmar eliminación", f"confirm_user_{selected}")
                    if confirm:
                        delete_user(selected)
                        st.success(f"Usuario '{selected}' eliminado.")
                        st.rerun()
        except Exception as e:
            st.error(f"Error al eliminar usuario: {e}")


def administrar_materiales():
    """Administración completa de materiales"""
    st.subheader("🧱 Administración de materiales")
    show_message_from_state()

    menu = st.radio("Acción", ["📄 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"], horizontal=True)

    # LISTAR
    if menu == "📄 Listar":
        try:
            materials = get_all_material() or []
            df = pd.DataFrame(materials)
            if df.empty:
                st.warning("⚠️ No hay materiales registrados.")
            else:
                st.dataframe(df)
                st.download_button("⬇️ Exportar materiales CSV", df_to_csv_bytes(df), "materiales.csv", "text/csv")
        except Exception as e:
            st.error(f"❌ Error al listar materiales: {e}")

    # CREAR
    elif menu == "➕ Crear":
        with st.form("create_material", clear_on_submit=True):
            nombre = st.text_input("Nombre del material")
            descripcion = st.text_area("Descripción")
            cantidad = st.number_input("Cantidad", min_value=0, step=1)
            unidad = st.text_input("Unidad de medida")
            submitted = st.form_submit_button("💾 Guardar")

            if submitted:
                if not nombre:
                    st.error("El nombre es obligatorio.")
                else:
                    try:
                        create_material({
                            "nombre": nombre,
                            "descripcion": descripcion,
                            "cantidad": cantidad,
                            "unidad": unidad
                        })
                        st.success(f"✅ Material '{nombre}' creado correctamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al crear material: {e}")

    # EDITAR
    elif menu == "✏️ Editar":
        try:
            materials = get_all_material() or []
            if not materials:
                st.warning("⚠️ No hay materiales para editar.")
            else:
                names = [m["nombre"] for m in materials]
                selected = st.selectbox("Selecciona un material", ["-- seleccionar --"] + names)
                if selected and selected != "-- seleccionar --":
                    material = next(m for m in materials if m["nombre"] == selected)
                    with st.form("edit_material"):
                        nombre = st.text_input("Nombre", material["nombre"])
                        descripcion = st.text_area("Descripción", material.get("descripcion", ""))
                        cantidad = st.number_input("Cantidad", min_value=0, step=1, value=int(material.get("cantidad", 0)))
                        unidad = st.text_input("Unidad", material.get("unidad", ""))
                        submitted = st.form_submit_button("🔁 Actualizar")
                        if submitted:
                            update_material(material["id"], {
                                "nombre": nombre,
                                "descripcion": descripcion,
                                "cantidad": cantidad,
                                "unidad": unidad
                            })
                            st.success(f"✅ Material '{nombre}' actualizado.")
                            st.rerun()
        except Exception as e:
            st.error(f"Error al editar material: {e}")

    # ELIMINAR
    elif menu == "🗑️ Eliminar":
        try:
            materials = get_all_material() or []
            if not materials:
                st.warning("⚠️ No hay materiales para eliminar.")
            else:
                names = [m["nombre"] for m in materials]
                selected = st.selectbox("Selecciona un material", ["-- seleccionar --"] + names)
                if selected and selected != "-- seleccionar --":
                    material = next(m for m in materials if m["nombre"] == selected)
                    st.warning(f"⚠️ Estás por eliminar el material '{material['nombre']}'")
                    confirm = confirm_action("¿Confirmas eliminar este material?", f"confirm_del_mat_{material['id']}")
                    if confirm:
                        delete_material(material["id"])
                        st.success(f"✅ Material '{material['nombre']}' eliminado.")
                        st.rerun()
        except Exception as e:
            st.error(f"Error al eliminar material: {e}")


def administrar_lugares():
    """Administración completa de lugares"""
    st.subheader("📍 Administración de lugares")
    show_message_from_state()

    menu = st.radio("Acción", ["📄 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"], horizontal=True)

    # LISTAR
    if menu == "📄 Listar":
        try:
            lugares = get_all_lugares() or []
            df = pd.DataFrame(lugares)
            if df.empty:
                st.warning("⚠️ No hay lugares registrados.")
            else:
                st.dataframe(df)
                st.download_button("⬇️ Exportar lugares CSV", df_to_csv_bytes(df), "lugares.csv", "text/csv")
        except Exception as e:
            st.error(f"❌ Error al listar lugares: {e}")

    # CREAR
    elif menu == "➕ Crear":
        with st.form("create_lugar", clear_on_submit=True):
            nombre = st.text_input("Nombre del lugar")
            ubicacion = st.text_input("Ubicación")
            tipo = st.text_input("Tipo")
            descripcion = st.text_area("Descripción")
            submitted = st.form_submit_button("💾 Guardar")

            if submitted:
                if not nombre:
                    st.error("El nombre es obligatorio.")
                else:
                    try:
                        create_lugar({
                            "nombre": nombre,
                            "ubicacion": ubicacion,
                            "tipo": tipo,
                            "descripcion": descripcion
                        })
                        st.success(f"✅ Lugar '{nombre}' creado correctamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al crear lugar: {e}")

    # EDITAR
    elif menu == "✏️ Editar":
        try:
            lugares = get_all_lugares() or []
            if not lugares:
                st.warning("⚠️ No hay lugares para editar.")
            else:
                names = [l["nombre"] for l in lugares]
                selected = st.selectbox("Selecciona un lugar", ["-- seleccionar --"] + names)
                if selected and selected != "-- seleccionar --":
                    lugar = next(l for l in lugares if l["nombre"] == selected)
                    with st.form("edit_lugar"):
                        nombre = st.text_input("Nombre", lugar["nombre"])
                        ubicacion = st.text_input("Ubicación", lugar.get("ubicacion", ""))
                        tipo = st.text_input("Tipo", lugar.get("tipo", ""))
                        descripcion = st.text_area("Descripción", lugar.get("descripcion", ""))
                        submitted = st.form_submit_button("🔁 Actualizar")
                        if submitted:
                            update_lugar(lugar["_id"], {
                                "nombre": nombre,
                                "ubicacion": ubicacion,
                                "tipo": tipo,
                                "descripcion": descripcion
                            })
                            st.success(f"✅ Lugar '{nombre}' actualizado.")
                            st.rerun()
        except Exception as e:
            st.error(f"Error al editar lugar: {e}")

    # ELIMINAR
    elif menu == "🗑️ Eliminar":
        try:
            lugares = get_all_lugares() or []
            if not lugares:
                st.warning("⚠️ No hay lugares para eliminar.")
            else:
                names = [l["nombre"] for l in lugares]
                selected = st.selectbox("Selecciona un lugar", ["-- seleccionar --"] + names)
                if selected and selected != "-- seleccionar --":
                    lugar = next(l for l in lugares if l["nombre"] == selected)
                    st.warning(f"⚠️ Estás por eliminar el lugar '{lugar['nombre']}'")
                    confirm = confirm_action("¿Confirmas eliminar este lugar?", f"confirm_del_lug_{lugar['_id']}")
                    if confirm:
                        delete_lugar(lugar["_id"])
                        st.success(f"✅ Lugar '{lugar['nombre']}' eliminado.")
                        st.rerun()
        except Exception as e:
            st.error(f"Error al eliminar lugar: {e}")


def mostrar_analytics():
    """Muestra la sección de analytics"""
    st.subheader("📊 Analytics — vista preliminar")
    st.info("Esta sección se actualizará con análisis sobre materiales, usuarios y lugares.")


# -------------------------
# PANEL DE ADMINISTRACIÓN PRINCIPAL
# -------------------------
def build_admin_frame():
    st.set_page_config(page_title="Panel de administración", layout="wide")
    st.title("⚙️ Panel de administración")

    seccion = st.radio(
        "¿Qué deseas administrar?",
        ["👤 Usuarios", "🧱 Materiales", "📍 Lugares", "📊 Analytics"],
        horizontal=True
    )

    # Ejecutar la sección correspondiente
    if seccion == "👤 Usuarios":
        administrar_usuarios()
    elif seccion == "🧱 Materiales":
        administrar_materiales()
    elif seccion == "📍 Lugares":
        administrar_lugares()
    elif seccion == "📊 Analytics":
        mostrar_analytics()