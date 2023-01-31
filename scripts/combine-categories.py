import pandas as pd
from pathlib import Path
from src.utils import get_project_root
from src.swinno_helpers import *

ROOT = get_project_root()

def clean_codes(input_df, code_digits, col):
    old = "(\d{code_digits})(?!\s+$)"
    new = "$1,"
    input_df[col] = input_df[col].replace(old, new, regex=True)
    return input_df

def check_duplicates(df, output_name, subset='sinno_id'):
    duplicates = df.loc[df.duplicated(subset=subset, keep=False),:]
    duplicates = duplicates.sort_values(by=subset)

    if duplicates.empty:
        print('No duplicates found.')
    else:
        print(f'{len(duplicates)} duplicates found.')
        df.to_csv(Path(ROOT, "data", "modified-data", f'{output_name}-duplicates.csv'))
        print(f'{output_name} written to csv.')

engine = connect_swinno_db()

for csv in Path(ROOT, "data", "raw-data").glob("*.csv"):

    file_name = Path(csv).stem

    print(f'****************** \n {file_name}')
   
    df = clean_import('csv', csv)
    df["sinno_id"] = df["sinno_id"].astype(int)
   
    cleaned_innovation_types = clean_codes(df, code_digits=3, col='innovation_type')
    cleaned_tags = clean_codes(df, code_digits=1, col='bioeconomy_vision')

    check_duplicates(cleaned_tags, output_name=file_name)

    split_innovation_types = split_cols(cleaned_tags, col_to_split='innovation_type', sep=',')
    melted_innovation_types = melt_table(split_innovation_types, id_vars='sinno_id', col_start='innovation', value_name='innovation_type')
    melted_innovation_types.to_sql(name = 'eco_innovations', con = engine, if_exists='append', echo=False)

    split_visions = split_cols(cleaned_tags, col_to_split='bioeconomy_visions', sep=',')
    melted_visions = melt_table(split_innovation_types, id_vars='sinno_id', col_start='bio', value_name='bioeconomy_vision')
    melted_visions.to_sql(name = 'bioeconomy_visions', con = engine, if_exists='append', echo=False)





