import sqlite3

connection = sqlite3.connect("data/volunteer_management.db")
cursor = connection.cursor()

tables = [
    "volunteers",
    "organisations",
    "opportunities",
    "matching_results"
]

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table}: {count} records")

connection.close()