import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

def preprocess_data(filepath="data/raw/synthetic_student_data.csv"):
    df = pd.read_csv(filepath)
    
    # Separate features (X) and target (y)
    X = df.drop(columns=['student_id', 'final_grade'])
    y = df['final_grade']
    
    # Encode target labels (A, B, C, D, F) into numbers
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Train/test split (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Scale numerical features 
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert back to DataFrame to preserve column names (critical for SHAP explainability later)
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns)
    
    # Save preprocessors for the UI inference layer
    os.makedirs("src/models/saved_models", exist_ok=True)
    joblib.dump(scaler, "src/models/saved_models/scaler.pkl")
    joblib.dump(label_encoder, "src/models/saved_models/label_encoder.pkl")
    
    return X_train_scaled, X_test_scaled, y_train, y_test