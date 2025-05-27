import pandas as pd
import os

def create_df(columns):
    df = pd.DataFrame(columns=columns)
    return df

def add_row(df, row):
    row = pd.DataFrame([row])
    df = pd.concat([df, row], ignore_index=True)
    return df

def add_rows(df, rows):
    for row in rows:
        row = pd.DataFrame([row])
        df = pd.concat([df, row], ignore_index=True)
    return df

def save_df(df, main_dir, file_name, sheet_name):
    file_path = main_dir + "\\" + file_name
    if os.path.exists(file_path):
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        df.to_excel(file_path, sheet_name=sheet_name, index=False, engine="openpyxl")