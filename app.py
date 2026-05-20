import streamlit as st

from utils.config_loader import load_config
from utils.form_generator import render_form
from utils.data_manager import (
    initialize_data_file,
    save_record,
    load_data,
    update_record
)

# -----------------------------
# LOAD CONFIG
# -----------------------------
config = load_config("config.xlsx")

# -----------------------------
# INIT DATA FILE
# -----------------------------
initialize_data_file(config)

# -----------------------------
# TITLE
# -----------------------------
st.title("Vulnerabilidades Laguna Seca")

# -----------------------------
# FORM
# -----------------------------
st.header("Ingreso de Nuevo Registro")

with st.form("create_form"):

    form_data = render_form(
        config,
        form_key_prefix="create"
    )

    submitted_create = st.form_submit_button(
        "Guardar"
    )

if submitted_create:

    save_record(form_data)

    st.success("Registro guardado correctamente")
    
    st.rerun()


# -----------------------------
# LOAD DATA
# -----------------------------
df = load_data()

# -----------------------------
# SHOW DATA
# -----------------------------
st.header("Lista de Registros")

display_df = df.copy()
display_df = display_df.fillna("")

st.dataframe(display_df)

    
# -----------------------------
# EDITION
# -----------------------------
st.header("Editar Registro")

if not df.empty:

    selected_id = st.selectbox(
        "Seleccionar ID",
        df["id"].tolist(),
        key="selected_id_edit"
    )

    selected_row = df[df["id"] == selected_id].iloc[0]

    existing_data = selected_row.to_dict()

    with st.form("edit_form"):

        edited_data = render_form(
            config,
            existing_data=existing_data,
            form_key_prefix="edit"
        )

        submitted_edit = st.form_submit_button(
            "Actualizar Registro"
        )

    if submitted_edit:

        update_record(
            selected_id,
            edited_data
        )

        st.success("Registro actualizado")

        st.rerun()

