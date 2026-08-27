import pandas as pd
from pathlib import Path

#------------------------------------------------
#File Paths

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT /"data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed" 

PLAYERS_FILE = RAW_DATA / "player_performance.csv"

#------------------------------------------------
# Load Data

players =pd.read_csv(PLAYERS_FILE)

#------------------------------------------------
# Initial Inspection

print("Dataset shape: ", players.shape)

print("\nColumns: ")
print(players.columns.tolist())


print("\nFirst 5 rows: ")
print(players.head())


print("\nData types: ")
print(players.dtypes)

print("\nMissing values: ")
print(players.isnull().sum())

print("\nDuplicate rows: ", [players.duplicated().sum()])

#---------------------------------------------
# Basic cleaning and standardization

#Remove leading/trailing whitespace from column names
players.columns =  players.columns.str.strip()

#Strip whitespace from string columns
string_columns = players.select_dtypes(include = ["object", "string"]).columns

for column in string_columns:
    players[column] = players[column].str.strip()

# Conver match_date to datetime
players["match_date"] = pd.to_datetime(
    players["match_date"], 
    errors = "coerce"
)

# Numeric Columns
numeric_columns = [
    "age",
    "jersey_number",
    "height_cm",
    "weight_kg",
    "market_value_eur",
    "minutes_played",
    "goals",
    "assists",
    "shots",
    "shots_on_target",
    "expected_goals_xg",
    "expected_assists_xa",
    "key_passes",
    "successful_passes",
    "total_passes",
    "pass_accuracy",
    "dribbles_attempted",
    "successful_dribbles",
    "crosses",
    "successful_crosses",
    "tackles",
    "interceptions",
    "clearances",
    "blocks",
    "aerial_duels_won",
    "aerial_duels_lost",
    "recoveries",
    "defensive_actions",
    "fouls_committed",
    "fouls_suffered",
    "yellow_cards",
    "red_cards",
    "offsides",
    "saves",
    "save_percentage",
    "punches",
    "clean_sheet",
    "goals_conceded",
    "penalty_saves",
    "distance_covered_km",
    "sprint_distance_km",
    "top_speed_kmh",
    "accelerations",
    "decelerations",
    "stamina_score",
    "player_rating",
    "performance_score",
    "offensive_contribution",
    "defensive_contribution",
    "possession_impact",
    "pressure_resistance",
    "creativity_score",
    "consistency_score",
    "clutch_performance_score",
    "total_goals_tournament",
    "total_assists_tournament",
    "total_minutes_tournament",
    "player_of_match_awards",
    "tournament_rating",
]

for column in numeric_columns:
    players[column] = pd.to_numeric(
        players[column],
        errors = "coerce"
    )

#------------------------------------------------
# Validate Cleaning

print("\nAfter basic cleaning: ")

print("Dataset shape: ", players.shape)

print("\nMatch date data type: ")
print(players["match_date"].dtype)

print("\nDuplicate rows: ")
print(players.duplicated().sum())

print("\nMissing values after cleaning: ")
print(players.isnull().sum().sum())

print("\nUnique players: ")
print(players["player_id"].nunique())

print("\nUnique matches: ")
print(players["match_id"].nunique())

print("\nUnique teams: ")
print(players["team"].nunique())

print("\nUnique positions: ")
print(players["position"].nunique())

print("\nTeam names: ")
print(sorted(players["team"].unique()))

#----------------------------------------------------------------------------------
# Classify player dataset information

# Player identity and profile information
player_profile_columns = [
    "player_id",
    "player_name",
    "age",
    "nationality",
    "team",
    "jersey_number",
    "position",
    "height_cm",
    "weight_kg",
    "preferred_foot",
    "club_name",
    "market_value_eur",
]

# Match information
match_information_columns = [
    "match_id",
    "match_date",
    "stadium",
    "city",
    "opponent_team",
    "tournament_stage",
]

# Match result information
match_result_columns = [
    "match_result",
    "goals_team",
    "goals_opponent",
]

# Individual match performance
match_performance_columns = [
    "minutes_played",
    "goals",
    "assists",
    "shots",
    "shots_on_target",
    "expected_goals_xg",
    "expected_assists_xa",
    "key_passes",
    "successful_passes",
    "total_passes",
    "pass_accuracy",
    "dribbles_attempted",
    "successful_dribbles",
    "crosses",
    "successful_crosses",
    "tackles",
    "interceptions",
    "clearances",
    "blocks",
    "aerial_duals_won",
    "aerial_duals_lost",
    "recoveries",
    "defensive_actions",
    "fouls_committed",
    "fouls_suffered",
    "yellow_cards",
    "red_cards",
    "offsides",
    "saves",
    "save_percentage",
    "punches",
    "clean_sheet",
    "goals_conceded",
    "penalty_saves",
    "distance_covered_km",
    "sprint_distance_km",
    "top_speed_kmh",
    "accelerations",
    "decelerations",
]

# Derived performance metrics
derived_performance_columns = [
    "stamina_score",
    "player_rating",
    "performance_score",
    "offensive_contribution",
    "defensive_contribution",
    "possession_impact",
    "pressure_resistance",
    "creativity_score",
    "consistency_score",
    "clutch_performance_score",
]

# Tournament-level information
tournament_columns = [
    "total_goals_tournament",
    "total_assists_tournament",
    "total_minutes_tournament",
    "player_of_the_match_awards",
    "tournament_rating",
] 

#--------------------------------------------------------------------------------------------
# Validate column classification

all_classified_columns = (
    player_profile_columns
    + match_information_columns
    + match_result_columns
    + match_performance_columns
    + derived_performance_columns
    + tournament_columns
)

print("\nColumn classification: ")
print("Player profile columns: ", len(player_profile_columns))
print("Match information columns: ", len(match_information_columns))
print("Match result columns: ", len(match_result_columns))
print("Match performance columns: ", len(match_performance_columns))
print("Derived performance columns: ")
print("Tournament columns", len(tournament_columns))

print("\nTotal classified columns: ", len(all_classified_columns))
print("Total dataset columns: ", len(players.columns))

# Check for missing classifications
unclassified_columns = [
    column for column in players.columns
    if column not in all_classified_columns
]

print("\nUnclassified columns: ")
print(unclassified_columns)

# Check for duplicate classifications
duplicate_classifications = [
    column
    for column in set(all_classified_columns)
    if all_classified_columns.count(column) > 1
]

print("\nColumns classified more than once: ")
print(duplicate_classifications)

print("\nClassified columns not found in dataset: ")
classified_not_in_dataset = [
    column
    for column in all_classified_columns
    if column not in players.columns
]

print(classified_not_in_dataset)

#----------------------
# Saved cleaned data

OUTPUT_FILE = PROCESSED_DATA / "players_cleaned.csv"

players.to_csv(OUTPUT_FILE, index = False)

print("\nCleaned player dataset saved to: ")
print(OUTPUT_FILE)
