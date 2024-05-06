from sqlalchemy import create_engine
from pathlib import Path
import polars as pl
import pandas as pd
from sqlalchemy.engine.base import Engine


def connect_swinno_db() -> Engine:
    path_to_db = (
        Path(
            "/Users/research/Library/CloudStorage/OneDrive-LundUniversity/research/swinno-db/data/swinno.db"
        )
        .absolute()
        .as_posix()
    )
    database_uri = f"sqlite:///{path_to_db}"
    engine = create_engine(database_uri)
    return engine


def query_innovation_experience(conn: Engine) -> pl.DataFrame:
    query = """
    SELECT
    i.literal_name_of_innovating_firm_sinnos_common_name_sinno_id AS firm,
    SUM(
        CASE
        WHEN bv.bioeconomy_vision = 1 THEN 1
        ELSE 0
        END
    ) AS biotechnology,
    SUM(
        CASE
        WHEN bv.bioeconomy_vision = 2 THEN 1
        ELSE 0
        END
    ) AS bioresources,
    SUM(
        CASE
        WHEN bv.bioeconomy_vision = 3 THEN 1
        ELSE 0
        END
    ) AS bioecology,
    SUM(
        CASE
        WHEN bv.bioeconomy_vision = 9 THEN 1
        ELSE 0
        END
    ) AS not_bioeconomy,
    SUM(
        CASE
        WHEN bv.bioeconomy_vision = 0 THEN 1
        ELSE 0
        END
    ) AS unsure,
    COUNT(distinct i.sinno_id) as total_innovation_count
    FROM
    bioeconomy_visions AS bv
    JOIN innovation AS i ON i.sinno_id = bv.sinno_id
    GROUP BY
    i.literal_name_of_innovating_firm_sinnos_common_name_sinno_id;
    """

    return pl.read_database(query, conn)


def query_isolated_innovation(conn: Engine):
    conn = conn
    query = """SELECT
  DISTINCT(sinno_id),
  year_of_commercialization AS year,
  literal_name_of_innovating_firm_sinnos_common_name_sinno_id AS name
FROM
  innovation
WHERE
  developed_in_collaboration_with_other_actors IS NOT 1"""

    return pl.read_database(query, conn)


def query_sinno_ids(conn: Engine):
    conn = conn
    query = """
    WITH Bioeconomy AS (
  SELECT
    DISTINCT sinno_id
  FROM
    (
      SELECT
        i.sinno_id,
        i.innovation_name_in_swedish AS name,
        i.literal_name_of_innovating_firm_sinnos_common_name_sinno_id AS firm,
        i.literal_name_of_collaborator_sinnos_common_name_sinno_id AS collaborator_0,
        i.literal_name_of_collaborator_sinnos_common_name_sinno_id1 AS collaborator_1,
        i.literal_name_of_collaborator_sinnos_common_name_sinno_id2 AS collaborator_2,
        i.literal_name_of_collaborator_sinnos_common_name_sinno_id3 AS collaborator_3,
        i.literal_name_of_collaborator_sinnos_common_name_sinno_id4 AS collaborator_4,
        i.literal_name_of_collaborator_sinnos_common_name_sinno_id5 AS collaborator_5,
        i.literal_name_of_collaborator_sinnos_common_name_sinno_id6 AS collaborator_6,
        i.literal_name_of_collaborator_sinnos_common_name_sinno_id7 AS collaborator_7,
        i.literal_name_of_collaborator_sinnos_common_name_sinno_id8 AS collaborator_8,
        i.description_in_swedish AS description,
        i.year_of_commercialization AS year,
        us.use_sector
      FROM
        innovation i
        JOIN use_sectors us ON i.sinno_id = us.sinno_id
      WHERE
        (
          us.use_sector LIKE '02%'
          OR us.use_sector LIKE '20%'
          OR us.use_sector LIKE '21%'
          OR us.use_sector LIKE '36%'
          OR product_code LIKE '02%'
          OR product_code LIKE '20%'
          OR product_code LIKE '21%'
          OR product_code LIKE '36%'
        )
        OR (
          description LIKE '%virke%'
          OR description LIKE '%cellulos%'
          OR description LIKE '%lignin%'
          OR description LIKE '%spån%'
          OR description LIKE '%bark%'
          OR description LIKE '%levulinsyra%'
          OR description LIKE '%furfural%'
          OR description LIKE '%svarttjära%'
          OR description LIKE '%svartlut%'
          OR description LIKE '%växtbas%'
          OR description LIKE '%ved%'
          OR description LIKE '%trä%'
          OR description LIKE '%skog%'
          OR description LIKE '%biobränsle%'
          OR description LIKE '%biologisk%'
          OR description LIKE '%nedbrytbar%'
          OR description LIKE '%papper%'
          OR description LIKE '%pappret%'
          OR description LIKE '%karton%'
          OR description LIKE '%tencel%'
          OR description LIKE '%lyocell%'
        )
        AND i.sinno_id NOT IN (
          SELECT
            sinno_id
          FROM
            categorization_notes
          WHERE
            notes NOT LIKE "%not forest%"
        )
    )
)
SELECT
  i.sinno_id,
  CAST(i.year_of_commercialization AS int) AS year,
  CASE
    WHEN b.sinno_id IS NOT NULL THEN 1
    ELSE 0
  END AS bioeconomy
FROM
  innovation i
  LEFT JOIN Bioeconomy b ON i.sinno_id = b.sinno_id;"""
    return pl.read_database(query, conn)


def query_bioeconomy_innovation(conn: Engine):
    conn = conn

    query = """ 
SELECT
  DISTINCT sinno_id
from
  (
    SELECT
      i.sinno_id,
      i.innovation_name_in_swedish AS name,
      i.literal_name_of_innovating_firm_sinnos_common_name_sinno_id AS firm,
      i.literal_name_of_collaborator_sinnos_common_name_sinno_id AS collaborator_0,
      i.literal_name_of_collaborator_sinnos_common_name_sinno_id1 AS collaborator_1,
      i.literal_name_of_collaborator_sinnos_common_name_sinno_id2 AS collaborator_2,
      i.literal_name_of_collaborator_sinnos_common_name_sinno_id3 AS collaborator_3,
      i.literal_name_of_collaborator_sinnos_common_name_sinno_id4 AS collaborator_4,
      i.literal_name_of_collaborator_sinnos_common_name_sinno_id5 AS collaborator_5,
      i.literal_name_of_collaborator_sinnos_common_name_sinno_id6 AS collaborator_6,
      i.literal_name_of_collaborator_sinnos_common_name_sinno_id7 AS collaborator_7,
      i.literal_name_of_collaborator_sinnos_common_name_sinno_id8 AS collaborator_8,
      i.description_in_swedish AS description,
      i.year_of_commercialization AS year,
      us.use_sector
    FROM
      innovation i
      JOIN use_sectors us ON i.sinno_id = us.sinno_id
    WHERE
      (
        us.use_sector LIKE '02%'
        OR us.use_sector LIKE '20%'
        OR us.use_sector LIKE '21%'
        OR us.use_sector LIKE '36%'
        OR product_code LIKE '02%'
        OR product_code LIKE '20%'
        OR product_code LIKE '21%'
        OR product_code LIKE '36%'
      )
      OR (
        description LIKE '%virke%'
        OR description LIKE '%cellulos%'
        OR description LIKE '%lignin%'
        OR description LIKE '%spån%'
        OR description LIKE '%bark%'
        OR description LIKE '%levulinsyra%'
        OR description LIKE '%furfural%'
        OR description LIKE '%svarttjära%'
        OR description LIKE '%svartlut%'
        OR description LIKE '%växtbas%'
        OR description LIKE '%ved%'
        OR description LIKE '%trä%'
        OR description LIKE '%skog%'
        OR description LIKE '%biobränsle%'
        OR description LIKE '%biologisk%'
        OR description LIKE '%nedbrytbar%'
        OR description LIKE '%papper%'
        OR description LIKE '%pappret%'
        OR description LIKE '%karton%'
        OR description LIKE '%tencel%'
        OR description LIKE '%lyocell%'
      )
      AND i.sinno_id NOT IN (
        SELECT
          sinno_id
        FROM
          categorization_notes
        WHERE
          notes NOT LIKE "%not forest%"
      )
  );
    """

    return pl.read_database(query, conn)


def query_collaborations(conn: Engine):
    conn = conn

    query = """
SELECT
  sinno_id,
  year_of_commercialization AS year,
  literal_name_of_innovating_firm_sinnos_common_name_sinno_id AS firm,
  literal_name_of_collaborator_sinnos_common_name_sinno_id AS collaborator_0,
  literal_name_of_collaborator_sinnos_common_name_sinno_id1 AS collaborator_1,
  literal_name_of_collaborator_sinnos_common_name_sinno_id2 AS collaborator_2,
  literal_name_of_collaborator_sinnos_common_name_sinno_id3 AS collaborator_3,
  literal_name_of_collaborator_sinnos_common_name_sinno_id4 AS collaborator_4,
  literal_name_of_collaborator_sinnos_common_name_sinno_id5 AS collaborator_5,
  literal_name_of_collaborator_sinnos_common_name_sinno_id6 AS collaborator_6,
  literal_name_of_collaborator_sinnos_common_name_sinno_id7 AS collaborator_7,
  literal_name_of_collaborator_sinnos_common_name_sinno_id8 AS collaborator_8
FROM
  innovation
WHERE
  developed_in_collaboration_with_other_actors = 1;
"""

    return pl.read_database(query, conn)


def query_count_bioeconomy_innovations(conn: Engine):
    conn = conn

    query_string = """
    SELECT
    i.literal_name_of_innovating_firm_sinnos_common_name_sinno_id AS firm,
    SUM(
        CASE
        WHEN bv.bioeconomy_vision = 1 THEN 1
        ELSE 0
        END
    ) AS biotechnology,
    SUM(
        CASE
        WHEN bv.bioeconomy_vision = 2 THEN 1
        ELSE 0
        END
    ) AS bioresources,
    SUM(
        CASE
        WHEN bv.bioeconomy_vision = 3 THEN 1
        ELSE 0
        END
    ) AS bioecology,
    SUM(
        CASE
        WHEN bv.bioeconomy_vision = 9 THEN 1
        ELSE 0
        END
    ) AS not_bioeconomy,
    SUM(
        CASE
        WHEN bv.bioeconomy_vision = 0 THEN 1
        ELSE 0
        END
    ) AS unsure,
    COUNT(distinct i.sinno_id) as total_innovation_count
    FROM
    bioeconomy_visions AS bv
    JOIN innovation AS i ON i.sinno_id = bv.sinno_id
    GROUP BY
    i.literal_name_of_innovating_firm_sinnos_common_name_sinno_id;
    """

    df = pl.read_database(query_string, conn)

    # Split the firm column into multiple columns
    firm_split = df["firm"].str.split(";", expand=True)

    # Create new columns for each unique value in the split column
    for col in firm_split.columns:
        df[col] = firm_split[col].str.strip()

    # Drop the original firm column
    df = df.drop(columns=["firm"])

    # ÖSA is poorly coded
    df.loc[df[1] == "Östbergs Fabriks", 1] = "ÖSA (Östbergs Fabriks AB i Alfta)"

    value_columns = [
        "biotechnology",
        "bioresources",
        "bioecology",
        "not_bioeconomy",
        "unsure",
        "total_innovation_count",
    ]

    df_aggregated = df.groupby(1)[value_columns].sum()
    return df_aggregated.reset_index().rename(columns={1: "firm"})


def query_total_innovation_counts(conn: Engine):
    conn = conn

    query = """
    SELECT
    i.literal_name_of_innovating_firm_sinnos_common_name_sinno_id AS firm,
    COUNT(DISTINCT i.sinno_id) as total_innovation_count
    FROM
    innovation AS i
    JOIN
    (
        SELECT
        DISTINCT
        i.sinno_id,
        i.description_in_swedish AS description

        FROM
        innovation i
        JOIN use_sectors us ON us.sinno_id = i.sinno_id AND i.year_of_commercialization > 1970
            WHERE
        (
            us.use_sector LIKE '02%'
            OR us.use_sector LIKE '20%'
            OR us.use_sector LIKE '21%'
            OR us.use_sector LIKE '36%'
            OR product_code LIKE '02%'
            OR product_code LIKE '20%'
            OR product_code LIKE '21%'
            OR product_code LIKE '36%'
        )
        OR (
            description LIKE '%virke%'
            OR description LIKE '%cellulos%'
            OR description LIKE '%lignin%'
            OR description LIKE '%spån%'
            OR description LIKE '%bark%'
            OR description LIKE '%levulinsyra%'
            OR description LIKE '%furfural%'
            OR description LIKE '%svarttjära%'
            OR description LIKE '%svartlut%'
            OR description LIKE '%växtbas%'
            OR description LIKE '%ved%'
            OR description LIKE '%trä%'
            OR description LIKE '%skog%'
            OR description LIKE '%biobränsle%'
            OR description LIKE '%biologisk%'
            OR description LIKE '%nedbrytbar%'
            OR description LIKE '%papper%'
            OR description LIKE '%pappret%'
            OR description LIKE '%karton%'
            OR description LIKE '%tencel%'
        )
    ) AS subquery ON i.sinno_id = subquery.sinno_id
    GROUP BY i.literal_name_of_innovating_firm_sinnos_common_name_sinno_id;
    """

    return pl.read_database(query, conn)


def query_bioeconomy_visions(conn):
    query = """
  SELECT bv.sinno_id
  , codes.Category AS bioeconomy_vision
  , i.year_of_commercialization AS "year"
  FROM bioeconomy_visions AS bv
  JOIN [classification_codes] AS codes ON codes.code = bv.bioeconomy_vision
  JOIN innovation AS i ON i.sinno_id = bv.sinno_id
  WHERE bv.sinno_id NOT IN (SELECT sinno_id FROM categorization_notes WHERE notes NOT LIKE "%not forest%")
  UNION
  SELECT DISTINCT(ei.sinno_id)
  , 'Bioecology Vision' AS bioeconomy_vision
  , i.year_of_commercialization AS "i.year"
  FROM eco_innovations AS ei
  JOIN innovation AS i ON i.sinno_id = ei.sinno_id
  WHERE ei.innovation_type IN (206, 107)
  AND ei.sinno_id NOT IN (
    SELECT ei2.sinno_id
    FROM eco_innovations as ei2
    WHERE ei2.innovation_type IN (999, '000')
    );
  -- adds recycling innovation to bioecology
  """
    return pd.read_sql(query, conn)


def query_eco_innovations(conn):
    query = """
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
"""
    return pd.read_sql(query, conn)


def query_uncleaned_bioeconomy(conn):
    query = """
     SELECT
        DISTINCT(i.sinno_id),
        i.innovation_name_in_swedish AS name,
        i.literal_name_of_innovating_firm_sinnos_common_name_sinno_id AS firm,
        i.description_in_swedish AS description,
        i.year_of_commercialization AS year,
        us.use_sector
      FROM
        innovation i
        JOIN use_sectors us ON i.sinno_id = us.sinno_id
      WHERE
        (
          us.use_sector LIKE '02%'
          OR us.use_sector LIKE '20%'
          OR us.use_sector LIKE '21%'
          OR us.use_sector LIKE '36%'
          OR product_code LIKE '02%'
          OR product_code LIKE '20%'
          OR product_code LIKE '21%'
          OR product_code LIKE '36%'
        )
        OR (
          description LIKE '%virke%'
          OR description LIKE '%cellulos%'
          OR description LIKE '%lignin%'
          OR description LIKE '%spån%'
          OR description LIKE '%bark%'
          OR description LIKE '%levulinsyra%'
          OR description LIKE '%furfural%'
          OR description LIKE '%svarttjära%'
          OR description LIKE '%svartlut%'
          OR description LIKE '%växtbas%'
          OR description LIKE '%ved%'
          OR description LIKE '%trä%'
          OR description LIKE '%skog%'
          OR description LIKE '%biobränsle%'
          OR description LIKE '%biologisk%'
          OR description LIKE '%nedbrytbar%'
          OR description LIKE '%papper%'
          OR description LIKE '%pappret%'
          OR description LIKE '%karton%'
          OR description LIKE '%tencel%'
          OR description LIKE '%lyocell%'
        );
    """
    return pd.read_sql(query, conn)
