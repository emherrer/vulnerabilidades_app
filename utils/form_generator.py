import streamlit as st
from datetime import datetime
import pandas as pd


def render_form(config, existing_data=None, form_key_prefix="form"):

    form_data = {}

    for field in config:

        field_name = field["internal_name"]
        display_name = field["display_name"]
        field_type = field["type"]
        options = field["options"]

        # IGNORAR AUTO
        if field_type == "auto":
            continue

        # VALOR EXISTENTE
        current_value = None

        if existing_data is not None:
            current_value = existing_data.get(field_name)

        # SELECT
        if field_type == "select":

            index = 0

            if current_value in options:
                index = options.index(current_value)

            value = st.selectbox(
                display_name,
                options,
                index=index,
                key=f"{form_key_prefix}_{sanitize_key(field_name)}"
            )

        # TEXT
        elif field_type == "text":

            value = st.text_input(
                display_name,
                value=current_value if current_value else "",
                key=f"{form_key_prefix}_{sanitize_key(field_name)}"
            )

        # TEXTAREA
        elif field_type == "textarea":

            value = st.text_area(
                display_name,
                value=current_value if current_value else "",
                key=f"{form_key_prefix}_{sanitize_key(field_name)}"
            )

        # DATE
        elif field_type == "date":

        # MANEJO DE FECHAS VACIAS
            if pd.isna(current_value):

                current_value = datetime.today()

        # SI ES TIMESTAMP → DATE
            elif isinstance(current_value, pd.Timestamp):

                current_value = current_value.date()

            value = st.date_input(
                display_name,
                value=current_value,
                key=f"{form_key_prefix}_{sanitize_key(field_name)}"
            )

        # NUMBER
        elif field_type == "number":

            value = st.number_input(
                display_name,
                value=float(current_value) if current_value else 0.0,
                key=f"{form_key_prefix}_{sanitize_key(field_name)}"
            )

        else:

            value = st.text_input(
                display_name,
                value=current_value if current_value else "",
                key=f"{form_key_prefix}_{sanitize_key(field_name)}"
            )

        form_data[field_name] = value

    return form_data


def sanitize_key(text):

    return (
        str(text)
        .strip()
        .lower()
        .replace(" ", "_")
    )