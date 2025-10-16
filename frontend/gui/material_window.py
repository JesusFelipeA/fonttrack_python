# frontend/gui/material_window.py

import streamlit as st
from backend.controllers.material_controller import (
    get_all_material as get_all_materials,
    create_material,
    update_material,
    delete_material
)


def build_material_frame():
    st.title("📦 Gestión de Materiales")

    menu = st.radio(
        "Acción",
        ["📄 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"],
        horizontal=True
    )

    # --- LISTAR ---
    if menu == "📄 Listar":
        materials = get_all_materials()
        if not materials:
            st.info("No hay materiales registrados aún.")
        else:
            for mat in materials:
                st.write(
                    f"**{mat.get('descripcion', 'Sin descripción')}** — "
                    f"{mat.get('clasificacion', 'Sin clasificación')} — "
                    f"{mat.get('existencia', 0)} unidades"
                )

    # --- CREAR ---
    elif menu == "➕ Crear":
        st.subheader("Agregar nuevo material")

        clave_material = st.text_input("Clave del material")
        descripcion = st.text_input("Descripción")
        generico = st.text_input("Genérico")
        clasificacion = st.text_input("Clasificación")
        existencia = st.number_input("Existencia inicial", min_value=0, step=1)
        costo_promedio = st.number_input("Costo promedio", min_value=0.0, step=0.1)
        lugar_id = st.text_input("ID del lugar")

        if st.button("Guardar material"):
            nuevo = {
                "clave_material": clave_material,
                "descripcion": descripcion,
                "generico": generico,
                "clasificacion": clasificacion,
                "existencia": existencia,
                "costo_promedio": costo_promedio,
                "lugar_id": lugar_id
            }
            create_material(nuevo)
            st.success("✅ Material agregado correctamente.")
            st.rerun()

    # --- EDITAR ---
    elif menu == "✏️ Editar":
        materials = get_all_materials()
        if not materials:
            st.warning("No hay materiales para editar.")
            return

        selected = st.selectbox(
            "Selecciona el material",
            [m.get("descripcion", "Sin descripción") for m in materials]
        )
        mat = next((m for m in materials if m.get("descripcion") == selected), None)

        if mat:
            nueva_clave = st.text_input("Clave del material", mat.get("clave_material", ""))
            nueva_descripcion = st.text_input("Descripción", mat.get("descripcion", ""))
            nuevo_generico = st.text_input("Genérico", mat.get("generico", ""))
            nueva_clasificacion = st.text_input("Clasificación", mat.get("clasificacion", ""))
            nueva_existencia = st.number_input("Existencia", value=int(mat.get("existencia", 0)), step=1)
            nuevo_costo = st.number_input("Costo promedio", value=float(mat.get("costo_promedio", 0.0)), step=0.1)
            nuevo_lugar = st.text_input("ID del lugar", mat.get("lugar_id", ""))

            if st.button("Actualizar"):
                datos = {
                    "clave_material": nueva_clave,
                    "descripcion": nueva_descripcion,
                    "generico": nuevo_generico,
                    "clasificacion": nueva_clasificacion,
                    "existencia": nueva_existencia,
                    "costo_promedio": nuevo_costo,
                    "lugar_id": nuevo_lugar
                }
                update_material(mat["_id"], datos)
                st.success("✅ Material actualizado correctamente.")
                st.rerun()

    # --- ELIMINAR ---
    elif menu == "🗑️ Eliminar":
        materials = get_all_materials()
        if not materials:
            st.warning("No hay materiales para eliminar.")
            return

        selected = st.selectbox(
            "Selecciona el material a eliminar",
            [m.get("descripcion", "Sin descripción") for m in materials]
        )
        mat = next((m for m in materials if m.get("descripcion") == selected), None)

        if mat and st.button("Eliminar"):
            delete_material(mat["_id"])
            st.success("🗑️ Material eliminado correctamente.")
            st.rerun()
