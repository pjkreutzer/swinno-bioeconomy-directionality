import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from src.swinno_helpers import connect_swinno_db, get_project_root

conn = connect_swinno_db()


def query_bioeconomy(conn):
    query = """
SELECT
  i.sinno_id,
  i.innovation_name_in_swedish AS name,
  i.description_in_swedish AS description,
  i.additional_information_if_origin_new_scientific_discovery || i.additional_information_if_origin_new_technologies_or_materials || i.additional_info_if_origin_official_regulation_legislation_and_standards || i.additional_information_if_origin_solution_for_a_problem || i.additional_information_if_origin_performance || i.additional_information_if_origin_other AS info,
  i.year_of_commercialization AS year,
  us.use_sector
FROM
  innovation i
  JOIN use_sectors us ON i.sinno_id = us.sinno_id
WHERE
  (us.use_sector LIKE '02%' OR us.use_sector LIKE '20%' OR us.use_sector LIKE '21%' OR us.use_sector LIKE '36%')
  OR (product_code LIKE '02%' OR product_code LIKE '20%' OR product_code LIKE '21%' OR product_code LIKE '36%')

UNION

SELECT
  i.sinno_id,
  i.innovation_name_in_swedish AS name,
  i.description_in_swedish AS description,
  i.additional_information_if_origin_new_scientific_discovery || i.additional_information_if_origin_new_technologies_or_materials || i.additional_info_if_origin_official_regulation_legislation_and_standards || i.additional_information_if_origin_solution_for_a_problem || i.additional_information_if_origin_performance || i.additional_information_if_origin_other AS info,
  i.year_of_commercialization AS year,
  us.use_sector
FROM
  innovation i
  JOIN use_sectors us ON i.sinno_id = us.sinno_id
WHERE
  (description LIKE '%virke%' OR description LIKE '%cellulos%' OR description LIKE '%lignin%' OR description LIKE '%spån%' OR description LIKE '%bark%'
   OR description LIKE '%levulinsyra%' OR description LIKE '%furfural%' OR description LIKE '%svarttjära%' OR description LIKE '%svartlut%' OR description LIKE '%växtbas%'
   OR description LIKE '%ved%' OR description LIKE '%trä%' OR description LIKE '%skog%' OR description LIKE '%biobränsle%' OR description LIKE '%biologisk%'
   OR description LIKE '%nedbrytbar%' OR description LIKE '%papper%' OR description LIKE '%pappret%' OR description LIKE '%karton%' OR description LIKE '%tencel%')
  ;
  """

    return pd.read_sql_query(query, con=conn)


def query_read(conn):
    query = """
  SELECT DISTINCT(CAST(sinno_id AS TEXT)) AS sinno_id FROM bioeconomy_visions;
  """
    return pd.read_sql(query, conn)


if __name__ == "__main__":
    last_run = datetime.today().strftime("%Y%m%d")
    out_path = Path(get_project_root(), "results/bioeconomy_definitions/")
    file_name = f"{last_run}_bioeconomy-articles-to-check.txt"

    read = query_read(conn)

    new_bioec = query_bioeconomy(conn)
    sinno_id_to_classify = new_bioec.loc[
        ~new_bioec["sinno_id"].isin(read["sinno_id"]), "sinno_id"
    ].unique()

    np.savetxt(Path(out_path, file_name), sinno_id_to_classify, fmt="%s")

    tagging_columns = [
        "bioeconomy_vision",
        "innovation_type",
        "article_checked",
        "notes",
    ]

    df_to_classify = new_bioec.loc[~new_bioec["sinno_id"].isin(read["sinno_id"]), :]
    df_to_classify = df_to_classify.drop_duplicates(subset="sinno_id")

    for col in tagging_columns:
        df_to_classify[col] = None

    df_to_classify.to_excel(
        Path(get_project_root(), "data/raw", f"{last_run}_innovations-to-check.xlsx"),
        index=False,
    )
