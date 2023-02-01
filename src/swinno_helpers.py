import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from src.utils import get_project_root


def split_cols(df, col_to_split: str, sep: str):
    """Splits columns that have joined information (e.g., SNI codes)

    Args:
        df (pd.DataFrame): The data frame in which the split should occur
        col_to_split (str): The name of the column to split

    Returns:
        pd.DataFrame: A new data frame with the original column content split into new columns and the original column removed.
    """
    temp_df = df
    split_cols = (
        temp_df.loc[:, col_to_split]
        .astype(str)
        .str.strip()
        .str.split(sep, expand=True)
        .fillna(np.nan)
    )

    for col in split_cols:
        temp_df[f"{col_to_split}_{col}"] = split_cols.loc[:, col]

    temp_df.drop(labels=col_to_split, axis=1, inplace=True)

    return temp_df


def melt_table(df, id_vars: str, col_start: str, value_name: str, **kwargs):
    """Melts tables into lookup tables

    Args:
        df (pd.DataFrame): The dataframe to melt
        id_vars (str): Variables to keep as ids
        col_start (str): The start of the columns to select
        value_name (str): The name of the value column in the melted table

    Returns:
        df (pd.DataFrame): Melted dataframe
    """
    temp_df = df.melt(
        id_vars=id_vars,
        value_vars=df.columns[df.columns.str.startswith(col_start)],
        value_name=value_name,
    )

    temp_df.drop("variable", axis=1, inplace=True)
    temp_df.dropna(inplace=True)

    temp_df = temp_df.sort_values(by=id_vars).reset_index(drop=True)

    return temp_df



def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def clean_import(file_type, file_path, **kwargs):

    if file_type == "csv":
        df = pd.read_csv(file_path, **kwargs)

    elif file_type == "xlsx":
        df = pd.read_excel(file_path, **kwargs)

    else:
        raise ValueError("Unsupported file type")

    df = clean_column_names(df)
    return df

def connect_swinno_db():

    database_dir = get_project_root().parent.absolute()
    database_uri = f"sqlite:///{database_dir}/swinno.db"
    engine = create_engine(database_uri)
    return engine