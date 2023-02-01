import pandas as pd
from src.utils import get_project_root
from src.categorization_helpers import *
from src.swinno_helpers import *

ROOT = get_project_root()
 

engine = connect_swinno_db()

list_innovation_type_df = []
list_visions_df = []
list_notes_df = []

for csv in Path(ROOT, "data", "raw-data", "tags").glob("*.csv"):

    file_name = Path(csv).stem

    print(f"****************** \n {file_name}")

    df = clean_import("csv", csv)
    df.dropna(subset="sinno_id", inplace=True)
    df["sinno_id"] = df["sinno_id"].astype(int)
    replaced_letters = replace_letters_codes(df, "bioeconomy_vision")

    cleaned_innovation_types = clean_codes(replaced_letters, code_digits=3, col="innovation_type")
    list_innovation_type_df.append(
        cleaned_innovation_types.loc[
            :,
            ["sinno_id", "innovation_type"],
        ]
    )

    cleaned_tags = clean_codes(df, code_digits=1, col="bioeconomy_vision")

    list_visions_df.append(cleaned_tags.loc[:, ["sinno_id", "bioeconomy_vision"]])

    notes = df[["sinno_id", "notes"]]
    list_notes_df.append(notes)

combined_innovation_types = pd.concat(list_innovation_type_df)
combined_visions = pd.concat(list_visions_df)
combined_notes = pd.concat(list_notes_df)

combined_innovation_types.name = "combined_innovation_types"
combined_visions.name = "combined_visions"
combined_notes.name = "combined_notes"

for combined_df in [combined_innovation_types, combined_notes, combined_visions]:
    csv_path = Path(ROOT, "data", "modified-data", f"{combined_df.name}-duplicates.csv")
    check_duplicates(combined_df, output_name=combined_df.name, output_path=csv_path)
    print("-" * 5)


split_visions = split_cols(combined_visions, col_to_split="bioeconomy_vision", sep=",")
melted_visions = melt_table(
    split_visions, id_vars="sinno_id", col_start="bio", value_name="bioeconomy_vision"
)
melted_visions = melted_visions.dropna()
melted_visions.to_sql(name='bioeconomy_visions', con=engine, if_exists='replace', index=False)

split_innovation_types = split_cols(
    combined_innovation_types, col_to_split="innovation_type", sep=","
)
melted_innovation_types = melt_table(
    split_innovation_types,
    id_vars="sinno_id",
    col_start="innovation",
    value_name="innovation_type",
)
melted_innovation_types.dropna()
melted_innovation_types.to_sql(name='eco_innovations', con=engine, if_exists='replace', index=False)

combined_notes = combined_notes.dropna()
combined_notes.to_sql(name='categorization_notes', con=engine, index=False, if_exists='replace')
