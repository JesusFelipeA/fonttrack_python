import streamlit as st
from backend.controllers.lugar_controller import (
    get_all_lugares,
    create_lugar,
    update_lugar,
    delete_lugar
)


def build_lugar_frame():
    st.title("📍 Gestión de Lugares")

    menu = st.radio(
        "Acción",
        ["📄 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"],
        horizontal=True
    )

    # --- LISTAR ---
    if menu == "📄 Listar":
        lugares = get_all_lugares()
        if not lugares:
            st.info("No hay lugares registrados aún.")
        else:
            for l in lugares:
                st.write(
                    f"🏠 **{l.get('nombre', 'Sin nombre')}** — "
                    f"Ubicación: {l.get('ubicacion', 'Sin ubicación')} — "
                    f"Tipo: {l.get('tipo', 'No especificado')}"
                )

    # --- CREAR ---
    elif menu == "➕ Crear":
        st.subheader("Agregar nuevo lugar")

        nombre = st.text_input("Nombre del lugar")
        ubicacion = st.text_input("Ubicación")
        tipo = st.text_input("Tipo de lugar (Ej. almacén, oficina, etc.)")
        descripcion = st.text_area("Descripción")

        if st.button("Guardar lugar"):
            nuevo = {
                "nombre": nombre,
                "ubicacion": ubicacion,
                "tipo": tipo,
                "descripcion": descripcion
            }
            create_lugar(nuevo)
            st.success("✅ Lugar agregado correctamente.")
            st.rerun()

    # --- EDITAR ---
    elif menu == "✏️ Editar":
        lugares = get_all_lugares()
        if not lugares:
            st.warning("No hay lugares para editar.")
            return

        selected = st.selectbox(
            "Selecciona el lugar",
            [l.get("nombre", "Sin nombre") for l in lugares]
        )
        lugar = next((l for l in lugares if l.get("nombre") == selected), None)

        if lugar:
            nuevo_nombre = st.text_input("Nombre", lugar.get("nombre", ""))
            nueva_ubicacion = st.text_input("Ubicación", lugar.get("ubicacion", ""))
            nuevo_tipo = st.text_input("Tipo", lugar.get("tipo", ""))
            nueva_descripcion = st.text_area("Descripción", lugar.get("descripcion", ""))

            if st.button("Actualizar"):
                datos = {
                    "nombre": nuevo_nombre,
                    "ubicacion": nueva_ubicacion,
                    "tipo": nuevo_tipo,
                    "descripcion": nueva_descripcion
                }
                update_lugar(lugar["_id"], datos)
                st.success("✅ Lugar actualizado correctamente.")
                st.rerun()

    # --- ELIMINAR ---
    elif menu == "🗑️ Eliminar":
        lugares = get_all_lugares()
        if not lugares:
            st.warning("No hay lugares para eliminar.")
            return

        selected = st.selectbox(
            "Selecciona el lugar a eliminar",
            [l.get("nombre", "Sin nombre") for l in lugares]
        )
        lugar = next((l for l in lugares if l.get("nombre") == selected), None)

        if lugar and st.button("Eliminar"):
            delete_lugar(lugar["_id"])
            st.success("🗑️ Lugar eliminado correctamente.")
            st.rerun()
