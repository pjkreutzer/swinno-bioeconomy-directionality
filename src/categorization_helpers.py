import pandas as pd
from pathlib import Path


def clean_codes(input_df, code_digits, col):
    old = r"(\d{{}})(?!\s+$)".format(code_digits)
    new = "$1,"
    input_df[col] = input_df[col].replace(old, new, regex=True).str.strip()
    return input_df


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
