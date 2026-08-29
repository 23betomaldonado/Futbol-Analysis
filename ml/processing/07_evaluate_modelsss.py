#--------------------------------------------------------------------------------
#  07_evaluate_models.py
#
# Final evaluation of trained/tuned models.
#
#--------------------------------------------------------------------------------

import pandas as pd
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import(
       accuracy_score, 
       classification_report,
       confusion_matrix, 
       precision_score,
       recall_score,
       f1_score
)

#---------------------------
# File Paths
#---------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

TRAINING_FILE = PROCESSED_DATA / "training_dataset.csv"

RESULTS_FILE = PROCESSED_DATA / "final_model_evaluation.csv"

#---------------------------------------------------
# Load training dataset
#---------------------------------------------------

dataset = pd.read_csv(TRAINING_FILE)

print("\nTraining dataset loaded.")
print("Shape: ", dataset.shape)

#----------------------------------------------
# Sort dataset chronologically
#----------------------------------------------

dataset["Date"] = pd.to_datetime(dataset["Date"])

dataset = dataset.sort_values(
       "Date"
).reset_index(drop = True)

print("\nDataset sorted chronologically.")
print("Date range: ")
print(dataset["Date"].min())
print("to")
print(dataset["Date"].max())

#-----------------------------------------------------
# Separate features and target
#-----------------------------------------------------

X = dataset.drop(columns =["Date","match_result"])
y = dataset["match_result"]

#-----------------------------------------------
# Chronological train/test split
#-----------------------------------------------

split_index = int(len(dataset) * 0.80)

X_train = X.iloc[:split_index].copy()
X_test = X.iloc[split_index:].copy()

y_train = y.iloc[:split_index].copy()
y_test = y.iloc[split_index:].copy()

print("\nTraining samples: ", len(X_train))
print("\nTesting samples: ", len(X_test))

#--------------------------------------------------------------------------------
# Create tuned model pipelines
#--------------------------------------------------------------------------------

logistic_model = Pipeline([
       ("scaler", StandardScaler()),
       ("model", LogisticRegression(
              C = 1,
              max_iter = 1000
       ))
])

random_forest_model = Pipeline([
       ("model", RandomForestClassifier(
              n_estimators = 100,
              max_depth = 5,
              min_samples_split = 2,
              random_state = 42
       ))
])

#--------------------------------------------------------------------------------
# Train final tuned models
#--------------------------------------------------------------------------------

print("\nTraining final Logistic Regression…")
logistic_model.fit(X_train, y_train)

print("Training final Random Forest…")
random_forest_model.fit(X_train, y_train)

print("\nFinal models trained successfully.")

#--------------------------------------------------------------------------------
# Generate final predictions
#--------------------------------------------------------------------------------

logistic_predictions = logistic_model.predict(X_test)
random_forest_predictions = random_forest_model.predict(X_test)

print("\nFinal predictions generated successfully.")

#--------------------------------------------------------------------------------
# Calculate final accuracy
#--------------------------------------------------------------------------------

logistic_accuracy = accuracy_score(
       y_test,
       logistic_predictions
)
random_forest_accuracy = accuracy_score(
       y_test,
       random_forest_predictions
)

#----------------------------------------------------------------------------
# Calculate final precision
#----------------------------------------------------------------------------

logistic_precision = precision_score(
       y_test,
       logistic_predictions,
       average = "weighted"
)
random_forest_precision = precision_score(
       y_test,
       random_forest_predictions,
       average = "weighted"
)

#-------------------------------------------------------------------------
# Calculate final recall
#-------------------------------------------------------------------------

logistic_recall = recall_score(
       y_test,
       logistic_predictions,
       average = "weighted"
)

random_forest_recall = recall_score(
       y_test,
       random_forest_predictions,
       average = "weighted"
)

#--------------------------------------------------------------------------
# Calculate final F1 score
#--------------------------------------------------------------------------

logistic_f1 = f1_score(
       y_test, 
       logistic_predictions,
       average = "weighted"
)
random_forest_f1 = f1_score(
       y_test, 
       random_forest_predictions,
       average = "weighted"
)

#-----------------------------------------------------------------------
# Display final metrics
#-----------------------------------------------------------------------

print("\nFinal Model Evaluation: ")

print("\nLogistic Regression")
print("Accuracy: ", round(logistic_accuracy, 4))
print("Precision: ", round(logistic_precision, 4))
print("Recall: ", round(logistic_recall, 4))
print("F1 Score: ", round(logistic_f1, 4))

print("\nRandom Forest")
print("Accuracy: ", round(random_forest_accuracy, 4))
print("Precision: ", round(random_forest_precision, 4))
print("Recall: ", round(random_forest_recall, 4))
print("F1 Score: ", round(random_forest_f1, 4))

#-----------------------------------------------------------------------
# Classification reports
#-----------------------------------------------------------------------

print("\nLogistic Regression Classification Report: ")
print(
       classification_report(
              y_test, 
              logistic_predictions
       )
)

print("\nRandom Forest Classification Report: ")
print(
       classification_report(
              y_test, 
              random_forest_predictions
       )
)

#----------------------------------------------------------------
# Confusion matrices
#-----------------------------------------------------------------

print("\nLogistic Regression Confusion Matrix: ")
print(
       confusion_matrix(
              y_test, 
              logistic_predictions
       )
)

print("\nRandom Forest Confusion Matrix: ")
print(
       confusion_matrix(
              y_test, 
              random_forest_predictions
       )
)

#----------------------------------------------------------------
# Create final model evaluation table
#-----------------------------------------------------------------

final_results = pd.DataFrame({
       "Model":[
              "Logistic Regression",
              "Random Forest"
],
       "Accuracy":[
              logistic_accuracy,
              random_forest_accuracy
],
       "Recall":[
              logistic_recall,
              random_forest_recall
],
       "F1_Score":[
              logistic_f1,
              random_forest_f1
]
})

#-----------------------------------------------------------------------
# Sort models by accuracy
#-----------------------------------------------------------------------

final_results = final_results.sort_values(
       "Accuracy",
       ascending = False      
).reset_index(drop=True)

print("\nFinal Model Comparison: ")
print(final_results)

#---------------------------------------------------------------------
# Identify best final model
#----------------------------------------------------------------------

best_model = final_results.iloc[0]

print("\nBest Final Model: ")
print("Model: ",best_model["Model"])
print("Accuracy: ", round(best_model["Accuracy"], 4))
print("F1 Score: ", round(best_model["F1_Score"], 4))

#----------------------------------------------------------------------
# Save final evaluation results
#----------------------------------------------------------------------

final_results.to_csv(
       RESULTS_FILE,
       index = False
)

print("\nFinal model evaluation saved to: ")
print(RESULTS_FILE)

#---------------------------------------------------------------------
# Verify saved final results
#---------------------------------------------------------------------

verified_results = pd.read_csv(RESULTS_FILE)

print("\nVerified final model evaluation: ")
print(verified_results)

print("\nNumber of models evaluated: ")
print(len(verified_results))

print("\nBest model from saved results: ")
print(verified_results.iloc[0]["Model"])

print("\nBest model accuracy: ")
print(round(verified_results.iloc[0]["Accuracy"],4))
