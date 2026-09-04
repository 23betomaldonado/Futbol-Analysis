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

PROJECT_ROOT = Path(__file__).resolve().parents[0].parent

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
MODEL_DATA = PROJECT_ROOT / "ml" / "models"

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
EMPTY_HISTORY ={
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

class FeatureBuilder:
    """Builds model ready feature rows from team names."""

    def __init__(self):
        #------------------------------------------------------------
        # Model feature list
        #------------------------------------------------------------

        with open(FEATURE_FILE) as f:
            self.model_features = json.load(f)

        #------------------------------------------------------------
        # Team history lookup
        #------------------------------------------------------------
        
        team_features = pd.read_csv(TEAM_FEATURES_FILE)
        self.team_lookup = team_features.set_index("team").to_dict("index")

        #------------------------------------------------------------
        # FIFA Ranking Lookup
        #------------------------------------------------------------

        ranking = pd.read_csv(RANKING_2026_FILE)
        ranking["team"] = ranking["team"].str.strip()

        ranking["rank"] = pd.to_numeric(ranking["rank"], errors = "coerce")
        ranking["points"] = pd.to_numeric(ranking["points"], errors = "coerce")

        self.ranking_lookup = ranking.set_index("team")["rank"].to_dict()
        self.points_lookup = ranking.set_index("team")["points"].to_dict()

        self.worst_rank = ranking["rank"].max() + 1

        #------------------------------------------------------------
        # Every team the API is willing to accept
        #------------------------------------------------------------

        self.known_teams = sorted(self.ranking_lookup.keys())

    #------------------------------------------------------------
    # Helpers
    #------------------------------------------------------------

    def history_name(self, team):
        return SCHEDULE_TO_HISTORY.get(team, team)

    def has_history(self, team):
        return self.history_name(team) in self.team_lookup

    def get_team_stats(self, team):
        return self.team_lookup.get(
            self.history_name(team),
            EMPTY_HISTORY
        )

    #------------------------------------------------------------------
    # Build a single feature row
    # 
    # rank_difference and points_difference follow 04_exactly:
    #   positive rank_difference = home team has the better FIFA rank
    #   positive points_difference = home team has more ranking points
    #-------------------------------------------------------------------

    def build_row(self, home_team, away_team):
        home = self.get_team_stats(home_team)
        away = self.get_team_stats(away_team)

        home_rank = self.ranking_lookup.get(home_team, self.worst_rank)
        away_rank = self.ranking_lookup.get(away_team, self.worst_rank)

        home_points = self.points_lookup.get(home_team, 0.0)
        away_points = self.points_lookup.get(away_team, 0.0)

        return{
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

            # Recent Form
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

            "rank_difference": away_rank -home_rank,
            "points_difference": home_points - away_points,
        }

    #------------------------------------------------------------------
    # Build a validated frame from a list of (home, away) pairs
    # 
    # The reorder against model_features is the important step. A wrong
    # column order would still run and produce confident nonsense.
    #-------------------------------------------------------------------

    def build_frame(self, fixtures):
        rows = [
            self.build_row(home, away)
            for home, away in fixtures
        ]

        frame = pd.DataFrame(rows)

        missing = [
            column
            for column in self.model_features
            if column not in frame.columns
        ]

        extra = [
            column
            for column in frame.columns
            if column not in self.model_features
        ]

        if missing:
            raise ValueError(
                f"Features missing from the feature frame: {missing}"
            )

        if extra: 
            raise ValueError(
                f"Unexpected features in the feature fram: {extra}"
            )

        return frame[self.model_features]

#------------------------------------------------------------------
# Model Loading...
# 
# Kept here so the API and the 10_ file load the model the same 
# way. The API should call this once at startup, not per request.
#-------------------------------------------------------------------

def load_model():
    return joblib.load(MODEL_FILE)

def class_order(model):
    """Read class order from the model rather than assuming it."""

    return list(model.named_steps["model"].classes_)

#------------------------------------------------------------------
# Prediction Helpers
#-------------------------------------------------------------------

def predict_fixtures(model, builder, fixtures):
    """Return a list of {Home Win, Draw, Away Win} probability dicts."""

    frame = builder.build_frame(fixtures)
    probabilities = model.predict_proba(frame)
    classes = class_order(model)

    return[
        {
            label: round(float(row[classes.index(label)]), 4)
            for label in ["Home Win", "Draw", "Away Win"]
        }
        for row in probabilities
    ]
def predict_symmetric(model, builder, team_a, team_b):
    """
    Average both orderings so dropdown order does not change 
    the answer.

    In this dataset 'home team' is really just listing order, 
    and the listed home team is systematically the stronger one. 
    For a fixture that convention is meaningful. For a user picking two teams
    from dropdowns it isnt, so both orderings get averaged.  
    """

    forward, reverse = predict_fixtures(
        model, 
        builder, 
        [(team_a, team_b), (team_b, team_a)]
    )

    return{
        f"{team_a} Win": round(
            (forward["Home Win"] + reverse["Away Win"]) / 2, 4
        ),
        "Draw": round(
            (forward["Draw"] +reverse["Draw"]) / 2, 4
        ),
        f"{team_b} Win": round(
            (forward["Away Win"] +reverse["Home Win"]) / 2, 4
        ),
    }