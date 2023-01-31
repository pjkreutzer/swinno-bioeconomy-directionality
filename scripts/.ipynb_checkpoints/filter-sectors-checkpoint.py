# Quick script to filter for relevant sectors based on Cristinas working paper

import pandas as pd
import pathlib

p = pathlib.Path("data", "modified-data", "swinno-classification.xlsx")
data = pd.read_excel(p, sheet_name="SWINNO 1970-2019")


