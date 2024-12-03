import polars as pl
from swinno_bioeconomy_directionality.config import (
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR,
)


if __name__ == "__main__":
    bioeconomy_visions = pl.read_csv(RAW_DATA_DIR / "bioeconomy_visions.csv")
