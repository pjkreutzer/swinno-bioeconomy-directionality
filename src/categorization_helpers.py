import pandas as pd
from pathlib import Path
import re


def clean_codes(df, column, code_digits, remove_whitespace=True, drop_na=True):
    if drop_na:
        df = df.dropna(subset=[column])

    df.loc[:, column] = df[column].astype(str)

    df.loc[:, column] = df[column].apply(
        lambda x: re.sub(r"\b(0)\b", r"0" * code_digits, x)
    )
    df.loc[:, column] = df[column].apply(
        lambda x: re.sub(r"\b(9)\b", r"9" * code_digits, x)
    )

    df.loc[:, column] = df[column].apply(
        lambda x: re.sub(rf"(\d{ {code_digits} })(?!$)", r"\1,", str(x))
    )

    if remove_whitespace:
        df.loc[:, column] = df[column].apply(lambda x: re.sub(r"\s", "", x))
        df.loc[:, column] = df[column].str.strip()

    return df


def replace_letters_codes(input_df, col):
    d = {"A": "1", "B": "2", "C": "3"}
    input_df[col] = input_df[col].str.replace(
        "(A|B|C)", lambda x: d[x.group()], regex=True
    )
    return input_df


def check_duplicates(df, output_name, output_path, subset="sinno_id"):
    duplicates = df.loc[df.duplicated(subset=subset, keep=False), :]
    duplicates = duplicates.sort_values(by=subset)

    if duplicates.empty:
        print("No duplicates found.")
    else:
        print(f"{len(duplicates)} duplicates found.")
        df.to_csv(output_path)
        print(f"{output_name} written to csv.")
