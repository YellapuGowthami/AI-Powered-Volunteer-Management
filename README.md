
# AI-Powered Intelligent Volunteer Management & Matching Platform

## Project Overview

An AI-powered volunteer management and matching platform designed to help organisations identify suitable volunteers for volunteering opportunities.

The platform combines data processing, machine learning and software engineering to provide ranked opportunity recommendations based on volunteer profiles and opportunity requirements.

This project is developed as a demonstration prototype using synthetic datasets.

## Key Features

- Volunteer profile management
- Organisation and volunteering opportunity data management
- Data cleaning and preprocessing
- Machine learning-based suitability prediction
- Ranked volunteer-opportunity recommendations
- SQLite database integration
- Interactive Streamlit application
- Automated testing using Pytest
- Responsible AI considerations

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, Logistic Regression |
| Data Visualisation | Matplotlib |
| Database | SQLite, SQL |
| Application | Streamlit |
| Testing | Pytest |
| Model Storage | Joblib |
| Version Control | Git, GitHub |

## Machine Learning Approach

The platform uses Logistic Regression to estimate volunteer-opportunity suitability.

The model considers six matching features:

1. Skills match
2. Interests match
3. Availability match
4. Location match
5. Work mode match
6. Experience match

The model produces suitability scores that are used to rank volunteering opportunities.

## Dataset Information

The prototype uses four synthetic datasets:

| Dataset | Records |
|---|---:|
| Volunteers | 300 |
| Organisations | 50 |
| Opportunities | 150 |
| Matching records | 1,500 |

The matching labels are synthetic and rule-derived. They do not represent verified real-world volunteer outcomes.

## Application Workflow

1. Load volunteer and opportunity data from SQLite.
2. Select a volunteer profile.
3. Retrieve available volunteering opportunities.
4. Calculate matching features.
5. Generate model-based suitability scores.
6. Rank opportunities by estimated score.
7. Display recommendations through Streamlit.

## Model Evaluation

The model is evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix
- Cross-validation
- Baseline comparison

Evaluation results must be interpreted in the context of synthetic training data and labels.

## Testing

Automated tests are implemented using Pytest.

Current test results:

**9 tests passed successfully.**

Run tests using:

```bash
python -m pytest -v
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YellapuGowthami/AI_Volunteer_Management.git
cd AI_Volunteer_Management
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Generate datasets

```bash
python src/generate_data.py
```

### 6. Clean datasets

```bash
python src/clean_data.py
```

### 7. Train the machine learning model

```bash
python src/train_model.py
```

### 8. Create the database

```bash
python src/database.py
```

### 9. Import datasets into SQLite

```bash
python src/import_data.py
```

### 10. Launch the application

```bash
python -m streamlit run app/app.py
```

## Responsible AI

This prototype incorporates considerations relating to:

- Data privacy
- Fairness and potential bias
- Transparency
- Model limitations
- Human oversight

See [Responsible AI Documentation](reports/responsible_ai.md).

## Limitations

- The datasets are synthetic.
- Matching labels are rule-derived.
- Real-world model performance has not been established.
- Predictions are experimental suitability estimates, not verified probabilities of volunteer success.
- Human review is required before any volunteer selection decision.

## Future Improvements

- Evaluation using representative real-world data
- Fairness and subgroup performance assessment
- Improved volunteer and organisation workflows
- User feedback and recommendation monitoring
- Enhanced accessibility and usability

## Author

**Yellapu Gowthami**

GitHub: https://github.com/YellapuGowthami

LinkedIn: https://linkedin.com/in/yellapu-gowthami

---

This project is an independent demonstration prototype developed to explore applied machine learning, data engineering and software engineering in volunteer management.

