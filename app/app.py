import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
import sqlite3


import joblib
import pandas as pd
import streamlit as st

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.matching import rank_opportunities

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "volunteer_management.db"
MODEL_PATH = BASE_DIR / "models" / "matching_model.pkl"


st.set_page_config(
    page_title="Intelligent Volunteer Matching",
    page_icon="🤝",
    layout="wide"
)


# Load trained model
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


# Load database records
@st.cache_data
def load_database_records():
    connection = sqlite3.connect(DB_PATH)

    volunteers = pd.read_sql_query(
        "SELECT * FROM volunteers ORDER BY volunteer_id",
        connection
    )

    opportunities = pd.read_sql_query(
        """
        SELECT
            o.*,
            org.organisation_name,
            org.sector
        FROM opportunities o
        LEFT JOIN organisations org
            ON o.organisation_id = org.organisation_id
        WHERE o.status = 'Open'
        ORDER BY o.opportunity_id
        """,
        connection
    )

    connection.close()

    return volunteers, opportunities


# Create a separate table for app predictions
def create_prediction_table():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS app_matching_predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            volunteer_id INTEGER NOT NULL,
            opportunity_id INTEGER NOT NULL,
            skills_match INTEGER,
            interests_match INTEGER,
            availability_match INTEGER,
            location_match INTEGER,
            work_mode_match INTEGER,
            experience_match INTEGER,
            estimated_score REAL,
            predicted_suitability INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (volunteer_id)
                REFERENCES volunteers(volunteer_id),
            FOREIGN KEY (opportunity_id)
                REFERENCES opportunities(opportunity_id)
        )
    """)

    connection.commit()
    connection.close()


def split_values(value):
    if pd.isna(value):
        return []

    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]


def save_prediction(
    volunteer_id,
    opportunity_id,
    factors,
    probability,
    prediction
):
    connection = sqlite3.connect(DB_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    connection.execute("""
        INSERT INTO app_matching_predictions (
            volunteer_id,
            opportunity_id,
            skills_match,
            interests_match,
            availability_match,
            location_match,
            work_mode_match,
            experience_match,
            estimated_score,
            predicted_suitability
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        volunteer_id,
        opportunity_id,
        factors["skills_match"],
        factors["interests_match"],
        factors["availability_match"],
        factors["location_match"],
        factors["work_mode_match"],
        factors["experience_match"],
        float(probability),
        int(prediction)
    ))

    connection.commit()
    connection.close()


# Main application
st.title("🤝 AI-Powered Intelligent Volunteer Management")

st.write(
    "An AI-based platform to connect volunteers "
    "with suitable volunteering opportunities."
)

st.info(
    "Demonstration application using synthetic data. "
    "Predictions are experimental and require human review."
)

if not DB_PATH.exists():
    st.error("Database not found. Please create the database first.")
    st.stop()

if not MODEL_PATH.exists():
    st.error("Trained model not found. Please train the model first.")
    st.stop()

try:
    model = load_model()
    volunteers, opportunities = load_database_records()
    create_prediction_table()

except Exception as error:
    st.error(f"Unable to load application data: {error}")
    st.stop()


# Database summary
st.header("Platform Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Registered Volunteers", len(volunteers))
col2.metric("Open Opportunities", len(opportunities))
col3.metric(
    "Organisations",
    opportunities["organisation_id"].nunique()
    if not opportunities.empty else 0
)

if volunteers.empty:
    st.warning("No volunteer records found in the database.")
    st.stop()

if opportunities.empty:
    st.warning("No open opportunities found in the database.")
    st.stop()


# Volunteer selection
st.header("1. Select Volunteer Profile")

volunteer_ids = volunteers["volunteer_id"].tolist()

selected_volunteer_id = st.selectbox(
    "Choose a volunteer",
    volunteer_ids,
    format_func=lambda value: (
        f"Volunteer {value} - "
        f"{volunteers.loc[
            volunteers['volunteer_id'] == value, 'location'
        ].iloc[0]}"
    )
)

volunteer = volunteers[
    volunteers["volunteer_id"] == selected_volunteer_id
].iloc[0]

with st.expander("View Volunteer Details"):
    st.write("**Skills:**", volunteer["skills"])
    st.write("**Interests:**", volunteer["interests"])
    st.write("**Experience:**", volunteer["experience_level"])
    st.write("**Location:**", volunteer["location"])
    st.write("**Availability:**", volunteer["availability"])
    st.write("**Preferred Work Mode:**", volunteer["preferred_work_mode"])


# Opportunity selection
st.header("2. Select Volunteering Opportunity")

opportunity_ids = opportunities["opportunity_id"].tolist()

selected_opportunity_id = st.selectbox(
    "Choose an opportunity",
    opportunity_ids,
    format_func=lambda value: (
        f"{opportunities.loc[
            opportunities['opportunity_id'] == value,
            'opportunity_title'
        ].iloc[0]} "
        f"(ID: {value})"
    )
)

opportunity = opportunities[
    opportunities["opportunity_id"] == selected_opportunity_id
].iloc[0]

with st.expander("View Opportunity Details"):
    st.write("**Organisation:**", opportunity["organisation_name"])
    st.write("**Sector:**", opportunity["sector"])
    st.write("**Description:**", opportunity["description"])
    st.write("**Required Skills:**", opportunity["required_skills"])
    st.write("**Preferred Experience:**", opportunity["preferred_experience"])
    st.write("**Location:**", opportunity["location"])
    st.write("**Schedule:**", opportunity["schedule"])
    st.write("**Work Mode:**", opportunity["work_mode"])


# Matching


# Ranked Volunteer Recommendations
st.header("3. AI-Powered Opportunity Recommendations")

if st.button("Find Top Recommendations", type="primary"):

    ranked_results = rank_opportunities(
        volunteer,
        opportunities,
        model
    )

    st.subheader("Ranked Opportunities")

    display_columns = [
        "rank",
        "opportunity_id",
        "opportunity_title",
        "organisation_name",
        "estimated_score"
    ]

    recommendations = ranked_results[display_columns].head(10).copy()

    recommendations["estimated_score"] = (
        recommendations["estimated_score"].round(2).astype(str) + "%"
    )

    st.dataframe(
        recommendations,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Recommendations use experimental ML scores "
        "and require human review."
    )


if st.button("Find Matching Result", type="primary"):

    volunteer_skills = set(split_values(volunteer["skills"]))
    required_skills = set(split_values(opportunity["required_skills"]))

    volunteer_interests = split_values(volunteer["interests"])
    opportunity_description = str(
        opportunity["description"]
    ).lower()

    skills_match = int(
        bool(volunteer_skills.intersection(required_skills))
    )

    interests_match = int(
        any(
            interest.lower() in opportunity_description
            for interest in volunteer_interests
        )
    )

    availability_match = int(
        volunteer["availability"] == opportunity["schedule"]
    )

    location_match = int(
        volunteer["location"] == opportunity["location"]
    )

    work_mode_match = int(
        volunteer["preferred_work_mode"] == opportunity["work_mode"]
    )

    experience_order = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3
    }

    volunteer_experience = experience_order.get(
        volunteer["experience_level"], 0
    )

    required_experience = experience_order.get(
        opportunity["preferred_experience"], 0
    )

    experience_match = int(
        volunteer_experience >= required_experience
    )

    factors = {
        "skills_match": skills_match,
        "interests_match": interests_match,
        "availability_match": availability_match,
        "location_match": location_match,
        "work_mode_match": work_mode_match,
        "experience_match": experience_match
    }

    input_data = pd.DataFrame([factors])

    probability = model.predict_proba(input_data)[0][1]
    prediction = model.predict(input_data)[0]

    st.header("3. Matching Result")

    st.metric(
        "Model-estimated suitability score",
        f"{probability * 100:.2f}%"
    )

    st.progress(float(probability))

    if prediction == 1:
        st.success(
            "The model predicts this opportunity as suitable."
        )
    else:
        st.warning(
            "The model predicts a lower suitability for this opportunity."
        )

    st.subheader("Matching Factors")

    factor_labels = {
        "skills_match": "Skills Match",
        "interests_match": "Interests Match",
        "availability_match": "Availability Match",
        "location_match": "Location Match",
        "work_mode_match": "Work Mode Match",
        "experience_match": "Experience Match"
    }

    for key, label in factor_labels.items():
        st.write(
            f"{'✅' if factors[key] else '❌'} {label}"
        )

    # Save prediction separately from synthetic training labels
    try:
        save_prediction(
            selected_volunteer_id,
            selected_opportunity_id,
            factors,
            probability,
            prediction
        )

        st.success("Matching prediction saved to the database.")

    except Exception as error:
        st.error(f"Unable to save prediction: {error}")

    st.caption(
        "This is an experimental model score, not a verified "
        "probability of volunteer success. Organisations must review "
        "applications and make final decisions."
    )
