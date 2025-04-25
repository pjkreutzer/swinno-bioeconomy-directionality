from swinno_bioeconomy_directionality.data_handling import database
import polars as pl
from swinno_bioeconomy_directionality.config import RAW_DATA_DIR


def pull_data():
    conn = database.connect_swinno_db()

    # Get sinno ids with year and bioeconomy indicator
    sinno_ids = database.query_sinno_ids(conn)
    sinno_ids.write_csv(RAW_DATA_DIR / "id_year_bioeconomy.csv")

    swinno = pl.read_database(
        """
        select sinno_id, year_of_commercialization as year, innovation_name_in_swedish as name
        from innovation;
        """,
        conn,
    )
    swinno.write_csv(RAW_DATA_DIR / "swinno_data.csv")

    bioeconomy_visions = database.query_bioeconomy_visions(conn)
    bioeconomy_visions.write_csv(RAW_DATA_DIR / "bioeconomy_visions.csv")

    recycle_innovation = pl.read_database(
        """
        SELECT *
        FROM classification_codes
        LEFT JOIN eco_innovations ON classification_codes.Code = eco_innovations.innovation_type
        WHERE eco_innovations.innovation_type = 107 OR eco_innovations.innovation_type = 206 
        AND sinno_id NOT IN (SELECT sinno_id FROM categorization_notes WHERE notes LIKE '%not forest%')
        """,
        conn,
    )
    recycle_innovation.write_csv(RAW_DATA_DIR / "recycling_innovation.csv")

    uncleaned_bioeconomy = database.query_uncleaned_bioeconomy(conn)
    uncleaned_bioeconomy.write_csv(RAW_DATA_DIR / "uncleaned_bioeconomy_query.csv")

    cleaned_bioeconomy = database.query_clean_bioeconomy(conn)
    cleaned_bioeconomy.write_csv(RAW_DATA_DIR / "id_year_bioeconomy.csv")


if __name__ == "__main__":
    pull_data()
