#------------------------------------------------------------------------------------
#04_build_training_dataset.py
#
# Updated 04_ file, new version is optomizing the ML trained dataset for stonger 
# predictions.
#
# The script:
# 1.Loads the cleaned World Cup match data
# 2.Creates match result target
# 3.Calculates historical team statistics
# 4.Calculate recent form statistics
# 5.Calculates goal difference stats
# 6.Creates matchup difference features
# 7.Checks for data leakage
# 8.Validates final dataset
# 9.Saves training_dataset.csv 
#-----------------------------------------------------------------------------------
import pandas as pd
from pathlib import Path

#-----------------------------------------------------------------------------------
# File paths
#-----------------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA = PROJECT_ROOT /  "data" / "processed"
MATCHES_FILE = PROCESSED_DATA  /  "matches_cleaned.csv"
OUTPUT_FILE = PROCESSED_DATA  / "training_dataset.csv"

#-------------------------------------------------------------------------------------
# Configuration
#-----------------------------------------------------------------------------------

# number of previous matches used for recent from features
RECENT_MATCHES = 5

#--------------------------------------------------------------------------------------
# Load match dataset
#-----------------------------------------------------------------------------------

matches = pd.read_csv(MATCHES_FILE)

print("\nMatches loaded successfully!")
print("Shape: ", matches.shape)

#-----------------------------------------------------------------------------------
# Basic Validation
#-----------------------------------------------------------------------------------

required_columns = [
     "home_team",
     "away_team",
     "home_score",
     "away_score",
     "Date"
]

missing_columns =[
    column
    for column in required_columns
    if column not in matches.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

#-----------------------------------------------------------------------------------
# Prepare date column
#-----------------------------------------------------------------------------------

matches["Date"] =pd.to_datetime(matches["Date"])

matches = matches.sort_values(
    "Date"
).reset_index(drop= True)

print("\nDataset sorted chronologically.")

print("Date range: ")
print(matches["Date"].min())
print("to")
print(matches["Date"].max())

#-----------------------------------------------------------------------------------
# Create target variable
#-----------------------------------------------------------------------------------

def determine_match_result(row):
    if row["home_score"] > row["away_score"]:
        return "Home Win"
    
    elif row["home_score"] < row["away_score"]:
        return "Away Win"

    else: return "Draw"

matches["match_result"] = matches.apply(
    determine_match_result,
    axis=1
)

#-----------------------------------------------------------------------------------
# Validate target
#-----------------------------------------------------------------------------------

print("\nMatch result distribution: ")
print(
    matches["match_result"].value_counts()
)

print("\nMatch result percentages: ")
print(
    matches["match_result"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

#-----------------------------------------------------------------------------------
# TEAM HISTORY
#-----------------------------------------------------------------------------------
"""
each team's history contains only matches that happened before 
the current match being processed

Current match
      ↓
Calculate features using old history
      ↓      
Add current match to history

this allows current result cannot leak into its own features
"""
team_history = {}

#-----------------------------------------------------------------------------------
# Feature Storage
#-----------------------------------------------------------------------------------

# This is the overall historical features

home_win_rates = []
away_win_rates = []

home_avg_goals_scored = []
away_avg_goals_scored = []

home_avg_goals_conceded = []
away_avg_goals_conceded = []

home_matches_played = [] 
away_matches_played = [] 

home_goal_differences = []
away_goal_differences = []

# Recent form features

home_recent_win_rates =[]
away_recent_win_rates =[]

home_recent_avg_goals_scored = []
away_recent_avg_goals_scored = []

home_recent_avg_goals_conceded = []
away_recent_avg_goals_conceded = []

home_recent_goal_differences = []
away_recent_goal_differences = []

#-----------------------------------------------------------------------------------
# PROCESS MATCHES CHRONOLOGICALLY
#-----------------------------------------------------------------------------------

for _, row in matches.iterrows():
    home_team = row["home_team"]
    away_team = row["away_team"]

    #---------------------------------------------------------------------------------
    # Get historical records
    #---------------------------------------------------------------------------------

    home_history = team_history.get(
        home_team,
        []
    )

    away_history = team_history.get(
        away_team,
        []
    )

    #---------------------------------------------------------------------------------
    # HOME TEAM OVERALL FEATURES
    #---------------------------------------------------------------------------------
    if len(home_history) > 0:
        home_wins = sum(
            result["win"]
            for result in home_history
        )
        home_goals_scored =sum(
            result["goals_scored"]
            for result in home_history
        )

        home_goals_conceded = sum(
            result["goals_conceded"]
            for result in home_history
        )

        home_goal_difference = (
            home_goals_scored
            - home_goals_conceded
        )

        home_win_rates.append(
            home_wins / len(home_history)
        )
        home_avg_goals_scored.append(
            home_goals_scored / len(home_history)
        )
        home_avg_goals_conceded.append(
            home_goals_conceded / len(home_history)
        )
        home_goal_differences.append(
            home_goal_difference / len(home_history)
        )
    else:
        home_win_rates.append(0.0)
        home_avg_goals_conceded.append(0.0)
        home_avg_goals_scored.append(0.0)
        home_goal_differences.append(0.0)

    home_matches_played.append(
        len(home_history)
    )

    #--------------------------------------------------------------------------------
    # AWAY TEAM OVERALL FEATURES
    #--------------------------------------------------------------------------------
    if len(away_history) > 0:
        away_wins = sum(
            result["win"]
            for result in away_history
        )

        away_goals_scored = sum(
            result["goals_scored"]
            for result in away_history
        )

        away_goals_conceded = sum(
            result["goals_conceded"]
            for result in away_history
        )

        away_goal_difference = (
            away_goals_scored
            - away_goals_conceded
        )

        away_win_rates.append(
            away_wins / len(away_history)
        )
        away_avg_goals_scored.append(
            away_goals_scored / len(away_history)
        )
        away_avg_goals_conceded.append(
            away_goals_conceded / len(away_history)
        )
        away_goal_differences.append(
            away_goal_difference / len(away_history)
        )
    else:
        away_win_rates.append(0.0)
        away_avg_goals_scored.append(0.0)
        away_avg_goals_conceded.append(0.0)
        away_goal_differences.append(0.0)

    away_matches_played.append(
        len(away_history)
    )

    #-------------------------------------------------------------------------------------
    # RECENT FORM
    #-------------------------------------------------------------------------------------

    """
    only using teams previously N matches.

    examples
    RECENT_MATCHES = 5

    the current match is not included.

    """
    home_recent_history = home_history[-RECENT_MATCHES:]
    away_recent_history = away_history[-RECENT_MATCHES:]

    #-------------------------------------------------------------------------------------
    # Home recent form
    #-------------------------------------------------------------------------------------

    if len(home_recent_history) > 0:
        recent_home_wins = sum(
            result["win"]
            for result in home_recent_history
        )
        recent_home_goals_scored = sum(
            result["goals_scored"]
            for result in home_recent_history
        )
        recent_home_goals_conceded = sum(
            result["goals_conceded"]
            for result in home_recent_history
        )

        recent_home_goal_difference = (
            recent_home_goals_scored
            -recent_home_goals_conceded
        )

        home_recent_win_rates.append(
            recent_home_wins
            / len(home_recent_history)
        )
        home_recent_avg_goals_scored.append(
            recent_home_goals_scored 
            / len(home_recent_history)
        )
        home_recent_avg_goals_conceded.append(
            recent_home_goals_conceded
            / len(home_recent_history)
        )
        home_recent_goal_differences.append(
            recent_home_goal_difference
            / len(home_recent_history)
        )

    else: 
        home_recent_win_rates.append(0.0)
        home_recent_avg_goals_scored.append(0.0)
        home_recent_avg_goals_conceded.append(0.0)
        home_recent_goal_differences.append(0.0)

    #-------------------------------------------------------------------------------------
    # Away recent form
    #------------------------------------------------------------------------------------

    if len(away_recent_history) > 0:
        recent_away_wins = sum(
            result["win"]
            for result in away_recent_history
        )
        recent_away_goals_scored = sum(
            result["goals_scored"]
            for result in away_recent_history
        )
        recent_away_goals_conceded = sum(
            result["goals_conceded"]
            for result in away_recent_history
        )

        recent_away_goal_difference = (
            recent_away_goals_scored
            -recent_away_goals_conceded
        )

        away_recent_win_rates.append(
            recent_away_wins
            / len(away_recent_history)
        )
        away_recent_avg_goals_scored.append(
            recent_away_goals_scored 
            / len(away_recent_history)
        )
        away_recent_avg_goals_conceded.append(
            recent_away_goals_conceded
            / len(away_recent_history)
        )
        away_recent_goal_differences.append(
            recent_away_goal_difference
            / len(away_recent_history)
        )

    else: 
        away_recent_win_rates.append(0.0)
        away_recent_avg_goals_scored.append(0.0)
        away_recent_avg_goals_conceded.append(0.0)
        away_recent_goal_differences.append(0.0)

    #-------------------------------------------------------------------------------------
    # UPDATE TEAM HISTORY
    #-------------------------------------------------------------------------------------
    # Determine result from the CURRENT match.
    if row["home_score"] > row["away_score"]:
        home_win = 1
        away_win = 0

    elif row["home_score"] < row["away_score"]:
        home_win = 0 
        away_win = 1

    else:
        home_win = 0
        away_win = 0

    #-------------------------------------------------------------------------------------
    # Add home team's current match
    #-------------------------------------------------------------------------------------
    if home_team not in team_history:
        team_history[home_team] = []

    team_history[home_team].append(
        {
            "win": home_win,
            "goals_scored": row["home_score"],
            "goals_conceded": row["away_score"]
        }
    )

    #-------------------------------------------------------------------------------------
    # Add away team's current match
    #-------------------------------------------------------------------------------------
    if away_team not in team_history:
        team_history[away_team] = []

    team_history[away_team].append(
        {
            "win": away_win,
            "goals_scored": row["away_score"],
            "goals_conceded": row["home_score"]
        }
    )

#-------------------------------------------------------------------------------------
# ADDING FEATURES TO DATASET
# Overall historicall features
#-------------------------------------------------------------------------------------
matches["home_win_rate"] = home_win_rates
matches["away_win_rate"] = away_win_rates

matches["home_avg_goals_scored"] = home_avg_goals_scored
matches["away_avg_goals_scored"] = away_avg_goals_scored

matches["home_avg_goals_conceded"] = home_avg_goals_conceded
matches["away_avg_goals_conceded"] = away_avg_goals_conceded

matches["home_matches_played"] = home_matches_played
matches["away_matches_played"] = away_matches_played

matches["home_goal_differences"] = home_goal_differences
matches["away_goal_differences"] = away_goal_differences

#-------------------------------------------------------------------------------------
# Recent form features
#-------------------------------------------------------------------------------------
matches["home_recent_win_rates"] = home_recent_win_rates
matches["away_recent_win_rates"] = away_recent_win_rates

matches["home_recent_avg_goals_scored"] = (
    home_recent_avg_goals_scored
)
matches["away_recent_avg_goals_scored"] = (
    away_recent_avg_goals_scored
)
matches["home_recent_avg_goals_conceded"] = (
    home_recent_avg_goals_conceded
)
matches["away_recent_avg_goals_conceded"] = (
    away_recent_avg_goals_conceded
)
matches["home_recent_goal_difference"] = (
    home_recent_goal_differences
)
matches["away_recent_goal_difference"] = (
    away_recent_goal_differences
)

#-------------------------------------------------------------------------------------
# MATCHUP DIFFERENCE FEATURES 
#-------------------------------------------------------------------------------------
# Theses explicitly tell the model which team has the advantage
# for each mahor statical category.
matches["win_rate_difference"] = (
    matches["home_win_rate"]
    -matches["away_win_rate"]
)
matches["recent_win_rate_difference"] = (
    matches["home_recent_win_rates"]
    -matches["away_recent_win_rates"]
)
matches["goal_scoring_difference"] = (
    matches["home_avg_goals_scored"]
    -matches["away_avg_goals_scored"]
)
matches["recent_goal_scoring_difference"] =(
    matches["home_recent_avg_goals_scored"]
    -matches["away_recent_avg_goals_scored"]
)
matches["goal_conceding_difference"] =(
    matches["home_avg_goals_conceded"]
    -matches["away_avg_goals_conceded"]
)
matches["recent_goal_conceding_difference"] =(
    matches["home_recent_avg_goals_conceded"]
    -matches["away_recent_avg_goals_conceded"]
)
matches["goal_difference_comparison"] =(
    matches["home_goal_differences"]
    -matches["away_goal_differences"]
)
matches["recent_goal_difference_comparison"] =(
    matches["home_recent_goal_difference"]
    -matches["away_recent_goal_difference"]
)

#-------------------------------------------------------------------------------------
# DEFINE ML FEATURES
#-------------------------------------------------------------------------------------
ml_features = [
    #----------------------------------------------
    # Overall historical performance
    #----------------------------------------------
    "home_win_rate",
    "away_win_rate",

    "home_avg_goals_scored",
    "away_avg_goals_scored",

    "home_avg_goals_conceded",
    "away_avg_goals_conceded",

    "home_matches_played",
    "away_matches_played",

    "home_goal_differences",
    "away_goal_differences",

    #----------------------------------------------
    # Recent form
    #----------------------------------------------
    "home_recent_win_rates",
    "away_recent_win_rates",

    "home_recent_avg_goals_scored",
    "away_recent_avg_goals_scored",

    "home_recent_avg_goals_conceded",
    "away_recent_avg_goals_conceded",

    "home_recent_goal_difference",
    "away_recent_goal_difference",

    #----------------------------------------------
    # Matchup differences
    #----------------------------------------------
    "win_rate_difference",

    "recent_win_rate_difference",

    "goal_scoring_difference",

    "recent_goal_scoring_difference",

    "goal_conceding_difference",

    "recent_goal_conceding_difference",

    "goal_difference_comparison",

    "recent_goal_difference_comparison"
]

#-------------------------------------------------------------------------------------
#  CREATE ML DATASET
#-------------------------------------------------------------------------------------

X = matches[ml_features].copy()
y = matches["match_result"].copy()

#-------------------------------------------------------------------------------------
# VALIDATION
#-------------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("ML DATASET VALIDATION")
print("=" * 80)

#-------------------------------------------------------------------------------------
# Feature shape
#-------------------------------------------------------------------------------------
print("\nML feature dataset shape: ")
print(X.shape)

#-------------------------------------------------------------------------------------
# Feature list
#-------------------------------------------------------------------------------------
print("\nML features: ")
for feature in ml_features:
    print(" -", feature)

print("\nNumber of ML features: ")
print(len(ml_features))

#-------------------------------------------------------------------------------------
# Target
#-------------------------------------------------------------------------------------

print("\nTarger shape:")
print(y.shape)

print("\nTarget distribution: ")
print(y.value_counts())

#-------------------------------------------------------------------------------------
# Missing Values
#-------------------------------------------------------------------------------------

missing_values = X.isnull().sum()

print("\nMissing values in ML features: ")
print(missing_values)

total_missing = missing_values.sum()

print("\nTotal missing values: ")
print(total_missing)

if total_missing > 0:
    raise ValueError(
        "Missing values detected in ML features."
    )

#-------------------------------------------------------------------------------------
# DATA LEAKAGE CHECK
#-------------------------------------------------------------------------------------

leakage_columns =[
    "home_score",
    "away_score",

    "home_xg",
    "away_xg",

    "home_penalty",
    "awau_penalty",

    "home_goal",
    "away_goal",

    "home_goal_long",
    "away_goal_long",

    "home_own_goal",
    "away_own_goal",

    "home_penalty_goal",
    "away_penalty_goal",

    "home_penalty_miss_long",
    "away_penalty_miss_long",

    "home_penalty_shootout_goal_long",
    "away_penalty_shootout_goal_long",

    "home_penalty_shootout_miss_long",
    "away_penalty_shootout_miss_long",

    "home_red_card",
    "away_red_card",

    "home_yellow_red_card",
    "away_yellow_red_card",

    "home_yellow_card_long",
    "away_yellow_card_long",

    "home_substitute_in_long",
    "away_substitute_in_long",
]

leakage_in_features =[
    column
    for column in leakage_columns
    if column in X.columns
]

print("\nData leakage check: ")

if len(leakage_in_features) == 0:
    print(
        "PASS - no match event or final score columns "
        "are included in the ML features."
    )
else:
    print(
        "WARNING POTENTIAL; LEAKAGE DETECTED!"
    )
    print(leakage_in_features)

    raise ValueError(
        "POTENTIAL DATA LEAKAGE DETECTED!"
    )

#-------------------------------------------------------------------------------------
# FEATURE VALIDATION
#-------------------------------------------------------------------------------------

missing_ml_features =[
    column 
    for column in ml_features
    if column not in matches.columns
]

print("\nMissing ML feature columns: ")

if len(missing_ml_features) == 0:
    print("None all ML features exist!")

else: 
    print(missing_ml_features)

    raise ValueError(
        "One or more ML features are missing."
    )

#-------------------------------------------------------------------------------------
# CREATE FINAL TRAINING DATASET
#-------------------------------------------------------------------------------------

training_dataset = matches[
    ["Date"] + ml_features
].copy()

training_dataset["match_result"] = y

print("\n" + "=" * 80)
print("FINAL TRAINING DATASET")
print("=" * 80)

print("\nShape: ")
print(training_dataset.shape)

print("\nColumns: ")
print(training_dataset.columns.tolist())

#-------------------------------------------------------------------------------------
# SAVE DATASET
#-------------------------------------------------------------------------------------

training_dataset.to_csv(
    OUTPUT_FILE,
    index = False
)

print("\nTraining dataset saved to:")
print(OUTPUT_FILE)

#-------------------------------------------------------------------------------------
# VERIFY SAVED DATASET
#-------------------------------------------------------------------------------------

verified_dataset = pd.read_csv(
    OUTPUT_FILE
)

print("\n" + "=" * 80)
print("SAVED DATASET VERIFICATION")
print("=" * 80)

print("\nShape: ")
print(verified_dataset.shape)

print("\nNumber of columns:")
print(len(verified_dataset.columns))

#-------------------------------------------------------------------------------------
# MISSING VALUES
#-------------------------------------------------------------------------------------
verified_missing = (
    verified_dataset.isnull().sum().sum()
) 

print("\nMissing values: ")
print(verified_missing)

#-------------------------------------------------------------------------------------
# DUPLICATE ROWS
#-------------------------------------------------------------------------------------

duplicate_count =(
    verified_dataset.duplicated().sum()
)

print("\nDuplicate rows: ")
print(duplicate_count)

#-------------------------------------------------------------------------------------
# TARGER DISTRIIBUTION
#-------------------------------------------------------------------------------------

print("\nTarget distribution: ")
print(
    verified_dataset["match_result"].value_counts()
)

#-------------------------------------------------------------------------------------
# FINAL SUMMARY
#-------------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("TRAINING DATASET READY")
print("=" * 80)

print("Matches: ", len(verified_dataset))

print("Features: ", len(ml_features))

print("Recent form window: ", RECENT_MATCHES, "matches")

print("Missing values: ", verified_missing)

print("Duplicate rows: ", duplicate_count)

print("\nOutput: ")
print(OUTPUT_FILE)

print("=" * 80)