#-------------------------------------------------------------
# features.py
#
#  Shared feature building logic.
#
# 10_predict_match.py and the API both import from this 
# file so the two can never drift apart.If a feature ever 
# changes, it changes here once. 
#
# Usage:
#   from ml.features import FeatureBuilder
#
# builder = FeatureBuilder()
# row = builder.build_row("Brazil", "Argentina")
# frame = builder.build_frame([("Brazil", "Argentina"), ("Spain", "Japan")])
#
#----------------------------------------------------------------

import pandas as pd
import joblib
import json

from pathlib import Path

#-------------------------------------------------------------------
# File paths
#-------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
MODEL_DATA = PROCESSED_DATA / "ml" / "models"

MODEL_FILE = MODEL_DATA / "logistic_regression_final.pkl"
FEATURE_FILE = MODEL_DATA / "model_features.json"

TEAM_FEATURES_FILE = PROCESSED_DATA / "team_features_current.csv"
RANKING_2026_FILE = PROCESSED_DATA / "fifa_ranking_2026_cleaned.csv"

#-------------------------------------------------------------------
# Team name Aliases
# team_features_current.csv is keyed by the names used in the 
# historical match data. The 2026 schedule and ranking use 
# current FIFA names. 
#-------------------------------------------------------------------

SCHEDULE_TO_HISTORY = {
    "Czechia": "Czech Republic",
}

#-------------------------------------------------------------------
# Default values for teams with no World Cup History
# 
# 04_ appends 0.0 for a team's first ever match, so the model has 
# seen this exact pattern during training. Their FIFA ranking 
# features are still real, and those carry the prediction. 
# 
#-------------------------------------------------------------------
