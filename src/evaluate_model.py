
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay

df = pd.read_csv("data/processed/matching_labels.csv")

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

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

model = joblib.load("models/matching_model.pkl")

ConfusionMatrixDisplay.from_estimator(
    model, X_test, y_test
)

plt.title("Volunteer Matching - Confusion Matrix")
plt.tight_layout()
plt.savefig("reports/confusion_matrix.png")
plt.show()

print("Confusion matrix saved successfully!")
