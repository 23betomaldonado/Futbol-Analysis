#--------------------------------------------------------------------------------------------------------
#08_generate_predictions.py
#
# This py file will help us use ML to predict matches if it will be a win/draw/loss
#
# This script uses the final tuned models to generate predictions that can eventually
# be used by the website
#--------------------------------------------------------------------------------------------------------

import pandas as pd
from pathlib import Path

from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

#-------------------------------------------------------------------------------------
# File paths
#-------------------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

TRAINING_FILE = PROCESSED_DATA / "training_dataset.csv"

RESULTS_FILE = PROCESSED_DATA  / "match_predictions.csv"

print("\nFile paths configured successfully.")

#--------------------------------------------------------------------
# Load training dataset
#--------------------------------------------------------------------

dataset = pd.read_csv(TRAINING_FILE)

print("\nTraining dataset loaded. ")
print("Shape: ", dataset.shape)

#--------------------------------------------------------------------
# Sort dataset chronologically
#--------------------------------------------------------------------

dataset["Date"] = pd.to_datetime(dataset["Date"])

dataset = dataset.sort_values(
       "Date"
).reset_index(drop = True)

print("\nDataset sorted chronologically.")
print("Date range: ")
print(dataset["Date"].min())
print("to")
print(dataset["Date"].max())

#---------------------------------------------------------------------
# Separate features and target
#---------------------------------------------------------------------

X = dataset.drop(columns = ["Date","match_result"])
y = dataset["match_result"]

print("\nFeature shape: ")
print(X.shape)

print("\nTarget shape: ")
print(y.shape)

#---------------------------------------------------------------------
# Chronological train/test split
#---------------------------------------------------------------------

split_index = int(len(dataset) * 0.80)

X_train = X.iloc[:split_index].copy()
X_test = X.iloc[split_index:].copy()

y_train = y.iloc[:split_index].copy()
y_test = y.iloc[split_index:].copy()

print("\nTraining samples: ", len(X_train))
print("Testing samples: ", len(X_test))

#---------------------------------------------------------------
# Create time series cross validation
#---------------------------------------------------------------

time_split = TimeSeriesSplit(n_splits = 5)

print("\nTime series cross validation configured.")
print("Number of splits: ", time_split.n_splits)

#------------------------------------------------------------
# Tune logistic Regression
#------------------------------------------------------------

logistic_pipeline = Pipeline([
       ("scaler", StandardScaler()),
       ("model", LogisticRegression(max_iter = 1000))
])

logistic_parameters = {
       "model__C" : [0.01, 0.1, 1, 10, 100]
} 

logistic_grid = GridSearchCV(
       estimator = logistic_pipeline,
       param_grid = logistic_parameters, 
       cv = time_split,
       scoring = "accuracy", 
       n_jobs = -1  
)

print("\nTuning Logistic Regression…")

logistic_grid.fit(X_train, y_train)

print("Best Logistic Regression parameters: ")
print(logistic_grid.best_params_)

print("Best Logistic Regression cross validation accuracy: ")
print(round(logistic_grid.best_score_, 4))

#--------------------------------------------------------------------------
# Tune Random Forest
#--------------------------------------------------------------------------

random_forest_pipeline = Pipeline([
       ("model", RandomForestClassifier(random_state = 42))
])

random_forest_parameters = {
       "model__n_estimators": [100,200,300],
       "model__max_depth": [None, 5, 10, 20], 
       "model__min_samples_split": [2,5,10]
}

random_forest_grid = GridSearchCV(
       estimator = random_forest_pipeline,
       param_grid = random_forest_parameters,
       cv = time_split, 
       scoring = "accuracy", 
       n_jobs = -1
)

print("\nTuning Random Forest…")

random_forest_grid.fit(X_train, y_train)

print("Best Random Forest parameters: ")
print(random_forest_grid.best_params_)

print("Best Random Forest cross validation accuracy: ")
print(round(random_forest_grid.best_score_, 4))

#------------------------------------------------------------------------
# Get best tuned models
#------------------------------------------------------------------------

logistic_model = logistic_grid.best_estimator_

random_forest_model = random_forest_grid.best_estimator_

print("\nBest tuned models selected successfully.")

#------------------------------------------------------------------------
# Generate predictions
#------------------------------------------------------------------------

logistic_predictions = logistic_model.predict(X_test)

random_forest_predictions = random_forest_model.predict(X_test)

print("\nPredictions generated successfully.")

#------------------------------------------------------------------------
# Generate prediction probabilities
#------------------------------------------------------------------------

logistic_probabilities = logistic_model.predict_proba(X_test)

random_forest_probabilities = random_forest_model.predict_proba(X_test)

print("\nPredictions probabilities generated successfully.")

#------------------------------------------------------------------------
# Get class labels
#------------------------------------------------------------------------

logistic_classes = logistic_model.named_steps["model"].classes_
random_forest_classes = random_forest_model.named_steps["model"].classes_

print("\nLogistic Regression classes: ")
print(logistic_classes)

print("\nRandom Forest classes: ")
print(random_forest_classes)

#------------------------------------------------------------------------
# Create Logistic Regression prediction results
#------------------------------------------------------------------------

logistic_results = pd.DataFrame({
       "Date": dataset["Date"].iloc[split_index:].values,
       #"Home Team": X_test["home_team"].values,
       #"Away Team": X_test["away_team"].values,
       "Actual Result": y_test.values,
       "Predicted Result": logistic_predictions,
       "Home Win Probability": logistic_probabilities[
              :, list(logistic_classes).index("Home Win")
       ],
       "Draw Probability": logistic_probabilities[
              :, list(logistic_classes).index("Draw")
       ],
       "Away Win Probability": logistic_probabilities[
              :, list(logistic_classes).index("Away Win")
       ]
})

#------------------------------------------------------------------------
# Create Random Forest prediction results
#------------------------------------------------------------------------

random_forest_results = pd.DataFrame({
       "Date": dataset["Date"].iloc[split_index:].values,
       #"Home Team": X_test["home_team"].values,
       #"Away Team": X_test["away_team"].values,
       "Actual Result": y_test.values,
       "Predicted Result": random_forest_predictions,
       "Home Win Probability": random_forest_probabilities[
              :, list(random_forest_classes).index("Home Win")
       ],
       "Draw Probability": random_forest_probabilities[
              :, list(random_forest_classes).index("Draw")
       ],
       "Away Win Probability": random_forest_probabilities[
              :, list(random_forest_classes).index("Away Win")
       ]
})

#------------------------------------------------------------------------
# Add model identifier
#------------------------------------------------------------------------

logistic_results.insert(
       0,
       "Model",
       "Logistic Regression"
)
random_forest_results.insert(
       0,
       "Model",
       "Random Forest"
)

#------------------------------------------------------------------------
# Combine model predictions
#------------------------------------------------------------------------

prediction_results = pd.concat(
       [
              logistic_results,
              random_forest_results
       ],
       ignore_index = True
)

#------------------------------------------------------------------------
# Round probability values
#------------------------------------------------------------------------

probability_columns = [
       "Home Win Probability",
       "Draw Probability",
       "Away Win Probability",
]

prediction_results[probability_columns] =(
       prediction_results[probability_columns]
       .round(4)
)

#---------------------------------------------------------------------
# Display prediction results
#---------------------------------------------------------------------

print("\nGenerated Match Predictions: ")
print(prediction_results)

#---------------------------------------------------------------------
# Display number of predictions
#---------------------------------------------------------------------

print("\nNumber of Predictions Generated: ")
print(len(prediction_results))


#---------------------------------------------------------------------
# Save prediction results
#---------------------------------------------------------------------

prediction_results.to_csv(
       RESULTS_FILE,
       index = False
)

print("\nMatch predictions saved to: ")
print(RESULTS_FILE)

#-----------------------------------------------------------------------
# Verify saved predictions results
#------------------------------------------------------------------------

verified_predictions = pd.read_csv(
       RESULTS_FILE
)

print("\nVerified prediction results: ")
print(verified_predictions)

print("\nNumber of saved predictions: ")
print(len(verified_predictions))

print("\nMissing values in saved predictions: ")
print(verified_predictions.isnull().sum().sum())

print("\nDuplicate rows in saved predictions: ")
print(verified_predictions.duplicated().sum())

#-----------------------------------------------------------------------
# Verify probability totals
#------------------------------------------------------------------------

verified_predictions["Probability Total"] = (
       verified_predictions["Home Win Probability"]
       + verified_predictions["Draw Probability"]
       + verified_predictions["Away Win Probability"]
)

print("\nProbability totals: ")
print(
verified_predictions["Probability Total"]
.round(4)
)

""""""
#
# ML TODO: 08_ works, but we commented out home team, and away team as metadata for our 
# Future website without using the ML features. Then simplified 08_ to use the finilized
# parameters from 06_ instead of rerunning GridSearchCV. current best model = Random Forest with 
# 55.96% accuracy.
#
""""""