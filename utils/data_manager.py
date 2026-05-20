import pandas as pd
import os


DATA_FILE = "data.xlsx"


def initialize_data_file(config):

    if os.path.exists(DATA_FILE):
        return

    columns = []

    for field in config:
        columns.append(field["internal_name"])

    df = pd.DataFrame(columns=columns)

    df.to_excel(DATA_FILE, index=False)


def load_data():

    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()

    return pd.read_excel(DATA_FILE)


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

    df.to_excel(DATA_FILE, index=False)
    

def update_record(record_id, updated_data):

    df = load_data()

    for column, value in updated_data.items():

        # CONVERTIR FECHAS
        if hasattr(value, "year"):
            value = pd.to_datetime(value)

        df.loc[df["id"] == record_id, column] = value

    df.to_excel(DATA_FILE, index=False)