import os

dirs = [
    "data/raw", "data/processed",
    "src/data_processing", "src/models", "src/explainability", "src/intervention", "src/utils",
    "app/pages", "app/components", "app/assets", "app/styles", "app/.streamlit",
    "notebooks", "tests"
]

files = [
    "src/__init__.py", "src/config.py",
    "src/data_processing/__init__.py", "src/data_processing/cleaner.py", "src/data_processing/features.py",
    "src/models/__init__.py", "src/models/train.py", "src/models/predict.py", "src/models/evaluate.py",
    "src/explainability/__init__.py", "src/explainability/shap_explainer.py",
    "src/intervention/__init__.py", "src/intervention/recommender.py",
    "app/main.py", "app/.streamlit/config.toml",
    "app/pages/1_student_dashboard.py", "app/pages/2_faculty_dashboard.py",
    "app/components/__init__.py", "app/components/cards.py", "app/components/charts.py", "app/components/layout.py",
    "app/styles/main.css",
    "requirements.txt", "README.md", ".gitignore"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

for f in files:
    with open(f, 'w') as file:
        pass

with open("requirements.txt", "w") as req:
    req.write("pandas==2.2.0\nnumpy==1.26.3\nscikit-learn==1.4.0\nshap==0.44.1\nstreamlit==1.31.0\nplotly==5.18.0\nmatplotlib==3.8.2\n")

print("Clean slate ready. Directories, files, and requirements.txt generated.")