import os

# Define the absolute path to the project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# -----------------------------------------
# DATA DIRECTORIES
# -----------------------------------------
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "synthetic_student_data.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed", "cleaned_data.csv")

# -----------------------------------------
# MODEL ARTIFACT DIRECTORIES
# -----------------------------------------
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "src", "models", "saved_models")
RF_MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "rf_model.pkl")
LR_MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "lr_model.pkl")
SCALER_PATH = os.path.join(SAVED_MODELS_DIR, "scaler.pkl")
ENCODER_PATH = os.path.join(SAVED_MODELS_DIR, "label_encoder.pkl")

# -----------------------------------------
# MACHINE LEARNING PARAMETERS
# -----------------------------------------
MODEL_SEED = 42
TEST_SPLIT_SIZE = 0.2

# Define target and feature columns
TARGET_COLUMN = "final_grade"
DROP_COLUMNS = ["student_id", TARGET_COLUMN]