#-------------------------------------------------------------------------------------
# 06_tune_models.py
#
# Model tuning and improved evaluation for models.
#-------------------------------------------------------------------------------------

import pandas as pd
from pathlib import Path

from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import(
       accuracy_score, 
       balanced_accuracy_score,
       f1_score,
       classification_report,
       confusion_matrix
)

#-------------------------------------------------------------------------------------
# File paths
#-------------------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

TRAINING_FILE = PROCESSED_DATA / "training_dataset.csv"

RESULTS_FILE = PROCESSED_DATA  / "tuned_model_results.csv"

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
# Chronological train/test split
#---------------------------------------------------------------------

split_index = int(len(dataset) * 0.80)

X_train = X.iloc[:split_index].copy()
X_test = X.iloc[split_index:].copy()

y_train = y.iloc[:split_index].copy()
y_test = y.iloc[split_index:].copy()

print("\nTraining samples: ", len(X_train))
print("Testing samples: ", len(X_test))

print("\nTraining data range: ")
print(dataset["Date"].iloc[:split_index].min())
print("to")
print(dataset["Date"].iloc[:split_index].max())

print("\nTesting data range: ")
print(dataset["Date"].iloc[split_index:].min())
print("to")
print(dataset["Date"].iloc[split_index:].max())


#---------------------------------------------------------------
# Create time series cross validation
#
# TimeSeriesSplit keeps the validation data later in time than the training
# data, which is appropriate for any historical match data.
#---------------------------------------------------------------

time_split = TimeSeriesSplit(n_splits = 5)

print("\nTime series cross validation: ")
print("Number of splits: ", time_split.n_splits)

#----------------------------------------------------------------
# Time Logistic Regression
#---------------------------------------------------------------

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
       scoring = "balanced_accuracy", 
       n_jobs = -1  
)

print("\nTuning Logistic Regression…")

logistic_grid.fit(X_train, y_train)

print("Best Logistic Regression parameters: ")
print(logistic_grid.best_params_)

print("Best Logistic Regression cross validation accuracy: ")
print(round(logistic_grid.best_score_, 4))

#--------------------------------------------------------------------------
# Tune Decision Tree
#--------------------------------------------------------------------------

decision_tree_pipeline = Pipeline([
    ("model", DecisionTreeClassifier(random_state= 42))
])

decision_tree_parameters = {
    "model__max_depth": [None, 3,5,10,20],
    "model__min_samples_split": [2,5,10],
    "model__min_samples_leaf": [1,2,5]
}

decision_tree_grid = GridSearchCV(
    estimator= decision_tree_pipeline,
    param_grid= decision_tree_parameters,
    cv = time_split,
    scoring = "balanced_accuracy", 
    n_jobs= -1
)

print("\nTuning Decision Tree...")

decision_tree_grid.fit(X_train,y_train)

print("Best Decision Tree parameters: ")
print(decision_tree_grid.best_params_)

print("Best Decision Tree cross validation accuracy")
print(round(decision_tree_grid.best_score_, 4))

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
       scoring = "balanced_accuracy",  
       n_jobs = -1
)

print("\nTuning Random Forest…")

random_forest_grid.fit(X_train, y_train)

print("Best Random Forest parameters: ")
print(random_forest_grid.best_params_)

print("Best Random Forest cross validation accuracy: ")
print(round(random_forest_grid.best_score_, 4))
#-----------------------------------------------------------------
# Generate predictions from tuned models
#-----------------------------------------------------------------

logistic_tuned_predictions = logistic_grid.predict(X_test)

decision_tree_tuned_predictions = decision_tree_grid.predict(X_test)

random_forest_tuned_predictions = random_forest_grid.predict(X_test)

print("\nTuned model predictions generated successfully.")

#-----------------------------------------------------------------
# Evaluate tuned models
#----------------------------------------------------------------

logistic_tuned_accuracy = accuracy_score(
       y_test,
       logistic_tuned_predictions
)

decision_tree_tuned_accuracy = accuracy_score(
       y_test,
       decision_tree_tuned_predictions
)

random_forest_tuned_accuracy = accuracy_score(
       y_test,
       random_forest_tuned_predictions
)

print("\nTuned Model Accuracy: ")

print(
       "Logistic Regression: ",
       round(logistic_tuned_accuracy, 4)
)

print(
      "Decision Tree: ",
      round(decision_tree_tuned_accuracy, 4)
)

print(
       "Random Forest: ",
       round(random_forest_tuned_accuracy, 4)
)

#---------------------------------------------
# Classification reports for tuned models
#-----------------------------------------------

print("\nTuned Logistic Regression Classification Report: ")
print(
       classification_report(
              y_test,
              logistic_tuned_predictions
       )
)

print("\nTDecision Tree Classification Report: ")
print(
       classification_report(
              y_test,
              decision_tree_tuned_predictions
       )
)


print("\nTuned Random Forest Classification Report: ")
print(
       classification_report(
              y_test,
              random_forest_tuned_predictions
       )
)

#------------------------------------------------------
# Confusion Matrices for tuned models
#------------------------------------------------------

print("\nTuned Logistic Regression Confusion Matrix: ")
print(
       confusion_matrix(
              y_test, 
              logistic_tuned_predictions
       )
)

print("\nTuned Decision Tree Confusion Matrix: ")
print(
       confusion_matrix(
              y_test, 
              decision_tree_tuned_predictions
       )
)

print("\nTuned Random Forest Confusion Matrix: ")
print(
       confusion_matrix(
              y_test, 
              random_forest_tuned_predictions
       )
)

#---------------------------------------------------------------
# Recreate baseline models for comparison
#---------------------------------------------------------------

baseline_logistic_pipeline = Pipeline([
       ("scaler", StandardScaler()),
       ("model", LogisticRegression(max_iter = 1000)),
])

baseline_decision_tree_pipeline = Pipeline([
    ("model", DecisionTreeClassifier(
        random_state= 42
    ))
])

baseline_random_forest_pipeline = Pipeline([
       ("model", RandomForestClassifier(
              n_estimators = 100,
              random_state = 42

       ))
])

print("\nTraining baseline Logistic Regression…")
baseline_logistic_pipeline.fit(X_train, y_train)

print("Training baseline Decision Tree...")
baseline_decision_tree_pipeline.fit(X_train, y_train)

print("Training baseline Random Forest…")
baseline_random_forest_pipeline.fit(X_train,y_train)

# Generate baseline predictions
logistic_predictions = baseline_logistic_pipeline.predict(X_test)
decision_tree_predictions = baseline_decision_tree_pipeline.predict(X_test)
random_forest_predictions = baseline_random_forest_pipeline.predict(X_test)
print("\nBaseline predictions generated successfully. ")

#------------------------------------------------------
# Compare baseline VS tuned models
#------------------------------------------------------

CLASS_LABELS = ["Home Win", "Draw", "Away Win"]

ALL_PREDICTIONS = [
    ("Logistic Regression - Baseline",    logistic_predictions),
    ("Logistic Regression - Tuned",       logistic_tuned_predictions),

    ("Decision Tree - Baseline",          decision_tree_predictions),
    ("Decision Tree - Tuned",          decision_tree_tuned_predictions),

    ("Random Forest - Baseline",          random_forest_predictions),
    ("Random Forest - Tuned",          random_forest_tuned_predictions),
]

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
            average= "macro"
        ),
    }

comparison_rows = []

for model_name, predictions in ALL_PREDICTIONS:
    comparison_rows.append(
        evaluate_predictions(
            model_name, 
            y_test,
            predictions
        )
    )
comparison_results = pd.DataFrame(comparison_rows)

comparison_results = comparison_results.sort_values(
    "Balanced Accuracy",
    ascending = False
).reset_index(drop= True)

print("\n" + "=" *70)
print("BASEKINE VS TUNED MODEL COMPARISON")
print("=" * 70)
print(comparison_results.round(4).to_string(index = False))
"""
comparison_results = pd.DataFrame({
       "Model" : [
              "Logistic Regression - Baseline",
              "Logistic Regression - Tuned",

              "Decision Tree - Baseline",
              "Decision Tree - Tuned",

              "Random Forest - Baseline",
              "Random Forest - Tuned"
       ],


       "Accuracy": [
              accuracy_score(y_test, logistic_predictions),
              logistic_tuned_accuracy,

              accuracy_score(y_test, decision_tree_predictions),
              decision_tree_tuned_accuracy,

              accuracy_score(y_test, random_forest_predictions),
              random_forest_tuned_accuracy
       ]
})

comparison_results = comparison_results.sort_values(
       "Accuracy",
       ascending = False
).reset_index(drop = True)

print("\nBaseline vs Tuned Model Comparison: ")
print(comparison_results)
"""

#----------------------------------------------------------------
# Identify best overall model
#----------------------------------------------------------------

best_model = comparison_results.iloc[0]

print("\nBest Overall Model: ")
print("Model: ", best_model["Model"])
print("Accuracy: ", round(best_model["Accuracy"], 4))
print("Balanced Accuracy: ", round(best_model["Balanced Accuracy"], 4))
print("Macro F1: ", round(best_model["Macro F1"], 4))

#--------------------------------------------------------
# Save tuned model results
#--------------------------------------------------------

comparison_results.to_csv(
       RESULTS_FILE,
       index = False
)

print("\nTuned model results saved to: ")
print(RESULTS_FILE)


#--------------------------------------------------------
# Verify saved tuned model results
#--------------------------------------------------------

verified_results = pd.read_csv(RESULTS_FILE)

print("\nVerified tuned model results: ")
print(verified_results)

print("\nNumber of models evaluated: ")
print(len(verified_results))

print("\nBest model from saved results: ")
print(verified_results.iloc[0]["Model"])

print("\nBest model accuracy: ")
print(round(verified_results.iloc[0]["Accuracy"], 4))
