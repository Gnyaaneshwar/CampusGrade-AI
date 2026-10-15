import shap
import joblib
import numpy as np
import pandas as pd

def get_student_explanation(student_features_scaled, predicted_class_index):
    """
    Generates SHAP values for a single student to explain the prediction.
    """
    # Load model inside function to ensure it runs cleanly when imported by Streamlit
    rf_model = joblib.load("src/models/saved_models/rf_model.pkl")
    
    # Initialize TreeExplainer
    explainer = shap.TreeExplainer(rf_model)
    
    # Calculate SHAP values
    shap_values = explainer.shap_values(student_features_scaled)
    
    # Handle different SHAP return formats based on version
    if isinstance(shap_values, list):
        # Older SHAP versions return a list of arrays: [class_0_array, class_1_array, ...]
        class_shap_values = shap_values[predicted_class_index][0]
    else:
        # Newer SHAP versions return a 3D numpy array: (n_samples, n_features, n_classes)
        # We extract the 0th sample, all features, for the specific predicted class
        class_shap_values = shap_values[0, :, predicted_class_index]
    
    # Create a dictionary mapping feature names to their impact scores
    feature_names = student_features_scaled.columns
    impact_dict = {feature_names[i]: class_shap_values[i] for i in range(len(feature_names))}
    
    # Sort by absolute impact (highest impact first)
    sorted_impact = dict(sorted(impact_dict.items(), key=lambda item: abs(item[1]), reverse=True))
    
    return sorted_impact