
import sqlite3
from pathlib import Path

# Database location
DB_PATH = Path("data/volunteer_management.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Volunteer profiles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            volunteer_id INTEGER PRIMARY KEY,
            skills TEXT,
            interests TEXT,
            experience_level TEXT,
            location TEXT,
            availability TEXT,
            preferred_work_mode TEXT
        )
    """)

    # Organisation profiles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS organisations (
            organisation_id INTEGER PRIMARY KEY,
            organisation_name TEXT,
            sector TEXT,
            location TEXT,
            organisation_size TEXT,
            description TEXT
        )
    """)

    # Volunteering opportunities
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            opportunity_id INTEGER PRIMARY KEY,
            organisation_id INTEGER,
            opportunity_title TEXT,
            description TEXT,
            required_skills TEXT,
            preferred_experience TEXT,
            location TEXT,
            schedule TEXT,
            work_mode TEXT,
            status TEXT,
            FOREIGN KEY (organisation_id)
                REFERENCES organisations(organisation_id)
        )
    """)

    # Matching records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matching_results (
            pair_id INTEGER PRIMARY KEY,
            volunteer_id INTEGER,
            opportunity_id INTEGER,
            skills_match INTEGER,
            interests_match INTEGER,
            availability_match INTEGER,
            location_match INTEGER,
            work_mode_match INTEGER,
            experience_match INTEGER,
            suitability_label INTEGER,
            FOREIGN KEY (volunteer_id)
                REFERENCES volunteers(volunteer_id),
            FOREIGN KEY (opportunity_id)
                REFERENCES opportunities(opportunity_id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database and tables created successfully!")


if __name__ == "__main__":
    create_tables()
