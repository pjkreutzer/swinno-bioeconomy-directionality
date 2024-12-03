import sqlite3
import pandas as pd


def unite(df, old_col_start: str, new_col_name: str, position: str):
    temp_df = df
    col_list = [col for col in temp_df if col.startswith(old_col_start)]
    temp_col = temp_df[col_list].astype(str).apply(lambda x: x.str.cat(sep=""), axis=1)
    temp_df = temp_df.drop(columns=col_list)
    temp_df.insert(loc=position, column=new_col_name, value=temp_col)

    return temp_df


db = sqlite3.connect("C:\\Users\ph8148kr\OneDrive - Lund University/research/swinno.db")

df = pd.read_sql(
    "SELECT [SINNO ID], [Use sectors],  [Use sector 2], [Use sector 3],[Use sector 4], [Use sector 5], [Use sector 6], [Use sector 7], [Use sector 8], [Use sector 9], [Literal name of innovating firm ; SINNO's common name ; SINNO ID], [Innovation name in Swedish], [Description in Swedish], [Additional information if Origin = New scientific discovery],[Additional information if Origin = New technologies or materials], [Additional info if Origin = Official regulation, legislation and standards.], [Additional information if Origin = Solution for a problem.], [Additional information if Origin = Performance], [Additional information if Origin = Other] FROM innovation",
    db,
)

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

sni_codes = [
    "01",
    "02",
    "13",
    "16",
    "17",
    "18",
    "20",
    "38",
    "41",
]

df = unite(df, "use", "use_sectors", position=1)
df = unite(df, "add", "info", position=5)

filtered_df = df[df["use_sectors"].isin(sni_codes)]

filtered_df.to_excel(
    "data/modified-data/filtered_swinno_1.xlsx", encoding="utf-8-sig", index=False
)
