
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

# Load datasets
volunteers = pd.read_csv(DATA_DIR / "volunteers.csv")
organisations = pd.read_csv(DATA_DIR / "organisations.csv")
opportunities = pd.read_csv(DATA_DIR / "opportunities.csv")
matches = pd.read_csv(DATA_DIR / "matching_labels.csv")

# 1. Volunteer experience distribution
volunteers["experience_level"].value_counts().plot(kind="bar")
plt.title("Volunteer Experience Distribution")
plt.xlabel("Experience Level")
plt.ylabel("Number of Volunteers")
plt.tight_layout()
plt.savefig(REPORT_DIR / "volunteer_experience.png")
plt.close()

# 2. Opportunity location distribution
opportunities["location"].value_counts().plot(kind="bar")
plt.title("Opportunity Location Distribution")
plt.xlabel("Location")
plt.ylabel("Number of Opportunities")
plt.tight_layout()
plt.savefig(REPORT_DIR / "opportunity_locations.png")
plt.close()

# 3. Matching label distribution
matches["suitability_label"].value_counts().sort_index().plot(kind="bar")
plt.title("Volunteer Matching Suitability Distribution")
plt.xlabel("Suitability Label (0 = Not Suitable, 1 = Suitable)")
plt.ylabel("Number of Matches")
plt.tight_layout()
plt.savefig(REPORT_DIR / "matching_distribution.png")
plt.close()

print("DATASET SUMMARY")
print("-------------------------")
print("Volunteers:", len(volunteers))
print("Organisations:", len(organisations))
print("Opportunities:", len(opportunities))
print("Matching records:", len(matches))

print("\nMatching label counts:")
print(matches["suitability_label"].value_counts())

print("\nEDA completed! Charts saved in reports folder.")
