from typing import List

import polars as pl
from pyhere import here


def calculate_5yma(data: pl.DataFrame, col: str | List[str]) -> pl.DataFrame:
    return data.with_columns(pl.col(col).rolling_mean(window_size=5).prefix("ma5_"))


if __name__ == "__main__":
    data_raw = here("data/raw")
    data_modified = here("data/modified")
    swinno_bioeconomy = pl.read_csv(data_raw / "id_year_bioeconomy.csv")

    swinno_bioeconomy = (
        swinno_bioeconomy.group_by("year")
        .agg(
            pl.col("bioeconomy").sum().alias("n_bioeconomy"),
            pl.col("sinno_id").n_unique().alias("n_innovation"),
        )
        .with_columns(share_bioeconomy=pl.col("n_bioeconomy") / pl.col("n_innovation"))
        .sort("year")
        .pipe(calculate_5yma, col=["n_innovation", "n_bioeconomy", "share_bioeconomy"])
    )
    swinno_bioeconomy.write_csv(data_modified / "swinno_bioeconomy_share.csv")
