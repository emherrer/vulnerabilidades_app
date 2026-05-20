import pandas as pd


def load_config(file_path="config.xlsx"):

    raw_df = pd.read_excel(
        file_path,
        sheet_name="campos",
        header=None
    )

    config = []

    columns = raw_df.columns

    for col in columns:

        internal_name = raw_df.iloc[0, col]
        display_name = raw_df.iloc[1, col]
        field_type = raw_df.iloc[2, col]

        options = raw_df.iloc[3:, col].dropna().tolist()

        field = {
            "internal_name": internal_name,
            "display_name": display_name,
            "type": field_type,
            "options": options
        }

        config.append(field)

    return config