# | label: Imports

import pandas as pd
import numpy as np
from pathlib import Path
from src.figures import *
from src.utils import get_project_root, format_table
from src.swinno_helpers import connect_swinno_db

ROOT = get_project_root()
conn = connect_swinno_db()

# set all text on plots to be monospace with rcParams
plt.rcParams["font.family"] = "Space Grotesk"

sns.set_theme(style="white")

# full code labels for merging


codes_df = pd.read_sql("SELECT * FROM classification_codes", conn)

codes_df["Category"] = codes_df["Category"].str.strip()
uncertain_eco = {"Code": "000", "Category": "Unsure"}
codes_df = codes_df.append(uncertain_eco, ignore_index=True)

codes_df = codes_df[~codes_df["Code"].duplicated(keep="last")]

codes_df = codes_df.set_index("Code")

# | label: Query bioeconomy

bioeconomy = pd.read_sql(
    """
select
  i.sinno_id,
  i.innovation_name_in_swedish AS name,
  i.description_in_swedish AS description,
  i.additional_information_if_origin_new_scientific_discovery || i.additional_information_if_origin_new_technologies_or_materials || i.additional_info_if_origin_official_regulation_legislation_and_standards || i.additional_information_if_origin_solution_for_a_problem || i.additional_information_if_origin_performance || i.additional_information_if_origin_other AS info,
  i.year_of_commercialization AS year,
  us.use_sector
from
  innovation i
  join use_sectors us on i.sinno_id = us.sinno_id
where
  (
    us.use_sector like '02%'
    or us.use_sector like '20%'
    or us.use_sector like '21%'
    or us.use_sector like '36%'
    or product_code like '02%'
    or product_code like '20%'
    or product_code like '21%'
    or product_code like '36%'
  )
  or (
    description like '%virke%'
    or description like '%cellulos%'
    or description like '%lignin%'
    or description like '%spån%'
    or description like '%bark%'
    or description like '%levulinsyra%'
    or description like '%furfural%'
    or description like '%svarttjära%'
    or description like '%svartlut%'
    or description like '%växtbas%'
    or description like '%ved%'
    or description like '%trä%'
    or description like '%skog%'
    or description like '%biobränsle%'
    or description like '%biologisk%'
    or description like '%nedbrytbar%'
    or description like '%papper%'
    or description like '%pappret%'
    or description like '%karton%'
    or description like '%tencel%'
  );
""",
    conn,
)

sni_codes = pd.read_sql_query(
    """
select
*
from 
sni_codes
""",
    conn,
)

sni_codes = sni_codes.rename(columns={"code": "use_sector"})

swinno = pd.read_sql_query(
    """
select sinno_id, year_of_commercialization as year, innovation_name_in_swedish as name
from innovation;
""",
    conn,
)

swinno["bioeconomy"] = swinno["sinno_id"].isin(bioeconomy["sinno_id"].unique())

# | label: Query eco-innovation

eco_innovations = pd.read_sql(
    """
SELECT
  sinno_id,
  innovation_type as innovation_type_code,
  c.Category as innovation_type
FROM
  eco_innovations
JOIN classification_codes AS c ON c.Code = eco_innovations.innovation_type
WHERE 
innovation_type NOT IN (701, 602, 601, 501, 111, 109, 108)
;
""",
    conn,
)

eco_innovations["innovation_type"] = eco_innovations["innovation_type"].str.strip()

# | label: Calculate Bioeconomy Share


def calculate_bioeconomy_share(swinno):
    df = swinno.copy()
    df = df[["sinno_id", "year", "bioeconomy"]]
    df = (
        df.groupby("year")
        .agg(
            total_count=("sinno_id", "nunique"), bioeconomy_count=("bioeconomy", "sum")
        )
        .reset_index()
    )
    df["bioeconomy_share"] = df["bioeconomy_count"] / df["total_count"]

    return df


bioeconomy_share = calculate_bioeconomy_share(swinno)

bioeconomy_share.to_csv(
    Path(ROOT, "data/modified-data/bioeconomy_share.csv"), index=False
)
