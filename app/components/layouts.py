import streamlit as st

def apply_glassmorphism_theme():
    """Injects global CSS for a high-density, responsive Dark Glassmorphism layout."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
        
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="collapsedControl"], [data-testid="stSidebar"] {display: none !important;}
        
        .stApp { 
            background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%) !important; 
            background-attachment: fixed;
        }
        
        * { font-family: 'Poppins', sans-serif !important; }
        
        /* Compact Container to fit 1080p and 768p natively */
        .block-container {
            padding-top: 1.5rem !important; 
            padding-bottom: 1.5rem !important;
            max-width: 1400px !important; 
        }

        /* Tighten Streamlit gaps */
        [data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
        div[data-testid="stSlider"] { padding-bottom: 0px !important; margin-bottom: -15px !important;}
        
        /* Compact Titles */
        .dash-title {
            font-size: 2rem; 
            font-weight: 800;
            color: #0F172A; 
            text-shadow: 0 2px 10px rgba(255, 255, 255, 0.4); 
            margin-bottom: 2px;
            line-height: 1.1;
            letter-spacing: -0.5px;
            text-align: center; /* FORCES TEXT ALIGNMENT */
        }
        
        .dash-subtitle { 
            color: #1E293B; 
            font-size: 0.95rem; 
            font-weight: 600;
            margin-bottom: 1rem; 
            text-shadow: 0 1px 4px rgba(255, 255, 255, 0.3);
            letter-spacing: 0.5px;
            text-align: center; /* FORCES TEXT ALIGNMENT */
        }

        /* Compact Glass Panels */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: rgba(15, 23, 42, 0.65) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important; 
            border-radius: 12px !important;
            padding: 0.8rem 1rem !important; 
            box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15) !important;
            transition: border-color 0.3s ease;
        }
        
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: rgba(255, 255, 255, 0.3) !important; 
        }

        /* Center Column Gradient (Student Dashboard) */
        [data-testid="column"]:nth-of-type(2) [data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(135deg, rgba(30, 58, 138, 0.8) 0%, rgba(49, 46, 129, 0.8) 100%) !important;
            border: 1px solid rgba(96, 165, 250, 0.3) !important; 
            box-shadow: 0 4px 16px 0 rgba(37, 99, 235, 0.2) !important;
        }

        [data-testid="stWidgetLabel"] p {
            color: #F8FAFC !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            margin-bottom: 0 !important;
        }
        .stSlider > div > div > div > div { color: #ffffff !important; }

        /* Sleek Back Button */
        div.stButton > button {
            background: rgba(15, 23, 42, 0.7);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            backdrop-filter: blur(8px);
            padding: 4px 14px;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin-top: 0px;
            position: relative; /* FIX: Force button above overlay text */
            z-index: 999;       /* FIX: Protect clickability */
        }
        
        div.stButton > button:hover {
            background: rgba(15, 23, 42, 0.95);
            border-color: #60A5FA !important;
            box-shadow: 0 4px 12px rgba(96, 165, 250, 0.3);
            transform: translateY(-2px);
            color: #ffffff !important;
        }
        
        [data-testid="stDataFrame"] { background: transparent; }
    </style>
    """, unsafe_allow_html=True)

def render_page_header(title, subtitle):
    # 1. Render the Back button isolated in a tiny corner column
    col_back, col_empty = st.columns([1, 11])
    
    with col_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.portal_open = False
            st.switch_page("main.py")

    # 2. Render the Title using a full-width container and negative margin.
    # This guarantees it is MATHEMATICALLY dead-center on the screen, 
    # ignoring the layout footprint of the Back button.
    st.markdown(f"""
    <div style="margin-top: -45px; pointer-events: none; position: relative; z-index: 0;">
        <div class="dash-title" style="pointer-events: auto;">{title}</div>
        <div class="dash-subtitle" style="pointer-events: auto;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def render_panel_header(title):
    st.markdown(f"""
    <div style="
        color: #F8FAFC;
        font-weight: 700;
        font-size: 0.85rem;
        margin-bottom: 8px; 
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
        text-align: center; /* FORCES PANEL HEADERS TO CENTER */
    ">{title}</div>
    """, unsafe_allow_html=True)