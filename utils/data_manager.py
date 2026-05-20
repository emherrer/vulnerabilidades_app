import pandas as pd
import os


DATA_FILE = "data.xlsx"


def _normalize_value(value, dtype=None):

    if isinstance(value, str) and value.strip() == "":
        if dtype is not None and dtype.kind == "M":
            return pd.NaT
        return pd.NA if dtype is not None and dtype.kind in "biufc" else ""

    if hasattr(value, "year"):
        return pd.to_datetime(value)

    if dtype is not None and dtype.kind in "biufc" and isinstance(value, str):
        return pd.to_numeric(value, errors="coerce")

    return value


def initialize_data_file(config):

    if os.path.exists(DATA_FILE):
        return

    columns = []

    for field in config:
        columns.append(field["internal_name"])

    df = pd.DataFrame(columns=columns)

    df.to_excel(DATA_FILE, index=False, engine="openpyxl")


def load_data():

    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()

    if os.path.getsize(DATA_FILE) == 0:
        os.remove(DATA_FILE)
        return pd.DataFrame()

    try:
        return pd.read_excel(DATA_FILE, engine="openpyxl")
    except (ValueError, OSError):
        os.remove(DATA_FILE)
        return pd.DataFrame()


def get_next_id(df):

    if df.empty:
        return 1

    return int(df["id"].max()) + 1


def save_record(form_data):

    df = load_data()

    form_data["id"] = get_next_id(df)

    for column, value in form_data.items():

        if hasattr(value, "year"):
            form_data[column] = pd.to_datetime(value)
    
    new_df = pd.DataFrame([form_data])

    df = pd.concat(
        [df, new_df],
        ignore_index=True
    )

    df.to_excel(DATA_FILE, index=False, engine="openpyxl")
    

def update_record(record_id, updated_data):

    df = load_data()

    for column, value in updated_data.items():

        if column not in df.columns:
            continue

        value = _normalize_value(value, df[column].dtype)

        df.loc[df["id"] == record_id, column] = value

    df.to_excel(DATA_FILE, index=False, engine="openpyxl")