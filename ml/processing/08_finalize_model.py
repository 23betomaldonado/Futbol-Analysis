#--------------------------------------------------------------------------------------------
# 09_finalize_model.py
#
# Finalize the best performing ML model for production use.
#
# This script:
# 1. Loads training dataset 
# 2. ID’s best model from evaluation results
# 3. Trains selected model on full dataset
# 4. Saves final production model
#--------------------------------------------------------------------------------------------

import pandas as pd
import joblib

from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

#----------------------------------------------------------------------------------------
# File paths
#----------------------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
MODEL_DATA = PROJECT_ROOT / "ml" / "models"

TRAINING_FILE = PROCESSED_DATA / "training_dataset.csv"
RESULTS_FILE = PROCESSED_DATA  / "final_model_evaluation.csv"

LOGISTIC_MODEL_FILE = MODEL_DATA / "logistic_regression_final.pkl"
RANDOM_FOREST_MODEL_FILE = MODEL_DATA / "random_forest_final.pkl"

MODEL_DATA.mkdir(parents = True, exist_ok = True)

print("\nFile paths configured successfully.")



#---------------------------------------------------------------------------------------
# Load Training dataset
#---------------------------------------------------------------------------------------

dataset = pd.read_csv(TRAINING_FILE)

print("\nTraining dataset loaded.")
print("Shape: ", dataset.shape)

#--------------------------------------------------------------------
# Sort dataset chronologically
#--------------------------------------------------------------------

dataset["Date"] = pd.to_datetime(dataset["Date"])

dataset = dataset.sort_values(
       "Date"
).reset_index(drop = True)

print("\nDataset sorted chronologically.")

#---------------------------------------------------------------------
# Separate features and target
#---------------------------------------------------------------------

X = dataset.drop(columns = ["Date", "home_team", "away_team", "match_result"])
y = dataset["match_result"]

print("\nFeature shape: ")
print(X.shape)

print("\nTarget shape: ")
print(y.shape)

#---------------------------------------------------------------------
# Load final model evaluation results
#---------------------------------------------------------------------

evaluation_results = pd.read_csv(RESULTS_FILE)

evaluation_results = evaluation_results.sort_values(
       "Accuracy",
       ascending= False
).reset_index(drop= True)

print("\nFinal model evaluation results loaded.")
print(evaluation_results)


#---------------------------------------------------------------------
# Identify best model
#---------------------------------------------------------------------
best_model_name = evaluation_results.iloc[0]["Model"]
best_accuracy = evaluation_results.iloc[0]["Accuracy"]

print("\nBest model: ")
print(best_model_name)

print("\nBest model accuracy: ")
print(round(best_accuracy, 4))

#---------------------------------------------------------------------
# Create final model
#---------------------------------------------------------------------

if best_model_name == "Logistic Regression": 
    final_model = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(
                max_iter = 1000
        ))
    ])

    model_file = LOGISTIC_MODEL_FILE

elif best_model_name == "Random Forest":
       final_model = Pipeline([
              ("model", RandomForestClassifier(
                     n_estimators = 100,
                     max_depth = 5,
                     min_samples_split =2,
                     random_state = 42
              ))
       ])

       model_file = RANDOM_FOREST_MODEL_FILE
else:
       raise ValueError(
              f"Unknown model selected: {best_model_name}"
)





#----------------------------------------------------------------------------------------
# Train final model on full dataset
#----------------------------------------------------------------------------------------
print("\nTraining final production model…")
final_model.fit(X, y)
print("\nFinal production model trained successfully.")

#----------------------------------------------------------------------------------------
# Save final model
#----------------------------------------------------------------------------------------
joblib.dump(
       final_model,
       model_file
)

print("\nFinal model saved to: ")
print(model_file)

#----------------------------------------------------------------------------------------
# Verify saved model
#----------------------------------------------------------------------------------------

loaded_model = joblib.load(model_file)

print("\nFinal model successfully loaded from disk.")

print("\nModel type:")
print(type(loaded_model))

print("\nModel verification completed successfully.")

#-------------------------------------------------------------------------
# Display of final model
#-------------------------------------------------------------------------
print("\n-----------------------------------------------------------------")
print("Final model summary")
print("-------------------------------------------------------------------")

print("Selected Model: ", best_model_name)
print("Evaluation accuracy: ", round(best_accuracy, 4))
print("Training samples: ", len(X))
print("Features: ", X.shape[1])
print("Saved Model: ", model_file)

print("-------------------------------------------------------------------")
print("Final Production Model Ready!")
print("-------------------------------------------------------------------")



#---------------------------------------------------------------
# Running Program
#---------------------------------------------------------------

# python ml/processing/09_finalize_model.py

