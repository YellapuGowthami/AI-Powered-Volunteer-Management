
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/volunteer_management.db")
DATA_PATH = Path("data/processed")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

try:
    # Import organisations first because opportunities depend on them
    organisations = pd.read_csv(DATA_PATH / "organisations.csv")

    cursor.executemany("""
        INSERT OR REPLACE INTO organisations
        VALUES (?, ?, ?, ?, ?, ?)
    """, organisations.itertuples(index=False, name=None))

    # Import volunteers
    volunteers = pd.read_csv(DATA_PATH / "volunteers.csv")

    cursor.executemany("""
        INSERT OR REPLACE INTO volunteers
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, volunteers.itertuples(index=False, name=None))

    # Import opportunities
    opportunities = pd.read_csv(DATA_PATH / "opportunities.csv")

    cursor.executemany("""
        INSERT OR REPLACE INTO opportunities
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, opportunities.itertuples(index=False, name=None))

    # Import matching records
    matches = pd.read_csv(DATA_PATH / "matching_labels.csv")

    cursor.executemany("""
        INSERT OR REPLACE INTO matching_results
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, matches.itertuples(index=False, name=None))

    connection.commit()

    print("All datasets imported successfully!")

    # Verify database records
    for table in [
        "volunteers",
        "organisations",
        "opportunities",
        "matching_results"
    ]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} records")

except Exception as error:
    connection.rollback()
    print("Database import failed:", error)

finally:
    connection.close()
