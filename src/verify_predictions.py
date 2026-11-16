
import sqlite3

connection = sqlite3.connect("data/volunteer_management.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT COUNT(*)
    FROM app_matching_predictions
""")

count = cursor.fetchone()[0]

print(f"Saved app predictions: {count}")

cursor.execute("""
    SELECT
        volunteer_id,
        opportunity_id,
        estimated_score,
        predicted_suitability
    FROM app_matching_predictions
    ORDER BY prediction_id DESC
    LIMIT 1
""")

result = cursor.fetchone()

print("Latest prediction:", result)

connection.close()
