
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# File paths
DATA_PATH = Path("data/processed/matching_labels.csv")
MODEL_DIR = Path("models")
REPORT_DIR = Path("reports")

MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# Load matching dataset
df = pd.read_csv(DATA_PATH)

features = [
    "skills_match",
    "interests_match",
    "availability_match",
    "location_match",
    "work_mode_match",
    "experience_match"
]

X = df[features]
y = df["suitability_label"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Train Logistic Regression model
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)
y_probability = model.predict_proba(X_test)[:, 1]

# Evaluate model
metrics = {
    "Accuracy": accuracy_score(y_test, y_pred),
    "Precision": precision_score(y_test, y_pred, zero_division=0),
    "Recall": recall_score(y_test, y_pred, zero_division=0),
    "F1 Score": f1_score(y_test, y_pred, zero_division=0),
    "ROC-AUC": roc_auc_score(y_test, y_probability)
}

print("\nLOGISTIC REGRESSION MODEL RESULTS")
print("---------------------------------")

for name, value in metrics.items():
    print(f"{name}: {value:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Compare with a simple majority-class baseline
baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)
baseline_predictions = baseline.predict(X_test)

print(
    "\nBaseline Accuracy:",
    round(accuracy_score(y_test, baseline_predictions), 4)
)

# Cross-validation
cv_scores = cross_val_score(
    model,
    X,
    y,
    cv=5,
    scoring="f1"
)

print("\n5-Fold Cross-Validation F1 Scores:", cv_scores)
print("Mean CV F1 Score:", round(cv_scores.mean(), 4))

# Save trained model
joblib.dump(model, MODEL_DIR / "matching_model.pkl")

# Save evaluation results
with open(REPORT_DIR / "model_evaluation.txt", "w") as file:
    for name, value in metrics.items():
        file.write(f"{name}: {value:.4f}\n")

    file.write(f"\nMean CV F1 Score: {cv_scores.mean():.4f}\n")

print("\nModel saved successfully!")
print("Evaluation report saved successfully!")
