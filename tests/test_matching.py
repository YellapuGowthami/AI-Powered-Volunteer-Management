
import sys
from pathlib import Path

import joblib
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.matching import (
    calculate_match_features,
    rank_opportunities
)


def test_matching_features():
    volunteer = {
        "skills": "Python, Data Analysis",
        "interests": "Technology, Education",
        "experience_level": "Advanced",
        "location": "London",
        "availability": "Weekends",
        "preferred_work_mode": "Remote"
    }

    opportunity = {
        "required_skills": "Python, Research",
        "description": "Support a Technology initiative",
        "preferred_experience": "Intermediate",
        "location": "London",
        "schedule": "Weekends",
        "work_mode": "Remote"
    }

    features = calculate_match_features(
        volunteer,
        opportunity
    )

    assert features == {
        "skills_match": 1,
        "interests_match": 1,
        "availability_match": 1,
        "location_match": 1,
        "work_mode_match": 1,
        "experience_match": 1
    }


def test_no_skills_match():
    volunteer = {
        "skills": "Teaching",
        "interests": "Education",
        "experience_level": "Beginner",
        "location": "London",
        "availability": "Weekends",
        "preferred_work_mode": "Remote"
    }

    opportunity = {
        "required_skills": "Python, Research",
        "description": "Support a Technology initiative",
        "preferred_experience": "Advanced",
        "location": "Manchester",
        "schedule": "Weekdays",
        "work_mode": "On-site"
    }

    features = calculate_match_features(
        volunteer,
        opportunity
    )

    assert features["skills_match"] == 0
    assert features["location_match"] == 0
    assert features["experience_match"] == 0


def test_ranked_opportunities():
    model_path = ROOT_DIR / "models" / "matching_model.pkl"
    model = joblib.load(model_path)

    volunteer = {
        "skills": "Python, Data Analysis",
        "interests": "Technology, Education",
        "experience_level": "Advanced",
        "location": "London",
        "availability": "Weekends",
        "preferred_work_mode": "Remote"
    }

    opportunities = pd.DataFrame([
        {
            "opportunity_id": 1,
            "opportunity_title": "Technology Volunteer",
            "organisation_name": "Organisation A",
            "required_skills": "Python",
            "description": "Support a Technology initiative",
            "preferred_experience": "Beginner",
            "location": "London",
            "schedule": "Weekends",
            "work_mode": "Remote"
        },
        {
            "opportunity_id": 2,
            "opportunity_title": "Community Volunteer",
            "organisation_name": "Organisation B",
            "required_skills": "Teaching",
            "description": "Support a Community initiative",
            "preferred_experience": "Advanced",
            "location": "Manchester",
            "schedule": "Weekdays",
            "work_mode": "On-site"
        }
    ])

    results = rank_opportunities(
        volunteer,
        opportunities,
        model
    )

    assert len(results) == 2
    assert results["rank"].tolist() == [1, 2]

    scores = results["estimated_score"].tolist()

    assert scores[0] >= scores[1]
