#------------------------------------------------------------------------
# 10_predict_match.py
#
# This file will generate predictions for the 2026 World Cup fixtures.
#
# This Script:
# 1. Loads the production model and shared FeatureBuilder
# 2. Loads the 2026 schedule
# 3. Predicts every fixture BOTH ways and averages the two.
# 4. Saves predictions_2026.csv for the website
#
# Why both ways:
#       89% of the World Cup matches in the training data were played 
# at neutral venues, so "home team" in that data is really just 
# listing order, not a home advantage. The listed home team also 
# happened to be the stronger side more often than not, which the 
# model partly learned as a position effect. Averaging both orderings 
# removes it.  
# 
# All feature building lives in ml/features.py so this file and the API
# can never drift apart.
#-----------------------------------------------------------------------

import sys
import pandas as pd

from pathlib import Path

#------------------------------------------------------------------------
# Make the project root importable
# 
# Python puts this script's own folder on the path, not the repo root, 
# so "from ml.features import..." needs the root added manually. 
#------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(PROJECT_ROOT))

from ml.features import(
    FeatureBuilder,
    load_model,
    predict_fixtures,
)

#------------------------------------------------------------------------
# File Paths
#------------------------------------------------------------------------

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
RAW_DATA = PROJECT_ROOT / "data" / "raw"

SCHEDULE_FILE = RAW_DATA / "schedule_2026.csv"
PREDICTIONS_FILE = PROCESSED_DATA / "predictions_2026.csv"

print("\nFile paths configured successfully!")

#------------------------------------------------------------------------
# Load model and features builder
#------------------------------------------------------------------------

builder = FeatureBuilder()
model = load_model()

print("\nProduction model loaded successfully!")
print("Expected features: ", len(builder.model_features))
print("Teams with history: ", len(builder.team_lookup))

#------------------------------------------------------------------------
# Load 2026 schedule
#------------------------------------------------------------------------

schedule = pd.read_csv(SCHEDULE_FILE)

schedule = schedule[
    schedule["home_team"].notna()
    & schedule["away_team"].notna()
].reset_index(drop = True)

print("\n2026 schedule loaded.")
print("Fixtures with both teams known: ", len(schedule))

#------------------------------------------------------------------------
# Report teams with no World Cup history 
#------------------------------------------------------------------------

teams_without_history = sorted({
    team
    for team in(
        list(schedule["home_team"]) +list(schedule["away_team"])
    )
    if not builder.has_history(team)
})

if teams_without_history:
    print("\nTeams with no World Cup History (ranking features only): ")
    for team in teams_without_history:
        print(" -", team)

#------------------------------------------------------------------------
# Predict every fixture in both orderings
#------------------------------------------------------------------------

forward_pairs = [
    (fixture["home_team"], fixture["away_team"])
    for _, fixture in schedule.iterrows()
]

reverse_pairs = [
    (away, home)
    for home, away in forward_pairs
]

forward = predict_fixtures(model, builder, forward_pairs)
reverse = predict_fixtures(model, builder, reverse_pairs)

print("\nPredictions generated (both orderings).")

#------------------------------------------------------------------------
# Average the two orderings
#
# In the reverse run the teams are swapped, so that run's "Away Win" is 
# the listed home team winning, and vice versa.
#------------------------------------------------------------------------

averaged = []
for f, r in zip(forward, reverse):
    averaged.append({
        "Home Win": round((f["Home Win"] + r["Away Win"]) / 2, 4),
        "Draw": round((f["Draw"] + r["Draw"]) / 2, 4),
        "Away Win": round((f["Away Win"] + r["Home Win"]) / 2, 4),
    })

#------------------------------------------------------------------------
# Build Output Table
#------------------------------------------------------------------------

results = pd.DataFrame({
    "Round": schedule["Round"].values, 
    "Date": schedule["Date"].values,
    "Home Team": schedule["home_team"].values,
    "Away Team": schedule["away_team"].values,
})

for label in ["Home Win", "Draw", "Away Win"]:
    results[label + " Probability"] = [
        row[label] for row in averaged
    ]

results["Predicted Result"] = [
    max(row, key = row.get)
    for row in averaged
]

results["Confidence"] = [
    round(max(row.values()), 4)
    for row in averaged
]

#------------------------------------------------------------------------
# Sanity Checks
#------------------------------------------------------------------------

totals = [
    round(sum(row.values()), 4)
    for row in averaged
]

print("\nProbability rows summing to 1: ")
print(sum(1 for t in totals if abs(t - 1.0) < 0.001), "of", len(results))

print("\nPredicted result distribution: ")
print(results["Predicted Result"].value_counts())

#------------------------------------------------------------------------
# Preview
#------------------------------------------------------------------------

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

#------------------------------------------------------------------------
# Save
#------------------------------------------------------------------------

results.to_csv(
    PREDICTIONS_FILE,
    index = False
)

print("\nPredictions saved to: ")
print(PREDICTIONS_FILE)

#------------------------------------------------------------------------
# Summary
#------------------------------------------------------------------------

print("\n" + "=" * 70)
print("10_ COMPLETE!!!")
print("=" * 70)
print("Fixtures used: ", len(results))
print("Teams withouth history: ", len(teams_without_history))
print("\nOutput: ")
print(" -", PREDICTIONS_FILE.name)
print("=" * 70)