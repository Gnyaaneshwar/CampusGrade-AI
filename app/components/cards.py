import streamlit as st

def render_gradient_metric(title, value, subtitle=""):
    html = f"""
    <div style="
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 10px 14px; 
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.15);
        text-align: left;
        margin-bottom: 10px; 
        transition: transform 0.2s ease;
    ">
        <div style="color: #94A3B8; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px;">{title}</div>
        <div style="
            font-size: 26px; 
            font-weight: 800; 
            margin-bottom: 0px;
            color: #F8FAFC;
            line-height: 1.1;
        ">{value}</div>
        <div style="color: #60A5FA; font-size: 11px; font-weight: 500;">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_progress_metric(title, value, percentage, subtitle=""):
    deg = int((percentage / 100) * 360)
    html = f"""
    <div style="
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.15);
        margin-bottom: 10px; 
    ">
        <div style="flex: 1; padding-right: 8px;">
            <div style="color: #94A3B8; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px;">{title}</div>
            <div style="color: #F8FAFC; font-size: 26px; font-weight: 800; margin-bottom: 0px; line-height: 1.1;">{value}</div>
            <div style="color: #60A5FA; font-size: 11px; font-weight: 500;">{subtitle}</div>
        </div>
        <div style="
            width: 42px; height: 42px; min-width: 42px; border-radius: 50%; 
            background: conic-gradient(#3B82F6 {deg}deg, rgba(255,255,255,0.05) 0deg);
            display: flex; align-items: center; justify-content: center;
            box-shadow: inset 0 0 6px rgba(0,0,0,0.4);
            flex-shrink: 0;
        ">
            <div style="
                width: 34px; height: 34px; background: #0F172A; border-radius: 50%; 
                display: flex; align-items: center; justify-content: center;
                font-size: 10px; font-weight: 700; color: #F8FAFC;
            ">{percentage}%</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_status_metric(title, status_text, subtitle="", status_level="monitor"):
    color = {"safe": "#10B981", "monitor": "#F59E0B", "risk": "#EF4444"}.get(status_level.lower(), "#3B82F6")
    html = f"""
    <div style="
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 10px 14px;
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.15);
        margin-bottom: 10px; 
    ">
        <div style="color: #94A3B8; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">{title}</div>
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0px;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background-color: {color}; box-shadow: 0 0 10px {color}; flex-shrink: 0;"></div>
            <div style="color: #F8FAFC; font-size: 26px; font-weight: 800; line-height: 1.1;">{status_text}</div>
        </div>
        <div style="color: #60A5FA; font-size: 11px; font-weight: 500;">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)