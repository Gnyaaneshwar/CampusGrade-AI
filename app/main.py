import streamlit as st
import os
import sys
from pathlib import Path

# FIX: Robust path resolution so 'app.components' always works regardless of where you run it
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(page_title="CampusGrade AI | Portal", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")

if 'portal_open' not in st.session_state:
    st.session_state.portal_open = False

def trigger_transition():
    st.session_state.portal_open = True

container_animation = "shutterDown 1.0s cubic-bezier(0.25, 1, 0.5, 1) forwards" if not st.session_state.portal_open else "shutterUp 1.0s cubic-bezier(0.25, 1, 0.5, 1) forwards"

def inject_custom_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
        
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="collapsedControl"], [data-testid="stSidebar"] {{display: none !important;}}
        
        .stApp {{ 
            background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%) !important; 
            background-attachment: fixed;
        }}
        
        * {{ font-family: 'Poppins', sans-serif !important; }}
        
        .block-container {{
            padding-top: 10vh !important; 
            padding-bottom: 5vh !important;
            max-width: 1100px !important;
            text-align: center;
            animation: {container_animation};
            margin: 0 auto;
        }}
        
        @keyframes shutterDown {{
            0% {{ opacity: 0; transform: translateY(-50px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes shutterUp {{
            0% {{ opacity: 0; transform: translateY(50px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .hero-title {{
            font-size: 4.5rem;
            font-weight: 800;
            color: #0F172A;
            text-shadow: 0 4px 16px rgba(255,255,255,0.5);
            margin-bottom: 0px;
            letter-spacing: -0.03em;
            line-height: 1.2;
        }}
        
        .hero-subtitle {{ 
            color: #1E293B; 
            font-size: 1.3rem; 
            font-weight: 600;
            margin-bottom: 50px; 
            text-shadow: 0 2px 8px rgba(255,255,255,0.4);
            opacity: 0.9;
        }}
        
        div.stButton > button {{
            background: rgba(15, 23, 42, 0.75);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(12px);
            padding: 16px 36px;
            font-size: 1.1rem;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 50px; 
            display: block;
            margin-left: auto;
            margin-right: auto;
            box-shadow: 0 8px 32px rgba(15, 23, 42, 0.2);
        }}
        
        div.stButton > button:hover {{
            background: rgba(15, 23, 42, 0.95);
            border-color: #60A5FA !important;
            box-shadow: 0 12px 40px rgba(96, 165, 250, 0.3);
            transform: translateY(-3px);
            color: #ffffff !important;
        }}
        
        .kpi-card {{
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px;
            padding: 28px 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .kpi-card:hover {{ 
            transform: translateY(-5px); 
            background: rgba(15, 23, 42, 0.8);
            border-color: rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
        }}
        
        .kpi-title {{ color: #94A3B8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; }}
        .kpi-val {{ color: #ffffff; font-size: 38px; font-weight: 700; margin-bottom: 6px; line-height: 1.1; }}
        .kpi-sub {{ color: #60A5FA; font-size: 13px; font-weight: 500; }}
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

if not st.session_state.portal_open:
    st.markdown("""
    <div>
        <div class="hero-title">CampusGrade AI</div>
        <div class="hero-subtitle">Intelligent Academic Intervention System</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.button("Enter Portal", on_click=trigger_transition, use_container_width=True)
    
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">System Status</div>
            <div class="kpi-val">Online</div>
            <div class="kpi-sub">ML Backend Active</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Records Processed</div>
            <div class="kpi-val">1,000+</div>
            <div class="kpi-sub">Synthetic DB</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Model Accuracy</div>
            <div class="kpi-val">90.0%</div>
            <div class="kpi-sub">Random Forest</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="margin-top: 5vh;">
        <h2 style='color: #0F172A; margin-bottom: 5px; font-size: 3.5rem; font-weight: 800; text-shadow: 0 4px 16px rgba(255,255,255,0.4); letter-spacing: -1px;'>Select Module</h2>
        <p style='color: #1E293B; margin-bottom: 40px; font-size: 1.2rem; font-weight: 600;'>Route the connection to a specific dashboard.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("Student Analytics Engine", use_container_width=True):
            st.switch_page("pages/1_student_dashboard.py")
        
        st.write("<br>", unsafe_allow_html=True)
        
        if st.button("Faculty Cohort Engine", use_container_width=True):
            st.switch_page("pages/2_faculty_dashboard.py")