from swinno_bioeconomy_directionality.data_handling import database
from pyhere import here
import pandas as pd

if __name__ == "__main__":
    conn = database.connect_swinno_db()
    outpath = here("data/raw")

    # Get sinno ids with year and bioeconomy indicator
    sinno_ids = database.query_sinno_ids(conn)
    sinno_ids.write_csv(here(outpath, "id_year_bioeconomy.csv"))

    bioeconomy_visions = database.query_bioeconomy_visions(conn)
    bioeconomy_visions.to_csv(here(outpath / "bioeconomy_visions.csv"), index=False)

    uncleaned_bioeconomy = database.query_uncleaned_bioeconomy(conn)
    uncleaned_bioeconomy.to_csv(
        here(outpath / "uncleaned_bioeconomy_query.csv"), index=False
    )
