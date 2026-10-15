import os
import json
import joblib
import pandas as pd

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    RandomizedSearchCV
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Project paths
ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = ROOT / "data" / "raw" / "synthetic_student_data.csv"

MODEL_DIR = ROOT / "src" / "models" / "saved_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42

FEATURES = [
    "previous_gpa",
    "internal_marks",
    "attendance_pct",
    "assignments_completed",
    "submission_delay_days",
    "learning_activity_score",
]

TARGET = "final_grade"


def train_model():
    # 1. Load and validate dataset
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH).drop_duplicates()

    required = FEATURES + [TARGET]
    missing = set(required) - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    df = df.dropna(subset=[TARGET])

    X = df[FEATURES].apply(
        pd.to_numeric, errors="raise"
    )
    y_text = df[TARGET].astype(str)

    # 2. Encode grade labels
    encoder = LabelEncoder()
    y = encoder.fit_transform(y_text)

    # 3. Keep test data separate from tuning
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # 4. Build preprocessing and model pipeline
    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        (
            "model",
            RandomForestClassifier(
                random_state=RANDOM_STATE,
                class_weight="balanced",
                n_jobs=-1
            )
        )
    ])

    # 5. Hyperparameter search
    parameters = {
        "model__n_estimators": [100, 200, 300],
        "model__max_depth": [None, 6, 10, 15, 20],
        "model__min_samples_split": [2, 4, 6, 10],
        "model__min_samples_leaf": [1, 2, 3, 5],
        "model__max_features": ["sqrt", 0.7, 1.0],
    }

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=parameters,
        n_iter=12,
        scoring="f1_macro",
        cv=cv,
        random_state=RANDOM_STATE,
        n_jobs=1,
        refit=True,
        verbose=1
    )

    print("Training and tuning Random Forest...")
    search.fit(X_train, y_train)

    # 6. Extract fitted preprocessing and model
    best_pipeline = search.best_estimator_

    imputer = best_pipeline.named_steps["imputer"]
    scaler = best_pipeline.named_steps["scaler"]
    model = best_pipeline.named_steps["model"]

    # 7. Save artifacts
    joblib.dump(model, MODEL_DIR / "rf_model.pkl")
    joblib.dump(imputer, MODEL_DIR / "imputer.pkl")
    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
    joblib.dump(encoder, MODEL_DIR / "label_encoder.pkl")
    joblib.dump(FEATURES, MODEL_DIR / "feature_columns.pkl")

    # 8. Save the untouched test set for evaluation
    test_df = X_test.copy()
    test_df[TARGET] = encoder.inverse_transform(y_test)

    test_df.to_csv(
        MODEL_DIR / "holdout_test.csv",
        index=False
    )

    # 9. Save training metadata
    metadata = {
        "best_cv_macro_f1": float(search.best_score_),
        "best_parameters": search.best_params_,
        "classes": encoder.classes_.tolist(),
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "random_state": RANDOM_STATE
    }

    with open(
        MODEL_DIR / "training_metadata.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(metadata, file, indent=4)

    print("\nTraining completed.")
    print("Best CV Macro F1:", round(search.best_score_, 4))
    print("Best parameters:", search.best_params_)
    print("Saved model files to:", MODEL_DIR)
    print("\nNext: run python src/models/evaluate.py")


if __name__ == "__main__":
    train_model()