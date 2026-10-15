import os
import sys
import html
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "src" / "models" / "saved_models"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.explainability.shap_explainer import get_student_explanation
from src.intervention.recommender import generate_recommendations
from app.components.layouts import apply_glassmorphism_theme, render_page_header, render_panel_header
from app.components.cards import render_progress_metric, render_status_metric, render_gradient_metric
from app.components.charts import render_shap_waterfall, render_student_radar

st.set_page_config(page_title="CampusGrade AI | Student Analytics", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")
apply_glassmorphism_theme()
render_page_header("Student Analytics Engine", "Predictive analytics, SHAP explanations, and intervention plans")

EXPECTED_FEATURES = ["previous_gpa", "internal_marks", "attendance_pct", "assignments_completed", "submission_delay_days", "learning_activity_score"]

@st.cache_resource
def load_models():
    required_files = {
        "model": MODEL_DIR / "rf_model.pkl",
        "imputer": MODEL_DIR / "imputer.pkl",
        "scaler": MODEL_DIR / "scaler.pkl",
        "encoder": MODEL_DIR / "label_encoder.pkl",
        "features": MODEL_DIR / "feature_columns.pkl",
    }
    missing_files = [str(path) for path in required_files.values() if not path.is_file()]
    if missing_files:
        raise FileNotFoundError("Missing model artifacts:\n" + "\n".join(missing_files))
    
    model = joblib.load(required_files["model"])
    imputer = joblib.load(required_files["imputer"])
    scaler = joblib.load(required_files["scaler"])
    encoder = joblib.load(required_files["encoder"])
    feature_columns = list(joblib.load(required_files["features"]))
    return model, imputer, scaler, encoder, feature_columns

try:
    rf_model, imputer, scaler, encoder, feature_columns = load_models()
except Exception as exc:
    st.error(f"Unable to load the ML model: {exc}")
    st.stop()

# Use smaller gaps for a tighter layout
col1, col2, col3 = st.columns([1.2, 1.3, 0.8], gap="small")

with col2:
    with st.container(border=True):
        render_panel_header("What-If Simulator")
        sim_col1, sim_col2 = st.columns(2, gap="small")
        with sim_col1:
            prev_gpa = st.slider("Previous GPA", 0.0, 10.0, 7.5, 0.1, key="previous_gpa")
            internal = st.slider("Internal Marks", 0, 100, 75, key="internal_marks")
            attendance = st.slider("Attendance %", 0, 100, 85, key="attendance_pct")
        with sim_col2:
            assignments = st.slider("Tasks Completed", 0, 10, 8, key="assignments_completed")
            delays = st.slider("Submission Delays (Days)", 0, 14, 2, key="submission_delay_days")
            activity = st.slider("Platform Activity", 0, 100, 70, key="learning_activity_score")

input_data = pd.DataFrame({
    "previous_gpa": [prev_gpa], "internal_marks": [internal], "attendance_pct": [attendance],
    "assignments_completed": [assignments], "submission_delay_days": [delays], "learning_activity_score": [activity]
})[feature_columns]

try:
    input_imputed = pd.DataFrame(imputer.transform(input_data), columns=feature_columns, index=input_data.index)
    input_scaled = pd.DataFrame(scaler.transform(input_imputed), columns=feature_columns, index=input_data.index)
    pred_index = rf_model.predict(input_scaled)[0]
    pred_grade = str(encoder.inverse_transform(np.asarray([pred_index]).astype(int))[0])
    probabilities = rf_model.predict_proba(input_scaled)[0]
    class_probabilities = {str(encoder.inverse_transform(np.asarray([c]).astype(int))[0]): float(p) for c, p in zip(rf_model.classes_, probabilities)}
    top_probability = max(probabilities) * 100
except Exception as exc:
    st.error(f"Prediction failed: {exc}")
    st.stop()

status, status_color_key = ("Low Risk", "safe") if pred_grade in ["A", "B"] else ("Monitor", "monitor") if pred_grade == "C" else ("High Risk", "risk")

try:
    shap_dict = get_student_explanation(input_scaled, pred_index) or {}
except Exception:
    shap_dict = {}

with col1:
    with st.container(border=True):
        render_panel_header("Digital Twin Radar")
        render_student_radar(prev_gpa, internal, attendance, assignments, delays, activity)

    with st.container(border=True):
        render_panel_header("Action Roadmap")
        recommendations = generate_recommendations(shap_dict) if shap_dict else []
        if not recommendations:
            st.info("No recommendations available.")
        else:
            roadmap_html = ""
            for idx, rec in enumerate(recommendations):
                safe_rec = html.escape(str(rec))
                is_last = idx == len(recommendations) - 1
                border_style = "border-left: 2px dashed rgba(96,165,250,0.4);" if not is_last else "border-left: 2px solid transparent;"
                roadmap_html += f"""
                <div style="position: relative; {border_style} margin-left: 5px; padding-left: 15px; padding-bottom: 8px;">
                    <div style="position: absolute; left: -6px; top: 2px; width: 10px; height: 10px; background: #3B82F6; border-radius: 50%; box-shadow: 0 0 6px rgba(59,130,246,0.6);"></div>
                    <div style="color: #93C5FD; font-weight: 700; font-size: 9px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Step {idx + 1}</div>
                    <div style="background: rgba(15,23,42,0.5); border: 1px solid rgba(255,255,255,0.1); padding: 8px 12px; border-radius: 8px; color: #F1F5F9; font-size: 11px; line-height: 1.4;">{safe_rec}</div>
                </div>
                """
            st.markdown(roadmap_html, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        render_panel_header("AI Factors")
        if shap_dict:
            render_shap_waterfall(shap_dict)
        else:
            st.info("SHAP factors are unavailable.")

with col3:
    render_progress_metric("Predicted Grade", pred_grade, round(top_probability, 1), "Model Confidence")
    render_status_metric("Risk Level", status, "Grade-based trajectory", status_color_key)
    render_gradient_metric("Academic Baseline", str(prev_gpa), "Previous GPA")
    render_gradient_metric("Engagement Index", str(activity), "Platform Activity")

    if attendance < 60 and activity < 50:
        persona, p_color = "Disengaged Ghost", "#94A3B8"
    elif delays >= 3 and activity >= 60:
        persona, p_color = "Last-Minute Sprinter", "#F59E0B"
    elif prev_gpa < 6.0 and activity >= 75:
        persona, p_color = "Struggling Grinder", "#3B82F6"
    elif delays <= 1 and attendance >= 85 and prev_gpa >= 7.5:
        persona, p_color = "Consistent Scholar", "#10B981"
    else:
        persona, p_color = "Unpredictable Wildcard", "#8B5CF6"

    archetype_html = f"""
    <div style="background: rgba(15,23,42,0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 12px 16px; margin-bottom: 10px; position: relative; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <div style="position: absolute; right: -15px; top: -15px; width: 60px; height: 60px; background: radial-gradient(circle, {p_color} 0%, transparent 70%); opacity: 0.2; pointer-events: none;"></div>
        <div style="color: #94A3B8; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">AI Behavioral Archetype</div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 8px; height: 8px; background: {p_color}; border-radius: 50%; box-shadow: 0 0 8px {p_color};"></div>
            <div style="color: #F8FAFC; font-size: 14px; font-weight: 700;">{html.escape(persona)}</div>
        </div>
    </div>
    """
    st.markdown(archetype_html, unsafe_allow_html=True)

    with st.container(border=True):
        render_panel_header("Grade Probabilities")
        ordered_grades = [str(g) for g in encoder.classes_ if str(g) in class_probabilities] + [g for g in class_probabilities if g not in [str(x) for x in encoder.classes_]]
        for grade in ordered_grades:
            prob = class_probabilities[grade]
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; color: #E2E8F0; font-size: 11px; margin-top: 4px; margin-bottom: 2px; font-weight: 500;">
                    <span>Grade {html.escape(grade)}</span><span>{prob * 100:.1f}%</span>
                </div>
            """, unsafe_allow_html=True)
            st.progress(min(max(prob, 0.0), 1.0))