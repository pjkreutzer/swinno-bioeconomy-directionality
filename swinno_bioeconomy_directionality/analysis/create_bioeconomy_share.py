from typing import List

import polars as pl

from swinno_bioeconomy_directionality.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
)

from swinno_bioeconomy_directionality.data_handling.io import DataLoader


def calculate_5yma(data: pl.DataFrame, col: str | List[str]) -> pl.DataFrame:
    return data.with_columns(
        pl.col(col).rolling_mean(window_size=5).name.prefix("ma5_")
    )


if __name__ == "__main__":
    swinno_bioeconomy = DataLoader(RAW_DATA_DIR).load_id_year_bioeconomy()

    swinno_bioeconomy = (
        swinno_bioeconomy.group_by("year")
        .agg(
            pl.col("bioeconomy").sum().alias("n_bioeconomy"),
            pl.col("sinno_id").n_unique().alias("n_innovation"),
        )
        .with_columns(pct_bioeconomy=pl.col("n_bioeconomy") / pl.col("n_innovation"))
        .sort("year")
        .pipe(calculate_5yma, col=["n_innovation", "n_bioeconomy", "pct_bioeconomy"])
    )
    swinno_bioeconomy.write_csv(PROCESSED_DATA_DIR / "swinno_bioeconomy_share.csv")
