#--------------------------------------------------------------------------
#
# main.py
#
# FastAPI backend for Futbol Analysis.
#
# Routes:
#   GET /                   health check
#   GET /api/teams          every team the model can predict
#   POST /api/predict       directional prediction( home vs away matters)
#   POST /api/compare       symmetric prediction (order doesnt matter)
#
# Performance Notes:
# The model and all lookup tables load ONCE at startup, not per req.
# That is the only expensive operation in this file.
#
# Per request the work is 0(1) time: a fixed 32 feature dict built 
# from hash lookups, then a fixed size matrix multiply. Adding more 
# teams does not slow down a prediction.
#
# Run with:
#   uvicorn api.main:app --reload
#------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ml.features import(
    FeatureBuilder,
    load_model,
    predict_fixtures,
    predict_symmetric,
)

#-------------------------------------------------------------------------
# App Setup
#-------------------------------------------------------------------------
app = FastAPI(
title = "Futbol Analysis API",
description = (
    "Match outcome predictions from a Logistic Regression Model"
    "trained on World Cup matches from 1930 to 2022"
    ),
    version = "1.0.0"
)

#-------------------------------------------------------------------------
# CORS
#
# The Reactfrontend runs on a different port during development, so the 
# browser blocks req. unless the API explicitly allows that origin. 
# 
# Note: Add the deployed frontend URL here once it exists. 
#-------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware, 
    allow_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

#-------------------------------------------------------------------------
# Load model once at startup
#
# This is the whole performance story. Loading inside a route handler 
# would reread and unpickle the model on every single req.
# 
#-------------------------------------------------------------------------

builder = FeatureBuilder()
model = load_model()

print("Model and feature builder loaded.")
print("Teams available: ", len(builder.known_teams))

#-------------------------------------------------------------------------
# Request bodies
#-------------------------------------------------------------------------

class PredictRequest(BaseModel):
    home_team: str
    away_team: str

class CompareRequest(BaseModel):
    team_a: str
    team_b: str

#-------------------------------------------------------------------------
# Validation Helper
#
# Set membership is O(1). known_teams is a sorted list, so it is 
# converted to a set once here rather than scanning the list on every 
# request.
# 
#-------------------------------------------------------------------------

KNOWN_TEAMS = set(builder.known_teams)

def check_team(team):
    if team not in KNOWN_TEAMS:
        raise HTTPException(
            status_code = 404,
            detail = f"Unknown team: {team}",
        )
    #Status 404 = Web server connected but couldnt find specific page/file.

#-------------------------------------------------------------------------
# Health Check
#-------------------------------------------------------------------------

@app.get("/")
def root():
    return{
        "status": "ok",
        "model":"Logistic Regression",
        "teams": len(builder.known_teams),
    }

#-------------------------------------------------------------------------
# CORS
#
# Every team with a 2026 FIFA ranking. has_history flags the teams with 
# no World Cup record, so the frontend can label them honestly. 
#-------------------------------------------------------------------------

@app.get("/api/teams")
def get_teams():
    return{
        "count": len(builder.known_teams),
        "teams": [
            {
                "name": team,
                "has_history": builder.has_history(team),
            }
            for team in builder.known_teams
        ],
    }

#-------------------------------------------------------------------------
# POST /api/predict
#
# Symmetric, same as /api/compare. 89% of World Cup matches in the 
# training data were at neutral venues, so "home team" is really just 
# listing order rather than a real home advantrage. Both ordering are 
# averaged so the order teams are passed in does not change the result.
# 
# Body:
#       {"home_team": "Brazil","away_team": "Argentina"}
#-------------------------------------------------------------------------

@app.post("/api/predict")
def predict(request: PredictRequest):
    check_team(request.home_team)
    check_team(request.away_team)

    if request.home_team == request.away_team:
        raise HTTPException(
            status_code = 400,
            detail = "A team cannot play itself!"
        )
    # Status 400 = server cant or wont process request because its a 
    # client-side error.

    probabilities = predict_symmetric(
        model,
        builder,
        request.home_team, 
        request.away_team,
    )

    predicted = max(probabilities, key = probabilities.get)

    return {
        "home_team": request.home_team,
        "away_team": request.away_team,
        "predicted_result": predicted,
        "probabilities": probabilities,
        "confidence": probabilities[predicted],
        "home_team_has_history": builder.has_history(request.home_team),
        "away_team_has_history": builder.has_history(request.away_team),
    }

#-------------------------------------------------------------------------
# POST /api/compare
#
# Symmetric. Use this for the Compare tab, where the user picks two teams 
# and the order they happened to pick them should not change the answer.
# 
# Body:
#       {"team_a": "Brazil", "team_b": "Argentina"}
#-------------------------------------------------------------------------

@app.post("/api/compare")
def compare(request: CompareRequest):
    check_team(request.team_a)
    check_team(request.team_b)

    if request.team_a == request.team_b:
        raise HTTPException(
            status_code = 400,
            detail = "A team cannot play itself!"
        )
    # Status 400 = server cant or wont process request because its a 
    # client-side error.

    probabilities = predict_symmetric(
        model,
        builder,
        request.team_a, 
        request.team_b,
    )

    predicted = max(probabilities, key = probabilities.get)

    return {
        "team_a": request.team_a,
        "team_b": request.team_b,
        "predicted_result": predicted,
        "probabilities": probabilities,
        "confidence": probabilities[predicted],
        "team_a_has_history": builder.has_history(request.team_a),
        "team_b_has_history": builder.has_history(request.team_b),
        "note": (
            "Averaged accross both ordering so the pick order doesnt"
            "affect the result"
            ),
    }
