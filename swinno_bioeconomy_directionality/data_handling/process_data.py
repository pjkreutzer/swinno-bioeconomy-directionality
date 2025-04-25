from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import polars as pl
import polars.selectors as cs

from swinno_bioeconomy_directionality.config import INTERIM_DATA_DIR


def clean_collaboration_data(data: pl.DataFrame) -> pl.DataFrame:
    return data.unique("sinno_id").select(
        [
            "sinno_id",
            "firm",
            cs.starts_with("collaborator"),
        ],
    )


def clean_taalbi_column_names(data: pl.DataFrame) -> pl.DataFrame:
    return data.rename({"SINNO_ID": "sinno_id", "Firm level 2": "firm"}).rename(
        lambda c: c.lower().strip().replace(" ", "_")
    )


def clean_taalbi_aggregation(data: pl.DataFrame) -> pl.DataFrame:
    return (
        data.pipe(clean_taalbi_column_names)
        .with_columns(pl.all().cast(pl.String))
        .with_columns(pl.col("*").replace("0", None))
        .pipe(clean_collaboration_data)
        .with_columns(cs.string().str.strip_chars())
    )


def split_columns(data: pl.DataFrame) -> pl.DataFrame:
    return (
        data.with_columns(
            cs.string()
            .exclude("sinno_id")
            .str.split(";")
            .list.eval(pl.element().str.strip_chars())
        ).pipe(_pad_node_list)
        # for each list columns apply the pad_node_list function
    )


def _pad_node_list(data: pl.DataFrame) -> pl.DataFrame:
    """
    Pad all string list columns with None if they have exactly 2 elements.

    Args:
        data (pl.DataFrame): Input DataFrame with list columns

    Returns:
        pl.DataFrame: DataFrame with padded list columns
    """
    # Get list of column names that are string lists
    list_cols = data.select(cs.by_dtype(pl.List(pl.String))).columns

    # Create expressions for each list column
    expressions = [
        pl.when(pl.col(col).list.len() == 2)
        .then(pl.col(col).list.concat([None]))
        .otherwise(pl.col(col))
        .alias(col)
        for col in list_cols
    ]

    return data.with_columns(expressions)


def get_firm_literal(data: pl.DataFrame) -> pl.DataFrame:
    return data.with_columns((cs.by_dtype(pl.List(pl.String))).list.first())


def get_firm_common(data: pl.DataFrame) -> pl.DataFrame:
    return data.with_columns(
        (cs.by_dtype(pl.List(pl.String)).exclude("year")).list.get(1)
    )


def get_firm_id(data: pl.DataFrame) -> pl.DataFrame:
    return data.with_columns((cs.by_dtype(pl.List(pl.String))).list.last())


def clean_swinno_collaboration(
    data: pl.DataFrame,
) -> Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    split_data = split_columns(data)
    literal_data = get_firm_literal(split_data)
    common_data = get_firm_common(split_data)
    id_data = get_firm_id(split_data)

    return literal_data, common_data, id_data


def reshape_node_year(node_data: pl.DataFrame) -> pl.DataFrame:
    index = node_data.select(pl.exclude(["firm", r"^collaborator+_\d+$"])).columns
    return (
        node_data.unpivot(index=index, value_name="node")
        .drop("variable")
        .drop_nulls("node")
    )
