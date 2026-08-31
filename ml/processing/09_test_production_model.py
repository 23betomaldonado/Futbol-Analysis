#--------------------------------------------------------------------------------
#
# 09_test_production_model.py
#
# Test the final production model.
#
# 1. Loads saved production model
# 2. Leads training dataset
# 3. Creates test feature set
# 4.Generates predictions & probabilities
# 5. Verifies production model works properly
#--------------------------------------------------------------------------------
import pandas as pd
import joblib

from pathlib import Path

#--------------------------------------------------------------------------------
# File paths
#-------------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
MODEL_DATA = PROJECT_ROOT / "ml" / "models"

TRAINING_FILE = PROCESSED_DATA / "training_dataset.csv"

LOGISTIC_MODEL_FILE = MODEL_DATA / "logistic_regression_final.pkl"
DECISION_TREE_MODEL_FILE = MODEL_DATA / "decision_tree_final.pkl"
RANDOM_FOREST_MODEL_FILE = MODEL_DATA / "random_forest_final.pkl"

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

X = dataset.drop(columns = ["Date","home_team","away_team", "match_result"])
y = dataset["match_result"]

print("\nFeature shape: ")
print(X.shape)

print("\nTarget shape: ")
print(y.shape)

#---------------------------------------------------------------------
# Load final production models
#---------------------------------------------------------------------

logistic_model = None
random_forest_model = None

if LOGISTIC_MODEL_FILE.exists():
       logistic_model = joblib.load(
              LOGISTIC_MODEL_FILE
       )

       print("\nLogistics Regression model loaded successfully!")

if RANDOM_FOREST_MODEL_FILE.exists():
       random_forest_model = joblib.load(
              RANDOM_FOREST_MODEL_FILE
       )

       print("\nRandom Forest model loaded successfully!")

#--------------------------------------------------------------------------
# Verify that atleast one model exists
#--------------------------------------------------------------------------

if logistic_model is None and random_forest_model is None:
       raise FileNotFoundError(
              "No final production model was found."
       )

#--------------------------------------------------------------------------
# Create test dataset
#--------------------------------------------------------------------------

test_size = min(10, len(X))

X_test = X.tail(test_size).copy()
y_test = y.tail(test_size).copy()

print("\nProduction test samples: ")
print(len(X_test))

#--------------------------------------------------------------------------
# Test Logistic Regression
#--------------------------------------------------------------------------

if logistic_model is not None: 

    print("\nTesting Logistic Regression…")

    logistic_predictions = logistic_model.predict(
        X_test
    )

    logistic_probabilities = logistic_model.predict_proba(
        X_test
    )

    print("\nLogistic Regression Predictions: ")
    print(logistic_predictions)
    print("\nLogistic Regression Probabilities: ")
    print(logistic_probabilities)
    print("\nLogistic Regression Classes: ")
    print(logistic_model.classes_)

#--------------------------------------------------------------------------
# Test Random Forest
#--------------------------------------------------------------------------

if random_forest_model is not None: 

    print("\nTesting Random Forest…")

    random_forest_predictions = random_forest_model.predict(
        X_test
    )

    random_forest_probabilities = random_forest_model.predict_proba(
        X_test
    )

    print("\nRandom Forest Predictions: ")
    print(random_forest_predictions)

    print("\nRandom Forest Probabilities: ")
    print(random_forest_probabilities)

    print("\nRandom Forest Classes: ")
    print(random_forest_model.classes_)

#--------------------------------------------------------------------------
# Verify probability totals
#--------------------------------------------------------------------------

if logistic_model is not None:
       logistic_probability_totals = (
              logistic_probabilities.sum(axis = 1)
       )

       print("\nLogistic Regression probability totals: ")
       print(
              logistic_probability_totals.round(4)
       )
if random_forest_model is not None:
       random_forest_probability_totals = (
              random_forest_probabilities.sum(axis = 1)
       )

       print("\nRandom Forest probability totals: ")
       print(
              random_forest_probability_totals.round(4)
       )


#-------------------------------------------------------------------
# Final verification
#-------------------------------------------------------------------

print("\n—----------------------------------------------------------")
print("PRODUCTION MODEL TEST")
print("----------------------------------------------------------------")

print("Test samples: ", len(X_test))
print("Features: ",X_test.shape[1])

if logistic_model is not None:
       print("Logistic Regression: PASS")

if random_forest_model is not None:
       print("Random Forest: PASS")

print("----------------------------------------------------------")
print("Prediction model test completed successfully!")
print("-----------------------------------------------------------")



