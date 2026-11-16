
import sqlite3
from pathlib import Path

import joblib
import pandas as pd
import pytest


ROOT_DIR = Path(__file__).resolve().parents[1]

DB_PATH = ROOT_DIR / "data" / "volunteer_management.db"
MODEL_PATH = ROOT_DIR / "models" / "matching_model.pkl"


def test_database_exists():
    assert DB_PATH.exists()


def test_database_record_counts():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    expected_counts = {
        "volunteers": 300,
        "organisations": 50,
        "opportunities": 150,
        "matching_results": 1500
    }

    for table, expected in expected_counts.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        actual = cursor.fetchone()[0]
        assert actual == expected

    connection.close()


def test_prediction_table_exists():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'app_matching_predictions'
    """)

    result = cursor.fetchone()

    connection.close()

    assert result is not None


def test_foreign_key_integrity():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_key_check")

    errors = cursor.fetchall()

    connection.close()

    assert errors == []


def test_model_exists():
    assert MODEL_PATH.exists()


def test_model_prediction():
    model = joblib.load(MODEL_PATH)

    features = pd.DataFrame([{
        "skills_match": 1,
        "interests_match": 1,
        "availability_match": 1,
        "location_match": 1,
        "work_mode_match": 1,
        "experience_match": 1
    }])

    probabilities = model.predict_proba(features)

    assert probabilities.shape == (1, 2)
    assert 0 <= probabilities[0][1] <= 1
    assert probabilities.sum() == pytest.approx(1.0)
