import pandas as pd
from pathlib import Path

#file path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

MATCHES_FILE = RAW_DATA / "matches_1930_2022.CSV"

#--------------------------------------------------------

#Load data
matches = pd.read_csv(MATCHES_FILE)

#---------------------------------------------------------

#Initial inspection
print("Dataset shape: ", matches.shape) 

print("\nColumns: ")     
print(matches.columns.tolist()) 

print("\nFirst 5 rows: ") 
print(matches.head()) 

print("\nData types: ") 
print(matches.dtypes) 

print("\nMissing values: ") 
print(matches.isnull().sum()) 

print("\nDuplicare rows: ", matches.duplicated().sum()) 

#----------------------------------------------------------
# Basic cleaning and standardization

# remove leading/trailing whitespace from column names
matches.columns = matches.columns.str.strip()

#Standardize team names
matches["home_team"] = matches["home_team"].str.strip()
matches["away_team"] = matches["away_team"].str.strip()

#Convert Date from string to datetime
matches["Date"] = pd.to_datetime(matches["Date"], errors = "coerce")

#Convert numeric columns to numeric types
numeric_columns = [
    "home_score",
    "away_score",
    "home_xg",
    "away_xg",
    "home_penalty",
    "away_penalty",
    "Attendance",
    "Year",
]

for column in numeric_columns:
    matches[column] = pd.to_numeric(matches[column], errors = "coerce")

#--------------------------------------------------------
#Validate Cleaning

print("\nAfter basic clening: ")
print("Dataset shape: ", matches.shape)

print("\nDate data type: ")
print(matches["Date"].dtype)

print("\nUnique home teams: ", matches["home_team"].nunique())
print("Unique away teams: ", matches["away_team"].nunique())

print("\nDuplicate rows: ", matches.duplicated().sum())

print("\nTotal unique teams: ")
all_teams = sorted(
    set(matches["home_team"].dropna()) | 
    set(matches["away_team"].dropna())
)

for team in all_teams:
    print(team)

print("\nTotal: ", len(all_teams))

#--------------------------------------------------------
# Inspect selected columns with missing values

columns_to_check = [
    "home_xg",
    "away_xg",
    "home_penalty",
    "away_penalty",
    "home_own_goal",
    "away_own_goal",
    "home_red_card",
    "away_red_card",
]

print("\nSelected columns  - sample values: ")

for column in columns_to_check:
    print(f"\n{column}:")
    print(matches[column].value_counts(dropna=False).head(10))

#--------------------------------------------------------
# Save cleaned dataset

PROCESSED_DATA.mkdir(parents = True, exist_ok = True)

OUTPUT_FILE = PROCESSED_DATA / "matches_cleaned.csv"

matches.to_csv(OUTPUT_FILE, index = False)

print("\nCleaned dataset saved to: ")
print(OUTPUT_FILE)

#---------------------------------------------------------
# Verify saved dataset

verified_matches = pd.read_csv(OUTPUT_FILE)

print("\nVerified saved dataser: ")
print("Shape: ", verified_matches.shape)
print("Columns: ", len(verified_matches.columns))
print("Duplicate rows: ", verified_matches.duplicated().sum())