import pandas as pd
from pathlib import Path

#--------------------------------------------------------
# File paths

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

RANKING_2022_FILE = RAW_DATA / "fifa_ranking_2022-10-06.csv"
RANKING_2026_FILE = RAW_DATA / "fifa_ranking_2026-06-08.csv"

#------------------------------------------------------
#Load data

ranking_2022 = pd.read_csv(RANKING_2022_FILE)
ranking_2026 = pd.read_csv(RANKING_2026_FILE)

#------------------------------------------------------
# Initial inspection

print("2022 Ranking Shape: ", ranking_2022.shape)
print("2026 Ranking Shape: ", ranking_2026.shape)

print("\n2022 Ranking Columns: ")
print(ranking_2022.columns.tolist())

print("\n2026 Ranking Columns: ")
print(ranking_2026.columns.tolist())

print("\n2022 First Five Rows: ")
print(ranking_2022.head())

print("2026 First Five Rows: ")
print(ranking_2026.head())

print("2022 Data Types: ")
print(ranking_2022.dtypes)

print("2026 Data Types: ")
print(ranking_2026.dtypes)

print("2022 Missing Values: ")
print(ranking_2022.isnull().sum())

print("2026 Missing Values: ")
print(ranking_2026.isnull().sum())

print("\n2022 Duplicate Rows: ", ranking_2022.duplicated().sum())
print("2026 Duplicate Rows: ",ranking_2026.duplicated().sum())

#---------------------------------------
# Clean ranking dataset
#---------------------------------------

# we are only keeping the columns we need for analysis
ranking_2022_cleaned = ranking_2022[
    [
        "team",
        "team_code",
        "association",
        "rank",
        "previous_rank",
        "points",
        "previous_points"
    ]
].copy()

ranking_2026_cleaned = ranking_2026[
    [
        "team",
        "team_code",
        "association",
        "rank",
        "previous_rank",
        "points",
        "previous_points",
        "rated_matches"
    ]
].copy()

#-------------------------------------------
# Save processed ranking dataset
#-------------------------------------------

ranking_2022_output = PROCESSED_DATA / "fifa_ranking_2022_cleaned.csv"
ranking_2026_output = PROCESSED_DATA / "fifa_ranking_2026_cleaned.csv"

ranking_2022_cleaned.to_csv(ranking_2022_output, index = False)
ranking_2026_cleaned.to_csv(ranking_2026_output, index = False)

print("\n2022 cleaned ranking saved to:  ")
print(ranking_2022_output)

print("\n2026 cleaned ranking saved to:  ")
print(ranking_2026_output)