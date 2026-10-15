import json
import joblib
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    log_loss,
)

ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = ROOT / "src" / "models" / "saved_models"
TARGET = "final_grade"


def evaluate_model():
    # 1. Load trained artifacts
    model_path = MODEL_DIR / "rf_model.pkl"
    imputer_path = MODEL_DIR / "imputer.pkl"
    scaler_path = MODEL_DIR / "scaler.pkl"
    encoder_path = MODEL_DIR / "label_encoder.pkl"
    features_path = MODEL_DIR / "feature_columns.pkl"
    test_path = MODEL_DIR / "holdout_test.csv"

    required_files = [
        model_path,
        imputer_path,
        scaler_path,
        encoder_path,
        features_path,
        test_path,
    ]

    for path in required_files:
        if not path.exists():
            raise FileNotFoundError(
                f"{path.name} not found. Run train.py first."
            )

    model = joblib.load(model_path)
    imputer = joblib.load(imputer_path)
    scaler = joblib.load(scaler_path)
    encoder = joblib.load(encoder_path)
    features = joblib.load(features_path)

    # 2. Load untouched test data
    df = pd.read_csv(test_path)

    X_test = df[features]
    y_test = encoder.transform(
        df[TARGET].astype(str)
    )

    # 3. Apply the same preprocessing as training
    X_imputed = imputer.transform(X_test)
    X_scaled = scaler.transform(X_imputed)

    # 4. Predict grades
    y_pred = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)

    # 5. Calculate evaluation metrics
    metrics = {
        "test_samples": int(len(y_test)),
        "accuracy": float(
            accuracy_score(y_test, y_pred)
        ),
        "precision_macro": float(
            precision_score(
                y_test, y_pred,
                average="macro",
                zero_division=0
            )
        ),
        "recall_macro": float(
            recall_score(
                y_test, y_pred,
                average="macro",
                zero_division=0
            )
        ),
        "f1_macro": float(
            f1_score(
                y_test, y_pred,
                average="macro",
                zero_division=0
            )
        ),
        "precision_weighted": float(
            precision_score(
                y_test, y_pred,
                average="weighted",
                zero_division=0
            )
        ),
        "recall_weighted": float(
            recall_score(
                y_test, y_pred,
                average="weighted",
                zero_division=0
            )
        ),
        "f1_weighted": float(
            f1_score(
                y_test, y_pred,
                average="weighted",
                zero_division=0
            )
        ),
        "log_loss": float(
            log_loss(
                y_test,
                probabilities,
                labels=list(range(len(encoder.classes_)))
            )
        ),
    }

    # 6. Per-grade classification report
    report = classification_report(
        y_test,
        y_pred,
        labels=list(range(len(encoder.classes_))),
        target_names=encoder.classes_,
        zero_division=0
    )

    print("\n========== MODEL EVALUATION ==========")

    for name, value in metrics.items():
        if isinstance(value, float):
            print(f"{name}: {value:.4f}")
        else:
            print(f"{name}: {value}")

    print("\n========== PER-GRADE REPORT ==========")
    print(report)

    # 7. Save evaluation metrics
    with open(
        MODEL_DIR / "evaluation_metrics.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(metrics, file, indent=4)

    with open(
        MODEL_DIR / "classification_report.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(report)

    # 8. Generate confusion matrix
    cm = confusion_matrix(
        y_test,
        y_pred,
        labels=list(range(len(encoder.classes_)))
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=encoder.classes_
    )

    fig, ax = plt.subplots(figsize=(8, 6))
    display.plot(
        ax=ax,
        cmap="Blues",
        values_format="d",
        colorbar=False
    )

    ax.set_title("CampusGrade AI - Confusion Matrix")
    fig.tight_layout()

    fig.savefig(
        MODEL_DIR / "confusion_matrix.png",
        dpi=180
    )

    plt.close(fig)

    print("\nSaved evaluation files to:", MODEL_DIR)
    print(
        "\nImportant: these metrics measure performance "
        "on synthetic labels, not real-world student outcomes."
    )


if __name__ == "__main__":
    evaluate_model()