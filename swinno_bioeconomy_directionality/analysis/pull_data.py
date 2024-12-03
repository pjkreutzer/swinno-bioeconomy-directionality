from swinno_bioeconomy_directionality.data_handling import database
import pandas as pd

from swinno_bioeconomy_directionality.config import RAW_DATA_DIR

if __name__ == "__main__":
    conn = database.connect_swinno_db()

    # Get sinno ids with year and bioeconomy indicator
    sinno_ids = database.query_sinno_ids(conn)
    sinno_ids.write_csv(RAW_DATA_DIR / "id_year_bioeconomy.csv")

    bioeconomy_visions = database.query_bioeconomy_visions(conn)
    bioeconomy_visions.to_csv(RAW_DATA_DIR / "bioeconomy_visions.csv", index=False)

    uncleaned_bioeconomy = database.query_uncleaned_bioeconomy(conn)
    uncleaned_bioeconomy.to_csv(
        RAW_DATA_DIR / "uncleaned_bioeconomy_query.csv", index=False
    )
