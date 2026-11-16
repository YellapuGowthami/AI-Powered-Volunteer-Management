
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

files = [
    "volunteers.csv",
    "organisations.csv",
    "opportunities.csv",
    "matching_labels.csv"
]

for file in files:
    path = DATA_DIR / file
    df = pd.read_csv(path)

    print(f"\n--- {file} ---")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Missing values:", df.isnull().sum().sum())
    print("Duplicate rows:", df.duplicated().sum())

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Save cleaned version
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_dir / file, index=False)

    print("Cleaned file saved successfully!")
    
print("\nData validation completed!")
