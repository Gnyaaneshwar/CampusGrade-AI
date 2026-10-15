import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.components.layouts import apply_glassmorphism_theme, render_page_header, render_panel_header
from app.components.cards import render_gradient_metric, render_status_metric
from app.components.charts import render_cohort_distribution

st.set_page_config(page_title="CampusGrade AI | Faculty Analytics", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")
apply_glassmorphism_theme()
render_page_header("Faculty Cohort Engine", "Class-wide performance distribution and risk triage")

@st.cache_data
def load_cohort_data():
    return pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw/synthetic_student_data.csv')))

df = load_cohort_data()
risk_df = df[df['final_grade'].isin(['D', 'F'])]

if len(risk_df) > 0:
    avg_att = risk_df['attendance_pct'].mean()
    primary_issue = "Critical Attendance Drop" if avg_att < 75 else "Assignment Completion Rate"
    pulse_text = f"High Risk Cluster Detected: {primary_issue}."
    pulse_color = "#EF4444" 
else:
    pulse_text = "Cohort Tracking Optimal."
    pulse_color = "#10B981" 

# Tighten gap
kpi1, kpi2, kpi3, kpi4 = st.columns([1, 1, 1, 1.5], gap="small")
with kpi1: 
    render_gradient_metric("Total Enrollment", str(len(df)), "Active Students")
with kpi2: 
    render_gradient_metric("Average GPA", str(round(df['previous_gpa'].mean(), 2)), "Historical Baseline")
with kpi3: 
    render_status_metric("High Risk", str(len(risk_df)), "Projected D or F", "risk")
with kpi4:
    st.markdown(f"""
    <div style="
        background: rgba(30, 58, 138, 0.4); 
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-radius: 12px; 
        padding: 12px 16px; 
        height: 100%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    ">
        <div style="color: #93C5FD; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
            <div style="width: 8px; height: 8px; background: {pulse_color}; border-radius: 50%; box-shadow: 0 0 10px {pulse_color};"></div>
            AI Cohort Pulse
        </div>
        <div style="color: #F8FAFC; font-size: 13px; font-weight: 500; line-height: 1.4;">{pulse_text}</div>
    </div>
    """, unsafe_allow_html=True)

col_chart, spacer, col_table = st.columns([1, 0.02, 1.2], gap="small")

with col_chart:
    with st.container(border=True):
        render_panel_header("Projected Grade Distribution")
        render_cohort_distribution(df)

with col_table:
    with st.container(border=True):
        render_panel_header("Priority At-Risk Triage")
        display_df = risk_df[['student_id', 'previous_gpa', 'attendance_pct', 'final_grade']].sort_values(by='attendance_pct')
        display_df.columns = ['Student ID', 'Prev GPA', 'Attendance %', 'Proj. Grade']
        
        # Constrain height so the table has an internal scrollbar on 1080p/768p and matches chart height
        st.dataframe(
            display_df.reset_index(drop=True), 
            use_container_width=True, 
            height=250,
            hide_index=True
        )