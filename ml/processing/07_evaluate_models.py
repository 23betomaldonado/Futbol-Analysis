#-------------------------------------------------------------------------------------
# 07_evaluate_models.py
#
# Final evaluation + website artifacts
#
# 06_ showed us that tuning gave no real improvement, so this file doesnt retune.
# It uses the winning parameters from 06_ and produces what the site needs:
#
# 1. Final metrics for all three models
# 2. per match predicted probabilities
# 3. A caliberation check (are the probabilities honest?)
# 4.Feature importance
#-------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

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

#-------------------------------------------------------------------------------------
# File paths
#-------------------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

TRAINING_FILE = PROCESSED_DATA / "training_dataset.csv"

RESULT_FILE = PROCESSED_DATA / "final_model_evaluation.csv"
PROBABILITIES_FILE = PROCESSED_DATA / "test_set_probabilities.csv"
CALIBRATION_FILE = PROCESSED_DATA / "calibration_check.csv"
IMPORTANCE_FILE = PROCESSED_DATA / "feature_importance.csv"

CLASS_LABELS = ["Home Win", "Draw", "Away Win"]

#-------------------------------------------------------------------------------------
# Load and sort dataset
#-------------------------------------------------------------------------------------

dataset = pd.read_csv(TRAINING_FILE)

dataset["Date"] = pd.to_datetime(dataset["Date"])

dataset = dataset.sort_values(
    "Date"
).reset_index(drop= True)

print("\nTraining dataset loaded.")
print("Shape: ", dataset.shape)

#-------------------------------------------------------------------------------------
# Separate features and target
#-------------------------------------------------------------------------------------

X = dataset.drop(columns = ["Date", "match_result"])
y = dataset["match_result"]

feature_names = X.columns.tolist()

#-------------------------------------------------------------------------------------
# Chronological train/test split
#-------------------------------------------------------------------------------------

split_index = int(len(dataset) * 0.80)

X_train = X.iloc[:split_index].copy()
X_test = X.iloc[split_index:].copy()

y_train = y.iloc[:split_index].copy()
y_test = y.iloc[split_index:].copy()

print("\nTraining samples: ", len(X_train))
print("Testing samples: ", len(X_test))

#-------------------------------------------------------------------------------------
# Build final models
#
# Parameters below come from the GridSearchCV results in 06_.
#-------------------------------------------------------------------------------------

logistic_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(
        C = 1,
        max_iter=  1000
    ))
])

decision_tree_model = Pipeline([
    ("model", DecisionTreeClassifier(
        max_depth = 3,
        min_samples_leaf= 1,
        min_samples_split= 2,
        random_state= 42
    ))
])

random_forest_model = Pipeline([
    ("model", RandomForestClassifier(
        n_estimators= 300,
        max_depth= 20,
        min_samples_split= 2,
        random_state= 42
    ))
])

FINAL_MODELS = [
    ("Logistic Regression",    logistic_model),
    ("Decision Tree",          decision_tree_model),
    ("Random Forest",          random_forest_model),
]

#-------------------------------------------------------------------------------------
# Train 
#-------------------------------------------------------------------------------------

for model_name, model in FINAL_MODELS:
    print("\nTraining", model_name, "...")
    model.fit(X_train, y_train)

print("\nAll final models trained successfully.")

#-------------------------------------------------------------------------------------
# Evaluate
#-------------------------------------------------------------------------------------

def evaluate_predictions(model_name, true_values, predicted_values):
    return {
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
predictions_by_model = {}

for model_name, model in FINAL_MODELS:
    predictions = model.predict(X_test)
    predictions_by_model[model_name] = predictions

    evaluation_rows.append(
        evaluate_predictions(
            model_name, 
            y_test, predictions
        )
    )

    print("\n" + "=" * 70)
    print(model_name, "- Confusion Matrix")
    print("=" * 70)
    print(
        classification_report(
            y_test, 
            predictions, 
            labels = CLASS_LABELS, 
            zero_division= 0
        )
    )

    print(model_name, "- Classification Report")
    print("Label order: ", CLASS_LABELS)
    print("Rows = actual, Columns = predicted")
    print(
        confusion_matrix(
            y_test, 
            predictions, 
            labels = CLASS_LABELS, 
        )
    )

#-------------------------------------------------------------------------------------
# Final Comparison Table
#-------------------------------------------------------------------------------------

final_results = pd.DataFrame(evaluation_rows)

final_results = final_results.sort_values(
    "Balanced Accuracy", ascending= False
).reset_index(drop = True)

print("\n" + "=" * 70)
print("FINAL MODEL COMPARISON")
print("=" * 70)
print(final_results.round(4).to_string(index= False))

best_model_name = final_results.iloc[0]["Model"]

print("\nBest final model: ", best_model_name)

final_results.to_csv(
    RESULT_FILE, 
    index= False
)

print("\nFinal evaluation saved to: ")
print(RESULT_FILE)

#-------------------------------------------------------------------------------------
# Per match probabilities for the website
#
# The site should show a probability spread, not just a single label. 
# "62% Home Win / 21% Draw / 17% Away Win" is more useful and more honest than 
# just giving the users a "Home Win".
#-------------------------------------------------------------------------------------

probability_frames = []

for model_name, model in FINAL_MODELS:
    probabilities = model.predict_proba(X_test)
    model_classes = list(model.named_steps["model"].classes_)

    frame = pd.DataFrame({
        "Model": model_name,
        "Date": dataset["Date"].iloc[split_index:].values,
        "Actual Result": y_test.values,
        "Predicted Result": predictions_by_model[model_name],
    })

    for label in CLASS_LABELS:
        frame[label + " Probability"] = probabilities[
            :, model_classes.index(label)
        ].round(4)

    probability_frames.append(frame)

probability_results = pd.concat(
    probability_frames,
    ignore_index= True
)

probability_results.to_csv(
    PROBABILITIES_FILE,
    index = False
)

print("\nPer match probabilities saved to: ")
print(PROBABILITIES_FILE)
print("Rows: ", len(probability_results))

#-------------------------------------------------------------------------------------
# Calibration Check
#
# Bucket every match by its predicted Home Win probability, then check how often 
# Home Win actually happened in each bucket.
# 
#  A well calibrated model is one where matches predicted at 60% end up being home 
# wins roughly 60% of the time. This matters more than accuracy for a site that 
# displays probabilities 
#-------------------------------------------------------------------------------------

calibration_rows =[]

probability_bins = [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 1.0]

for model_name, model in FINAL_MODELS:
    model_frame = probability_results[
        probability_results["Model"] == model_name
    ].copy()

    model_frame["Bucket"] = pd.cut(
        model_frame["Home Win Probability"],
        bins = probability_bins,
        include_lowest= True
    )

    for bucket, group in model_frame.groupby("Bucket", observed = True):
        if len(group) == 0:
            continue
        calibration_rows.append({
            "Model": model_name, 
            "Predicted Range": str(bucket),
            "Matches": len(group),
            "Mean Predicted": round(
                group["Home Win Probability"].mean(), 4
            ),
            "Actual Home Win Rate": round(
                (group["Actual Result"] == "Home Win").mean(), 4
            ),
        })

calibration_results = pd.DataFrame(calibration_rows)

print("\n" + "=" * 70)
print("CALIBRATION CHECK - Home Win probability")
print("=" * 70)
print("If model is honest, 'Mean Predicted' and")
print("'Actual Home Win Rate' should be close in every row.")
print("")
print(calibration_results.to_string(index= False))

calibration_results.to_csv(
    CALIBRATION_FILE,
    index= False
)

print("\nCalibration check saved to: ")
print(CALIBRATION_FILE)

#-------------------------------------------------------------------------------------
# Feature importance
#
# Random Forest exposes feature_importance_directly.
# Logisti Regression exposes coefficients per class: the average of their
# absolute values shows which features move the prediction most. 
#-------------------------------------------------------------------------------------

random_forest_importance = pd.DataFrame({
    "Feature": feature_names,
    "Importance": random_forest_model.named_steps["model"].feature_importances_,
    "Source": "Random Forest",
})

logistic_coefficients = logistic_model.named_steps["model"].coef_

logistic_importance = pd.DataFrame({
    "Feature": feature_names,
    "Importance": np.abs(logistic_coefficients).mean(axis = 0),
    "Source": "Logistic Regression",
})

feature_importance = pd.concat(
    [random_forest_importance, logistic_importance],
    ignore_index= True
)

feature_importance["Importance"] = feature_importance["Importance"].round(4)

feature_importance = feature_importance.sort_values(
    ["Source", "Importance"],
    ascending = [True, False]
).reset_index(drop = True)

print("\n" + "=" * 70)
print("TOP 10 FEATURES - Logistic Regression")
print("=" * 70)
print(
    feature_importance[
        feature_importance["Source"] == "Logistic Regression"
    ].head(10).to_string(index = False)
)

print("\n" + "=" * 70)
print("TOP 10 FEATURES - Random Forest")
print("=" * 70)
print(
    feature_importance[
        feature_importance["Source"] == "Random Forest"
    ].head(10).to_string(index = False)
)

feature_importance.to_csv(
    IMPORTANCE_FILE,
    index = False
)

print("\nFeature importance saved to: ")
print(IMPORTANCE_FILE)

#-------------------------------------------------------------------------------------
# Summary
#-------------------------------------------------------------------------------------

print("\n" + "=" * 70)
print("07_ COMPLETE")
print("=" * 70)
print("Best model: ", best_model_name)
print("Test matches: ", len(X_test))
print("Features: ", len(feature_names))
print("\nFiles produced: ")
print(" -", RESULT_FILE.name)
print(" -", PROBABILITIES_FILE.name)
print(" -", CALIBRATION_FILE.name)
print(" -", IMPORTANCE_FILE.name)
print("=" *70)