import streamlit as st
from datetime import datetime

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
# SESSION STATE
# -----------------------------
if "success_message" not in st.session_state:
    st.session_state.success_message = None

# -----------------------------
# TITLE
# -----------------------------
st.title("Vulnerabilidades Laguna Seca")

# -----------------------------
# LOAD DATA
# -----------------------------
df = load_data()

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

    st.session_state.success_message = "Registro guardado correctamente"
    
    # RECARGAR DATOS
    df = load_data()

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
        st.session_state.success_message = "Registro actualizado"
        
        # RECARGAR DATOS
        df = load_data()
        
# -----------------------------
# SHOW SUCCESS MESSAGE
# -----------------------------
if st.session_state.success_message:

    st.success(st.session_state.success_message)

    # LIMPIAR DESPUÉS DE MOSTRAR
    st.session_state.success_message = None
    
# -----------------------------
# SHOW DATA
# -----------------------------
st.header("Lista de Registros")

display_df = df.copy()
display_df = display_df.fillna("")

st.dataframe(display_df)