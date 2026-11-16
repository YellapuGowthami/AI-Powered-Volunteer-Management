
import os
import random
import pandas as pd

random.seed(42)
os.makedirs("data/raw", exist_ok=True)

skills_list = [
    "Python", "Data Analysis", "Communication",
    "Teaching", "Marketing", "Project Management",
    "Web Development", "Graphic Design", "Research",
    "Event Management"
]

interests_list = [
    "Education", "Technology", "Environment",
    "Healthcare", "Community", "Animal Welfare"
]

locations = ["London", "Nottingham", "Birmingham", "Manchester"]
availability_options = ["Weekdays", "Weekends", "Evenings"]
work_modes = ["Remote", "On-site", "Hybrid"]
experience_levels = ["Beginner", "Intermediate", "Advanced"]

# 1. Generate volunteers
volunteers = []

for i in range(1, 301):
    volunteers.append({
        "volunteer_id": i,
        "skills": ", ".join(random.sample(skills_list, 3)),
        "interests": ", ".join(random.sample(interests_list, 2)),
        "experience_level": random.choice(experience_levels),
        "location": random.choice(locations),
        "availability": random.choice(availability_options),
        "preferred_work_mode": random.choice(work_modes)
    })

volunteers_df = pd.DataFrame(volunteers)
volunteers_df.to_csv("data/raw/volunteers.csv", index=False)

# 2. Generate organisations
organisations = []

for i in range(1, 51):
    organisations.append({
        "organisation_id": i,
        "organisation_name": f"Organisation_{i}",
        "sector": random.choice(interests_list),
        "location": random.choice(locations),
        "organisation_size": random.choice(["Small", "Medium", "Large"]),
        "description": f"An organisation working in {random.choice(interests_list)}"
    })

organisations_df = pd.DataFrame(organisations)
organisations_df.to_csv("data/raw/organisations.csv", index=False)

# 3. Generate opportunities
opportunities = []

for i in range(1, 151):
    opportunities.append({
        "opportunity_id": i,
        "organisation_id": random.randint(1, 50),
        "opportunity_title": f"Volunteer Opportunity {i}",
        "description": f"Support a {random.choice(interests_list)} initiative",
        "required_skills": ", ".join(random.sample(skills_list, 2)),
        "preferred_experience": random.choice(experience_levels),
        "location": random.choice(locations),
        "schedule": random.choice(availability_options),
        "work_mode": random.choice(work_modes),
        "status": random.choice(["Open", "Open", "Closed"])
    })

opportunities_df = pd.DataFrame(opportunities)
opportunities_df.to_csv("data/raw/opportunities.csv", index=False)

# 4. Generate volunteer-opportunity matching records
pairs = []

for i in range(1500):
    volunteer = random.choice(volunteers)
    opportunity = random.choice(opportunities)

    volunteer_skills = set(volunteer["skills"].split(", "))
    required_skills = set(opportunity["required_skills"].split(", "))

    skills_match = int(bool(volunteer_skills & required_skills))

    skills_match = int(bool(volunteer_skills & required_skills))

    interests_match = int(
        any(
            interest in opportunity["description"]
            for interest in volunteer["interests"].split(", ")
        )
    )

    availability_match = int(
        volunteer["availability"] == opportunity["schedule"]
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

    experience_match = int(
        experience_order[volunteer["experience_level"]]
        >= experience_order[opportunity["preferred_experience"]]
    )

    # Synthetic demonstration label; not real-world ground truth
    score = (
        0.30 * skills_match
        + 0.10 * interests_match
        + 0.15 * availability_match
        + 0.15 * location_match
        + 0.10 * work_mode_match
        + 0.20 * experience_match
    )

    suitability_label = int(score >= 0.50)

    pairs.append({
        "pair_id": i + 1,
        "volunteer_id": volunteer["volunteer_id"],
        "opportunity_id": opportunity["opportunity_id"],
        "skills_match": skills_match,
        "interests_match": interests_match,
        "availability_match": availability_match,
        "location_match": location_match,
        "work_mode_match": work_mode_match,
        "experience_match": experience_match,
        "suitability_label": suitability_label
    })

pairs_df = pd.DataFrame(pairs)
pairs_df.to_csv("data/raw/matching_labels.csv", index=False)

print("All synthetic datasets created successfully!")
print("Volunteers:", len(volunteers_df))
print("Organisations:", len(organisations_df))
print("Opportunities:", len(opportunities_df))
print("Matching records:", len(pairs_df))
print("\nDataset generation completed.")
