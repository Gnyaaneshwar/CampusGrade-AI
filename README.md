# 🎓 CampusGrade AI — Intelligent Academic Intervention System

An AI-powered academic analytics platform that predicts student performance, identifies academic risk, and provides explainable insights to support timely academic intervention.

🔗 **Live Demo:** [CampusGrade AI](https://campusgrade-ai-c3skgkb6luj5plee2qweff.streamlit.app/)

💻 **GitHub Repository:** [Gnyaaneshwar/CampusGrade-AI](https://github.com/Gnyaaneshwar/CampusGrade-AI)

---

## 📌 Overview

CampusGrade AI is a machine learning-based academic analytics system designed to help students understand their academic performance and help faculty identify students who may need additional support.

The platform combines grade prediction, academic risk analysis, interactive dashboards, and Explainable AI (XAI) to make model predictions easier to understand and act upon.

The system includes separate student and faculty dashboards, offering personalized academic insights and cohort-level performance analysis.

## ✨ Key Features

### 🎯 Student Dashboard
- Interactive academic performance analysis.
- What-If Simulator to explore how changes in academic inputs may affect predictions.
- Grade prediction and predicted class probabilities.
- Academic risk identification.
- SHAP-based explanations of important prediction factors.
- Personalized action roadmap and academic recommendations.

### 👨‍🏫 Faculty Dashboard
- Cohort-level academic performance overview.
- Student enrollment and average GPA metrics.
- Identification of potentially at-risk students.
- Projected grade distribution visualization.
- Priority-based at-risk student analysis.

### 🤖 Machine Learning
- Random Forest-based grade prediction.
- Data preprocessing and feature engineering.
- Model training and evaluation workflow.
- Saved model artifacts for prediction.
- SHAP-based model explainability.

### 📊 Interactive Visualizations
- Academic performance metrics.
- Grade distribution charts.
- Risk indicators and summary cards.
- Student-level and cohort-level insights.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computing |
| Scikit-learn | Machine learning and preprocessing |
| SHAP | Explainable AI |
| Plotly | Interactive visualizations |
| Matplotlib | Data visualization |
| Git & GitHub | Version control and source code management |
| Streamlit Community Cloud | Application deployment |

## ⚙️ System Workflow

1. **Data Input:** Load academic data containing relevant student performance indicators.
2. **Data Preprocessing:** Clean data and prepare features for model inference.
3. **Feature Engineering:** Transform academic attributes into model-ready inputs.
4. **Model Prediction:** Use the trained machine learning model to predict academic outcomes.
5. **Risk Analysis:** Interpret predicted outcomes to identify students who may require attention.
6. **Explainable AI:** Use SHAP to understand which features contribute to model predictions.
7. **Academic Intervention:** Present insights and recommended actions through student and faculty dashboards.

## 🧠 Explainable AI with SHAP

CampusGrade AI incorporates SHAP (SHapley Additive exPlanations) to help interpret machine learning predictions.

Instead of presenting only a predicted grade, the platform can explain how input features influence a prediction.

This supports more transparent academic analysis and helps users understand the factors associated with predicted outcomes.

**Important:** Model explanations describe the model's behavior; they do not establish that a particular academic factor causes a student's performance.

## 📂 Project Structure

```text
CampusGrade-AI/
│
├── app/
│   ├── main.py
│   ├── components/
│   │   ├── cards.py
│   │   ├── charts.py
│   │   └── layouts.py
│   ├── pages/
│   │   ├── 1_student_dashboard.py
│   │   └── 2_faculty_dashboard.py
│   └── styles/
│       └── main.css
│
├── data/
│   └── raw/
│       └── synthetic_student_data.csv
│
├── src/
│   ├── config.py
│   ├── data_processing/
│   │   ├── cleaner.py
│   │   └── features.py
│   ├── explainability/
│   │   └── shap_explainer.py
│   ├── intervention/
│   │   └── recommender.py
│   └── models/
│       ├── train.py
│       ├── evaluate.py
│       ├── predict.py
│       └── saved_models/
│
├── tests/
├── notebooks/
├── .streamlit/
├── generate_mock_data.py
├── setup_project.py
├── requirements.txt
└── README.md
```

## 🚀 Run Locally

### Prerequisites

- Python 3.10 or a compatible Python version supported by the installed dependencies.
- Git.
- pip package manager.

### 1. Clone the repository

```bash
git clone https://github.com/Gnyaaneshwar/CampusGrade-AI.git
cd CampusGrade-AI
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the application

```bash
streamlit run app/main.py
```

The application should open in your browser at the local URL provided by Streamlit, usually `http://localhost:8501`.

**Note:** The application requires its expected model artifacts and data files. If running from a fresh clone, verify that all required artifacts are present and that the model paths are configured correctly.

## 📈 Model Development

The repository contains scripts for the machine learning workflow:

- `src/models/train.py` — model training.
- `src/models/evaluate.py` — model evaluation.
- `src/models/predict.py` — prediction logic.
- `src/data_processing/cleaner.py` — data cleaning.
- `src/data_processing/features.py` — feature preparation.
- `src/explainability/shap_explainer.py` — model explanation.
- `src/intervention/recommender.py` — academic intervention recommendations.

The project includes saved model artifacts for inference. Actual model quality should be assessed using appropriate held-out data and evaluation metrics before deploying predictions for real academic decisions.

## 🖥️ Live Application

Try the deployed application:

**[Launch CampusGrade AI →](https://campusgrade-ai-c3skgkb6luj5plee2qweff.streamlit.app/)**

The application is hosted using Streamlit Community Cloud.

## 🔮 Future Enhancements

- Integrate verified institutional academic data with appropriate authorization.
- Improve model evaluation and prediction reliability.
- Add historical performance tracking and progress visualization.
- Provide more detailed, personalized intervention recommendations.
- Introduce faculty reporting and downloadable academic summaries.
- Evaluate model fairness and performance across relevant student groups.
- Add authentication and role-based access control where required.
- Monitor model performance and data quality over time.

## 🔒 Data Privacy and Responsible AI

CampusGrade AI is intended to support academic decision-making, not replace faculty judgment.

- Use synthetic or properly authorized and anonymized data for demonstrations.
- Protect student information and restrict access to sensitive records.
- Treat predictions as estimates rather than guaranteed academic outcomes.
- Validate model performance and potential bias before real-world use.
- Ensure that high-impact academic decisions involve appropriate human review.

## 👨‍💻 Author

**Gnyaaneshwar S**

B.Tech — Computer Science and Engineering (Data Science)

**Project:** CampusGrade AI — Intelligent Academic Intervention System

- GitHub: [@Gnyaaneshwar](https://github.com/Gnyaaneshwar)
- Live Demo: [CampusGrade AI](https://campusgrade-ai-c3skgkb6luj5plee2qweff.streamlit.app/)

---

⭐ If you find this project interesting, consider starring the repository!

*Built with Python, Machine Learning, Explainable AI, and Streamlit.*