import polars as pl
from pathlib import Path


from swinno_bioeconomy_directionality.config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from swinno_bioeconomy_directionality.swinno_helpers import connect_swinno_db


def load_tag_data(tags_path: Path) -> pl.DataFrame:
    """Load manually tagged innovation data."""
    tag_files = tags_path.glob("*.csv")
    tag_dfs = [
        pl.read_csv(
            p, columns=["sinno_id", "bioeconomy_vision", "innovation_type", "notes"]
        )
        for p in tag_files
    ]
    return pl.concat(tag_dfs)


def load_final_classifications(path: Path) -> pl.DataFrame:
    """Load finalized innovation classifications."""
    files = path.glob("*innovations-to-check.csv")
    dfs = [
        pl.read_csv(
            f,
            columns=[
                "sinno_id",
                "bioeconomy_vision",
                "innovation_type",
                "article_checked",
                "notes",
            ],
        )
        for f in files
    ]
    return pl.concat(dfs)


def resolve_classifications(
    tags_df: pl.DataFrame, final_df: pl.DataFrame
) -> pl.DataFrame:
    """Merge uncertain and final classifications, giving preference to checked entries."""
    # Include manually tagged entries that aren't in the final classification
    missing = tags_df.filter(~pl.col("sinno_id").is_in(final_df["sinno_id"]))
    merged = pl.concat([final_df, missing], how="diagonal")

    # Prefer duplicates with checked articles
    duplicates = merged.filter(pl.col("sinno_id").is_duplicated()).sort("sinno_id")
    preferred = duplicates.filter(pl.col("article_checked").is_not_null())

    # Combine non-duplicates and preferred duplicates
    unique_entries = merged.filter(~pl.col("sinno_id").is_duplicated())
    return pl.concat([unique_entries, preferred])


def clean_codes(
    df: pl.DataFrame,
    column: str,
    code_digits: int,
    remove_whitespace: bool = True,
    drop_na: bool = True,
) -> pl.DataFrame:
    # Start with optional drop_na
    if drop_na:
        df = df.drop_nulls([column])

    df = df.pipe(replace_letters_codes, column)
    col = pl.col(column).cast(pl.Utf8).str.strip_chars()

    # Replace semicolons with commas
    col = col.str.replace_all(";", ",")

    # Replace standalone 0 and 9 with repeated digits (e.g., "0" -> "0000" if code_digits == 4)
    padded_0 = "0" * code_digits
    padded_9 = "9" * code_digits
    col = col.str.replace_all(r"\b0\b", padded_0)
    col = col.str.replace_all(r"\b9\b", padded_9)

    # Replace improperly formatted code sequences with a comma (this part is a bit ambiguous in original logic)
    # Example: insert commas after codes of fixed length unless it's the last in the string.
    # This step requires assumptions about structure. We simplify and fix double commas in next step.

    # Replace double commas with single commas
    col = col.str.replace_all(",,", ",")

    if remove_whitespace:
        col = col.str.replace_all(r"\s", ",")

    # Apply the cleaned column
    df = df.with_columns(col.alias(column))

    return df


def replace_letters_codes(df: pl.DataFrame, col: str) -> pl.DataFrame:
    col_expr = (
        pl.col(col)
        .cast(pl.Utf8)
        .str.replace_all("A", "1")
        .str.replace_all("B", "2")
        .str.replace_all("C", "3")
    )
    return df.with_columns(col_expr.alias(col))


def split_cols(df: pl.DataFrame, col_to_split: str, sep: str = ",") -> pl.DataFrame:
    """Splits a string column into multiple new columns and removes the original column."""
    return df.with_columns(
        pl.col(col_to_split).str.split(sep).list.to_struct(n_field_strategy="max_width")
    ).unnest(col_to_split)


def melt_table(
    df: pl.DataFrame, index: str, col_start: str, value_name: str
) -> pl.DataFrame:
    """Melts wide-format table into long-format, removing blanks and nulls."""
    # Find all columns starting with the prefix
    value_vars = [c for c in df.columns if c.startswith(col_start)]

    melted = df.unpivot(index=index, on=value_vars, value_name=value_name)

    # Remove empty strings and nulls
    melted = melted.filter(
        (pl.col(value_name).is_not_null()) & (pl.col(value_name) != "")
    )

    return melted.select([index, value_name]).sort(index)


def main():
    engine = connect_swinno_db()  # May be used later for DB ops

    # Load data
    tags_path = RAW_DATA_DIR / "tags"
    final_path = RAW_DATA_DIR / "final_classifications"

    tags_df = load_tag_data(tags_path)
    final_df = load_final_classifications(final_path)

    # Resolve uncertain classifications
    classifications = resolve_classifications(tags_df, final_df).with_columns(
        pl.col("sinno_id").cast(pl.String)
    )

    ## Bioeconomy
    retagged_bv_path = (
        RAW_DATA_DIR / "final_classifications" / "retagged_bioeconomy_visions.csv"
    )
    retagged_bv = pl.read_csv(
        retagged_bv_path,
        schema_overrides={"sinno_id": pl.String, "bioeconomy_vision": pl.String},
    )
    bv_classifications = classifications.filter(
        ~pl.col("sinno_id").is_in(retagged_bv["sinno_id"])
    )

    clean_bv_classifications = clean_codes(bv_classifications, "bioeconomy_vision", 1)
    split_bv = split_cols(
        clean_bv_classifications, col_to_split="bioeconomy_vision", sep=","
    )
    melted_bv = melt_table(
        split_bv, index="sinno_id", col_start="field_", value_name="bioeconomy_vision"
    )

    bioeconomy_visions_table = pl.concat([melted_bv, retagged_bv]).drop_nulls()

    ## Eco-Innovation Types
    retagged_ei_path = (
        RAW_DATA_DIR / "final_classifications" / "retagged_eco_innovations.csv"
    )
    retagged_ei = pl.read_csv(
        retagged_ei_path,
        schema_overrides={"sinno_id": pl.String, "innovation_type": pl.String},
    )
    ei_classifications = classifications.filter(
        ~pl.col("sinno_id").is_in(retagged_ei["sinno_id"])
    )

    clean_ei_classifications = clean_codes(ei_classifications, "innovation_type", 3)
    split_ei = split_cols(
        clean_ei_classifications, col_to_split="innovation_type", sep=","
    )
    melted_ei = melt_table(
        split_ei, index="sinno_id", col_start="field_", value_name="innovation_type"
    )

    eco_innovation_table = pl.concat([melted_ei, retagged_ei]).drop_nulls()

    ## Notes
    retagged_notes_path = RAW_DATA_DIR / "final_classifications" / "retagged_notes.csv"
    retagged_notes = pl.read_csv(
        retagged_notes_path,
        schema_overrides={"sinno_id": pl.String, "notes": pl.String},
    )
    notes_classifications = classifications.filter(
        ~pl.col("sinno_id").is_in(retagged_notes["sinno_id"])
    ).select(["sinno_id", "notes"])

    combined_notes = pl.concat([notes_classifications, retagged_notes]).drop_nulls()

    bioeconomy_visions_table.write_csv(
        PROCESSED_DATA_DIR / "bioeconomy_visions.csv",
    )

    eco_innovation_table.write_csv(PROCESSED_DATA_DIR / "eco_innovations.csv")

    combined_notes.write_csv(
        PROCESSED_DATA_DIR / "categorization_notes.csv",
    )
    with engine.connect() as conn:
        bioeconomy_visions_table.write_database(
            "bioeconomy_visions", connection=conn, if_table_exists="replace"
        )

        eco_innovation_table.write_database(
            "eco_innovations", connection=conn, if_table_exists="replace"
        )

        combined_notes.write_database(
            "categorization_notes", connection=conn, if_table_exists="replace"
        )


if __name__ == "__main__":
    main()
