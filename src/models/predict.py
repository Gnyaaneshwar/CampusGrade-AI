import joblib
import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = ROOT / "src" / "models" / "saved_models"


def load_model_artifacts():
    """Load the trained model and preprocessing objects."""

    return {
        "model": joblib.load(
            MODEL_DIR / "rf_model.pkl"
        ),
        "imputer": joblib.load(
            MODEL_DIR / "imputer.pkl"
        ),
        "scaler": joblib.load(
            MODEL_DIR / "scaler.pkl"
        ),
        "encoder": joblib.load(
            MODEL_DIR / "label_encoder.pkl"
        ),
        "features": joblib.load(
            MODEL_DIR / "feature_columns.pkl"
        ),
    }


def predict_student(student_data):
    """Predict a student's grade from the six input features."""

    artifacts = load_model_artifacts()

    features = artifacts["features"]

    input_df = pd.DataFrame(
        [student_data],
        columns=features
    )

    # Apply training-time preprocessing
    input_imputed = artifacts["imputer"].transform(
        input_df
    )

    input_scaled = artifacts["scaler"].transform(
        input_imputed
    )

    model = artifacts["model"]
    encoder = artifacts["encoder"]

    # Predict grade
    prediction = model.predict(input_scaled)[0]

    predicted_grade = encoder.inverse_transform(
        [prediction]
    )[0]

    # Calculate class probabilities
    probabilities = model.predict_proba(
        input_scaled
    )[0]

    grade_probabilities = {
        str(grade): round(float(prob) * 100, 2)
        for grade, prob in zip(
            encoder.classes_,
            probabilities
        )
    }

    return {
        "predicted_grade": str(predicted_grade),
        "grade_probabilities": grade_probabilities,
        "top_class_probability": round(
            float(max(probabilities)) * 100, 2
        ),
        "warning": (
            "Model probability is not a guarantee "
            "of prediction correctness."
        ),
    }


if __name__ == "__main__":
    sample_student = {
        "previous_gpa": 7.5,
        "internal_marks": 75,
        "attendance_pct": 85,
        "assignments_completed": 8,
        "submission_delay_days": 2,
        "learning_activity_score": 70,
    }

    result = predict_student(sample_student)

    print("Predicted grade:", result["predicted_grade"])
    print("\nGrade probabilities:")

    for grade, probability in result[
        "grade_probabilities"
    ].items():
        print(f"{grade}: {probability}%")

    print("\nNote:", result["warning"])