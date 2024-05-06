bioeconomy_visions = pd.read_sql(
    """
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
""",
    conn,
)

bioeconomy_visions.loc[
    bioeconomy_visions["bioeconomy_vision"] == "Not Bioeconomy",
    ["bioeconomy_vision"],
] = "Vision Neutral"

uncertain_bioeconomy_visions = bioeconomy_visions.query("bioeconomy_vision == 'Unsure'")


certain_bioeconomy_visions = bioeconomy_visions.loc[
    ~bioeconomy_visions["sinno_id"].isin(uncertain_bioeconomy_visions["sinno_id"]), :
]

count_certain_bioeconomy_visions = (
    certain_bioeconomy_visions.groupby(["year", "bioeconomy_vision"])
    .size()
    .reset_index(name="count")
)

count_certain_bioeconomy_visions.to_csv("data/modified/count_certain_visions.csv")
total_certain_bioeconomy_visions = (
    count_certain_bioeconomy_visions.groupby("bioeconomy_vision")
    .agg("sum", numeric_only=True)
    .sort_values("count", ascending=False)
    .reset_index()
)
