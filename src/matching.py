
import pandas as pd


EXPERIENCE_ORDER = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3
}


def split_values(value):
    if pd.isna(value):
        return []

    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]


def calculate_match_features(volunteer, opportunity):

    volunteer_skills = set(split_values(volunteer["skills"]))
    required_skills = set(split_values(opportunity["required_skills"]))

    volunteer_interests = split_values(volunteer["interests"])

    description = str(opportunity["description"]).lower()

    skills_match = int(
        bool(volunteer_skills.intersection(required_skills))
    )

    interests_match = int(
        any(
            interest.lower() in description
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

    volunteer_experience = EXPERIENCE_ORDER.get(
        volunteer["experience_level"], 0
    )

    required_experience = EXPERIENCE_ORDER.get(
        opportunity["preferred_experience"], 0
    )

    experience_match = int(
        volunteer_experience >= required_experience
    )

    return {
        "skills_match": skills_match,
        "interests_match": interests_match,
        "availability_match": availability_match,
        "location_match": location_match,
        "work_mode_match": work_mode_match,
        "experience_match": experience_match
    }


def rank_opportunities(volunteer, opportunities, model):

    if opportunities.empty:
        return opportunities.copy()

    results = opportunities.copy()

    features = pd.DataFrame([
        calculate_match_features(volunteer, opportunity)
        for _, opportunity in results.iterrows()
    ])

    results["estimated_score"] = (
        model.predict_proba(features)[:, 1] * 100
    )

    results["predicted_suitability"] = model.predict(features)

    results = results.sort_values(
        by="estimated_score",
        ascending=False
    ).reset_index(drop=True)

    results.insert(
        0,
        "rank",
        range(1, len(results) + 1)
    )

    return results
