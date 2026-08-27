#-----------------------------------------------------------------------------------
# 05_train_baseline_model.py
#
# Train and evaluate baseline ML models using the training dataset
#
# Models:
#      - Logistic Regression
#      - Decision Tree
#      - Random Forest
#
# Evaluation:
#     - Accuracy
#     - Balanced Accuracy
#     - Macro F1
#     - Classiification Report
#     - Confusion Metrix
#     - Always Home Win benchmark
#
#-----------------------------------------------------------------------------------


import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import(
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    classification_report, 
    confusion_matrix,
)

#----------------------------------------------
#file paths
#----------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

TRAINING_FILE = PROCESSED_DATA / "training_dataset.csv"

RESULTS_FILE = PROCESSED_DATA / "baseline_model_results.csv"
#----------------------------------------------
# Load training dataset
#----------------------------------------------

dataset = pd.read_csv(TRAINING_FILE)

print("Training dataset columns: ")
print(dataset.isnull().sum().sum())

print("\nTraining dataset columns: ")
print(dataset.columns.tolist())

print("\nMissing values: ")
print(dataset.isnull().sum().sum())

print("\nDuplicate rows: ")
print(dataset.duplicated().sum())

print("\nTarget distribution: ")
print(dataset["match_result"].value_counts())


#----------------------------------------------
# Separate features and target
#----------------------------------------------

X = dataset.drop(columns = ["Date","match_result"])
y = dataset["match_result"]

print("\nFeature shape: ")
print(X.shape)

print("\nTarget shape: ")
print(y.shape)

print("\nTarget percentage: ")
print(y.value_counts(normalize = True)
       .mul(100)
       .round(2)
)

#-------------------------------------------------
# Sort dataset chronologically
#-------------------------------------------------

dataset["Date"] = pd.to_datetime(dataset["Date"])
dataset = dataset.sort_values("Date").reset_index(drop = True)

#-------------------------------------------------
# Recreate features and target after sorting
#-------------------------------------------------

X = dataset.drop(columns = ["Date", "match_result"])
y = dataset["match_result"]

#-------------------------------------------------
# Chronological train/test split
#-------------------------------------------------

split_index = int(len(dataset) * 0.80)

X_train = X.iloc[: split_index].copy()
X_test = X.iloc[split_index:].copy()

y_train = y.iloc[: split_index].copy()
y_test = y.iloc[split_index:].copy()

print("\nTraining samples: ")
print(len(X_train))

print("\nTesting samples: ")
print(len(X_test))

print("\nTraining date range: ")
print(dataset["Date"].iloc[:split_index].min())
print("to")
print(dataset["Date"].iloc[:split_index].max())

print("\nTesting date range: ")
print(dataset["Date"].iloc[split_index:].min())
print("to")
print(dataset["Date"].iloc[split_index:].max())

#----------------------------------------------
# Create baseline model pipelines
#----------------------------------------------

logistic_model = Pipeline([
       ("scaler", StandardScaler()),
       ("model", LogisticRegression(max_iter = 1000))
])

decision_tree_model = Pipeline([
       ("model", DecisionTreeClassifier(random_state = 42))
])

random_forest_model = Pipeline([
       ("model", RandomForestClassifier(
              n_estimators = 100,
              random_state = 42
       ))
])

#-----------------------------------------------
# Train baseline models
#-----------------------------------------------

print("\nTraining Logistic Regression…")
logistic_model.fit(X_train, y_train)

print("Training Decision Tree…")
decision_tree_model.fit(X_train, y_train)

print("Training Random Forest…")
random_forest_model.fit(X_train, y_train)

print("\nAll baseline models trained successfully.")

#-----------------------------------------------------
# Generate predictions
#-----------------------------------------------------

logistic_predictions =logistic_model.predict(X_test)
decision_tree_predictions = decision_tree_model.predict(X_test)
random_forest_predictions = random_forest_model.predict(X_test)

print("\nPredictions generated successfully. ")

#------------------------------------------------------------------------------------
# Evaluate baseline models
#------------------------------------------------------------------------------------

import numpy as np

CLASS_LABELS = ["Home Win", "Draw", "Away Win"]

MODEL_PREDICTIONS = [
    ("Logistic Regression", logistic_predictions),
    ("Decision Tree",       decision_tree_predictions),
    ("Random Forest",       random_forest_predictions),
]

#-------------------------------------------------------------------------------------
# Always Home Win benchmark
#
# Predictions "Home Win" for every single match.
# Any model that cannot beat this is not learning anything.
#------------------------------------------------------------------------------------

always_home_win_predictions = np.full(
    len(y_test), 
    "Home Win", 
    dtype = object
)

ALL_PREDICTIONS = MODEL_PREDICTIONS + [
    ("Always Home Win", always_home_win_predictions)
]

#------------------------------------------------------------------------------------
# Calculate metrics
#------------------------------------------------------------------------------------

def evaluate_predictions(model_name, true_values, predicted_values):
    return{
        
        "Model": model_name,
        "Accuracy": accuracy_score(
              true_values,
              predicted_values
        ),
        "Balanced Accuracy": balanced_accuracy_score(
              true_values,
              predicted_values
        ),
        "Macro F1": f1_score(
              true_values,
              predicted_values,
              average = "macro"
        ),     
    }

evaluation_rows = []

for model_name, predictions in ALL_PREDICTIONS:
    evaluation_rows.append(
        evaluate_predictions(
            model_name, 
            y_test,
            predictions
        )
    )

#------------------------------------------------------------------------------------
# Classification reports
#------------------------------------------------------------------------------------
for model_name, predictions in ALL_PREDICTIONS:
    print("\n" + "=" * 70)
    print(model_name, "- Classification Report")
    print("=" * 70)
    print(
        classification_report(
            y_test, 
            predictions,
            labels= CLASS_LABELS, 
            zero_division= 0
        )
    )

#------------------------------------------------------------------------------------
# Confusion matrices
#------------------------------------------------------------------------------------
for model_name, predictions in ALL_PREDICTIONS:
    print("\n" + model_name, "- Confusion Matrix")
    print("Label order: ", CLASS_LABELS)
    print("Rows = actual, Columns = predicted")
    print(
        confusion_matrix(
            y_test,
            predictions, 
            labels= CLASS_LABELS
        )
    )

#------------------------------------------------------------------------------------
# Model comparison table
#------------------------------------------------------------------------------------
model_results = pd.DataFrame(evaluation_rows)
model_results = model_results.sort_values(
    "Balanced Accuracy",
    ascending = False
).reset_index(drop = True)

print("\n" + "=" * 70)
print("BASELINE MODELCOMPARISON")
print("=" * 70)
print(model_results.round(4).to_string(index= False))

#------------------------------------------------------------------------------------
# Benchmark Check
#------------------------------------------------------------------------------------
benchmark_row = model_results[
    model_results["Model"] == "Always Home Win"
].iloc[0]

benchmark_balanced_accuracy = benchmark_row["Balanced Accuracy"]

print("\nAlways Home Win balanced accuracy: ")
print(round(benchmark_balanced_accuracy, 4))

print("\nModels that beat the benchmark: ")

for row in evaluation_rows:
    if row["Model"] == "Always Home Win":
        continue
    if row["Balanced Accuracy"] > benchmark_balanced_accuracy:
        print(" PASS -", row["Model"])
    else: 
        print(" FAIL -", row["Model"])

#------------------------------------------------------------------------------------
# Identify best baseline model
#------------------------------------------------------------------------------------
real_models = model_results[
    model_results["Model"] != "Always Home Win"
].reset_index(drop = True)

best_model = real_models.iloc[0]

print("\nBest Baseline Model: ")
print("Model: ", best_model["Model"])
print("Accuracy: ", round(best_model["Accuracy"], 4))
print("Balanced Accuracy: ", round(best_model["Balanced Accuracy"], 4))
print("Macro F1:", round(best_model["Macro F1"], 4))

#------------------------------------------------------------------------------------
# Save baseline model results
#------------------------------------------------------------------------------------
model_results.to_csv(
    RESULTS_FILE, 
    index = False
)

print("\nBaseline model results saved to: ")
print(RESULTS_FILE)

verified_results = pd.read_csv(RESULTS_FILE)

print("\nVerified baseline results: ")
print(verified_results.round(4).to_string(index = False))

"""
#--------------------------------------------------
# Evaluate baseline models
#--------------------------------------------------

logistic_accuracy = accuracy_score(y_test, logistic_predictions)

decision_tree_accuracy = accuracy_score(
       y_test, 
       decision_tree_predictions
)

random_forest_accuracy = accuracy_score(
       y_test,
       random_forest_predictions
)
print("\nBaseline Model Accuracy: ")
print(
       "Logistic Regression: ", 
       round(logistic_accuracy, 4)
)

print(
       "Decision Tree: ", 
       round(decision_tree_accuracy, 4)
)

print(
       "Random Forest: ", 
       round(random_forest_accuracy, 4)
)

#---------------------------------------------------------
# Classification reports
#----------------------------------------------------------

print("\nLogistic Regression Classification Report: ")
print(
       classification_report(
              y_test,
              logistic_predictions
       )
)
print("\nDecision Tree Classification Report: ")
print(
       classification_report(
              y_test,
              decision_tree_predictions
       )
)

print("\nRandom Forest Classification Report: ")
print(
       classification_report(
              y_test, 
              random_forest_predictions       
       )
)

#---------------------------------------------------------------------
# Confusion matrices
#---------------------------------------------------------------------

print("\nLogistic Regression Confusion Matrix: ")
print(
       confusion_matrix(
              y_test, 
              logistic_predictions
       )
)

print("\nDecision Tree Confusion Matrix: ")
print(
       confusion_matrix(
              y_test, 
              decision_tree_predictions
       )
)

print("\nRandom Forest Confusion Matrix: ")
print(
       confusion_matrix(
              y_test, 
              random_forest_predictions
       )
)

#------------------------------------------------------------
# Compare baseline models
#------------------------------------------------------------

model_results = pd.DataFrame({
       "Model": [
              "Logistic Regression",
              "Decision Tree",
              "Random Forest"
       ],
       "Accuracy": [
              logistic_accuracy,
              decision_tree_accuracy,
              random_forest_accuracy
       ]
})
model_results = model_results.sort_values(
       "Accuracy",
       ascending = False
)

print("\nBaseline Model Comparison: ")
print(model_results)

#-----------------------------------------------------------
# Identify best baseline model
#-----------------------------------------------------------

best_model = model_results.iloc[0]

print("\nBest Baseline Model: ")
print("Model: ", best_model["Model"])
print("Accuracy: ", round(best_model["Accuracy"], 4))

#-----------------------------------------------------------
# Save baseline model results
#-----------------------------------------------------------

RESULTS_FILE =PROCESSED_DATA / "baseline_model_results.csv"

model_results.to_csv(
       RESULTS_FILE,
       index = False
)

print("\nBaseline model results saved to: ")
print(RESULTS_FILE)

#----------------------------------------------------------
# Verify saved baseline results
#-----------------------------------------------------------

verified_results =pd.read_csv(RESULTS_FILE)

print("\nVerified baseline results: ")
print(verified_results)

print("\nNumber of models evaluated: ")
print(len(verified_results))

print("\nBest model from saved results: ")
print(verified_results.iloc[0]["Model"])

print("\nBest model accuracy: ")
print(round(verified_results.iloc[0]["Accuracy"], 4))
"""