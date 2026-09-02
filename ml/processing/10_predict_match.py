#------------------------------------------------------------------------
# 10_predict_match.py
#
# This file will generate predictions for the 2026 World Cup fixtures.
#
# This Script:
# 1. Loads the production model and its feature list
# 2. Loads each team's current feature state from 04_
# 3. Loads 2026 FIFA rankings
# 4. Builds a feature row for every fixture in schedule_2026.csv
# 5. Predict outcome probabilities
# 6. Saves predictions_2026.csv for the website
#
# Note: the teams with no WC history get 0.0 for the history
# based features. This is exactly what 04_ does with a team's 
# first ever match, so the model is familiar with with this pattern
# during training.
#
# features are still real, which is what carries the prediction.
#
#-----------------------------------------------------------------------

import pandas as pd
import joblib
import json

from pathlib import Path

#----------------------------------------------------------------
# File Paths
#----------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
RAW_DATA = PROJECT_ROOT / "data" / "raw"
MODEL_DATA = PROJECT_ROOT / "ml" / "models" 

MODEL_FILE = MODEL_DATA / "logistic_regression_final.pkl"
FEATURE_FILE = MODEL_DATA / "model_features.json"

TEAM_FEATURES_FILE = PROCESSED_DATA / "team_features_current.csv"
RANKING_2026_FILE = PROCESSED_DATA / "fifa_ranking_2026_cleaned.csv"
SCHEDULE_FILE = RAW_DATA / "schedule_2026.csv"

PREDICTIONS_FILE = PROCESSED_DATA / "predictions_2026.csv"

print("\nFile paths configured successfully!")

#----------------------------------------------------------------
# Team Name Aliases
#----------------------------------------------------------------

SCHEDULE_TO_HISTORY ={
    "Czechia": "Czech Republic",
}

def history_name(schedule_team):
    return SCHEDULE_TO_HISTORY.get(schedule_team, schedule_team)

#----------------------------------------------------------------
# Load production Model
#----------------------------------------------------------------

model = joblib.load(MODEL_FILE)

with open(FEATURE_FILE) as f:
    model_features = json.load(f)

print("\nProduction model loaded successfully!")
print("Expected features: ", len(model_features))

#----------------------------------------------------------------
# Load team feature state
#----------------------------------------------------------------

team_features =pd.read_csv(TEAM_FEATURES_FILE)

team_lookup = team_features.set_index("team").to_dict("index")

print("\nTeam feature state loaded.")
print("Teams with history: ", len(team_lookup))

#----------------------------------------------------------------
# Load 2026 FIFA rankings
#----------------------------------------------------------------

ranking_2026 = pd.read_csv(RANKING_2026_FILE)

ranking_2026["team"] = ranking_2026["team"].str.strip()

ranking_2026["rank"] = pd.to_numeric(
    ranking_2026["rank"],
    errors = "coerce"
)

ranking_lookup = ranking_2026.set_index("team")["rank"].to_dict()
points_lookup = ranking_2026.set_index("team")["points"].to_dict()

worst_rank = ranking_2026["rank"].max() + 1

print("\n2026 FIFA ranking loaded.")
print("Fallback rank for unranked teams: ", worst_rank)

#----------------------------------------------------------------
# Load 2026 schedule
#----------------------------------------------------------------

schedule = pd.read_csv(SCHEDULE_FILE)

schedule = schedule[
    schedule["home_team"].notna()
    & schedule["away_team"].notna()
].reset_index(drop = True)

print("\n2026 schedule loaded.")
print("Fixtures with both teams known: ", len(schedule))

#----------------------------------------------------------------
# Default features values for teams with no World Cup History
#----------------------------------------------------------------

EMPTY_HISTORY = {
    "matches_played": 0,
    "win_rate": 0.0,
    "avg_goals_scored": 0.0,
    "avg_goals_conceded": 0.0,
    "goal_difference": 0.0,
    "recent_win_rate": 0.0,
    "recent_avg_goals_scored": 0.0,
    "recent_avg_goals_conceded": 0.0,
    "recent_goal_difference": 0.0,
}

def get_team_stats(schedule_team):
    return team_lookup.get(
        history_name(schedule_team),
        EMPTY_HISTORY
    )

#----------------------------------------------------------------
# Build features rows
#
# Column names below must match model_features.json exactly.
# Note the inconsistent pluralisation carried over from 04_:
#
# goal_difference          ==> home_goal_differences (plural)
# recent_win_rate          ==> home_recent_win_rate (plural)
# recent_goal_difference   ==> home_recent_goal_difference (singular)
#
#----------------------------------------------------------------

feature_rows = []
teams_without_history = set()

for _, fixture in schedule.iterrows():
    home_team = fixture["home_team"]
    away_team = fixture["away_team"]


    home = get_team_stats(home_team)
    away = get_team_stats(away_team)

    if history_name(home_team) not in team_lookup:
        teams_without_history.add(home_team)

    if history_name(away_team) not in team_lookup:
        teams_without_history.add(away_team)

    #----------------------------------------------------------------
    # FIFA ranking values
    #----------------------------------------------------------------

    home_rank = ranking_lookup.get(home_team, worst_rank)
    away_rank = ranking_lookup.get(away_team, worst_rank)

    home_points = points_lookup.get(home_team, 0.0)
    away_points = points_lookup.get(away_team, 0.0)

    #----------------------------------------------------------------
    # Assemble the 32 model features
    #
    # rank_difference and points_difference follow 04_ exactly:
    # positive rank_difference = home team has the better FIFA rank
    # positive points_difference = home team has more ranking points
    #
    #----------------------------------------------------------------

    feature_rows.append({
        # Overall historical performance
        "home_win_rate": home["win_rate"],
        "away_win_rate": away["win_rate"],

        "home_avg_goals_scored": home["avg_goals_scored"],
        "away_avg_goals_scored": away["avg_goals_scored"],

        "home_avg_goals_conceded": home["avg_goals_conceded"],
        "away_avg_goals_conceded": away["avg_goals_conceded"],

        "home_matches_played": home["matches_played"],
        "away_matches_played": away["matches_played"],

        "home_goal_differences": home["goal_difference"],
        "away_goal_differences": away["goal_difference"],

        # Recent form
        "home_recent_win_rates": home["recent_win_rate"],
        "away_recent_win_rates": away["recent_win_rate"],

        "home_recent_avg_goals_scored": home["recent_avg_goals_scored"],
        "away_recent_avg_goals_scored": away["recent_avg_goals_scored"],

        "home_recent_avg_goals_conceded": home["recent_avg_goals_conceded"],
        "away_recent_avg_goals_conceded": away["recent_avg_goals_conceded"],

        "home_recent_goal_difference": home["recent_goal_difference"],
        "away_recent_goal_difference": away["recent_goal_difference"],

        # Matchup differences
        "win_rate_difference": (
            home["win_rate"] - away["win_rate"]
        ),
        "recent_win_rate_difference": (
            home["recent_win_rate"] - away["recent_win_rate"]
        ),
        "goal_scoring_difference": (
            home["avg_goals_scored"] - away["avg_goals_scored"]
        ),
        "recent_goal_scoring_difference": (
            home["recent_avg_goals_scored"] - away["recent_avg_goals_scored"]
        ),
        "goal_conceding_difference": (
            home["avg_goals_conceded"] - away["avg_goals_conceded"]
        ),
        "recent_goal_conceding_difference": (
            home["recent_avg_goals_conceded"] - away["recent_avg_goals_conceded"]
        ),
        "goal_difference_comparison": (
            home["goal_difference"] - away["goal_difference"]
        ),
        "recent_goal_difference_comparison": (
            home["recent_goal_difference"] - away["recent_goal_difference"]
        ),

        # FIFA ranking strength
        "home_rank": home_rank,
        "away_rank": away_rank,

        "home_points": home_points,
        "away_points": away_points,

        "rank_difference": away_rank - home_rank,
         "points_difference": home_points - away_points,                    
    })
X_2026 = pd.DataFrame(feature_rows)

#----------------------------------------------------------------
# Validate features before predicting
#
# Reordering to match model_features.json is the important step here.
# A wrong column order still run and produce confident nonsense. 
# 
#----------------------------------------------------------------

missing = [
    column
    for column in model_features
    if column not in X_2026.columns
]

extra = [
    column
    for column in X_2026.columns
    if column not in model_features
]

if missing:
    raise ValueError(
        f"Features missing from the 2026 feature frame: {missing}"
    )
if extra:
    raise ValueError(
        f"Unexpected features in the 2026 feature frame: {extra}"
    )

X_2026 = X_2026[model_features]

print("\nFeature frame built and validated.")
print("Shape: ", X_2026.shape)

if teams_without_history:
    print("\nTeams with no World Cup History (ranking features only): ")
    for team in sorted(teams_without_history):
        print(" -", team)

#----------------------------------------------------------------
# Predicting
#
# Read classes_ from the model rather than assuming an order. 
# The production model orders them alphabetically: Away Win, 
# Draw, Home Win. 
#  
#----------------------------------------------------------------

predictions = model.predict(X_2026)
probabilities = model.predict_proba(X_2026)

model_classes = list(model.named_steps["model"].classes_)

print("\nPredictions generated.")
print("Class order from model: ", model_classes)

#----------------------------------------------------------------
# Build Output Table
#----------------------------------------------------------------

results = pd.DataFrame({
    "Round": schedule["Round"].values,
    "Date": schedule["Date"].values,
    "Home Team": schedule["home_team"].values,
    "Away Team": schedule["away_team"].values,
    "Predicted Result": predictions,
})

for label in ["Home Win", "Draw", "Away Win"]:
    results[label + " Probability"] = probabilities[
        :, model_classes.index(label)
    ].round(4)

results["Confidence"] = probabilities.max(axis = 1).round(4)

#-----------------------------------------------------------------
# Sanity Checks
#-----------------------------------------------------------------

probability_totals = probabilities.sum(axis = 1).round(6)

print("\nProbability rows summing to 1: ")
print((probability_totals == 1.0).sum(), "of", len(results))

print("\nPredicted result distribution: ")
print(results["Predicted Result"].value_counts())

#-----------------------------------------------------------------
# Preview
#-----------------------------------------------------------------

print("\n" + "=" * 70)
print("SAMPLE PREDICTIONS")
print("=" * 70)

print(
    results.head(10)[[
        "Home Team",
        "Away Team",
        "Predicted Result",
        "Home Win Probability",
        "Draw Probability",
        "Away Win Probability",
    ]].to_string(index = False)
)

#-----------------------------------------------------------------
# Save
#-----------------------------------------------------------------

results.to_csv(
    PREDICTIONS_FILE,
    index= False
)

print("\nPredictions saved to: ")
print(PREDICTIONS_FILE)

#-----------------------------------------------------------------
# Summary
#-----------------------------------------------------------------

print("\n" + "=" * 70)
print("10_ COMPLETE!!!")
print("=" * 70)
print("Fixtures used: ", len(results))
print("Teams without history ", len(teams_without_history))
print("\nOutput: ")
print(" -", PREDICTIONS_FILE.name)
print("=" * 70)

