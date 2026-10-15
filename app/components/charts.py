import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def render_student_radar(gpa, internal, attendance, assignments, delays, activity):
    categories = ['Baseline', 'Internal', 'Attendance', 'Tasks', 'Punctual', 'Activity']
    norm_gpa = (gpa / 10.0) * 100
    norm_assign = (assignments / 10.0) * 100
    norm_punctual = max(0, 100 - ((delays / 14.0) * 100))
    values = [norm_gpa, internal, attendance, norm_assign, norm_punctual, activity]
    values.append(values[0])
    categories.append(categories[0])
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values, theta=categories, fill='toself', fillcolor='rgba(59, 130, 246, 0.25)',
        line=dict(color='#3B82F6', width=2), marker=dict(color='#ffffff', size=5, line=dict(color='#3B82F6', width=1)),
        hoverinfo="text", text=[f"{val:.1f}%" for val in values]
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 100], 
                gridcolor="rgba(255,255,255,0.1)", 
                linecolor="rgba(255,255,255,0.1)",
                tickfont=dict(size=8, color="rgba(255,255,255,0.4)")
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)", 
                linecolor="rgba(255,255,255,0.1)",
                tickfont=dict(color="#E2E8F0", size=10, family="Poppins")
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=15, b=15),
        height=200, showlegend=False # Reduced height for single-viewport fit
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_shap_waterfall(shap_dict):
    features = [f.replace('_', ' ').title() for f in shap_dict.keys()]
    impacts = list(shap_dict.values())
    
    fig = go.Figure(go.Waterfall(
        orientation="v", measure=["relative"] * len(impacts) + ["total"], x=features + ["Final"],
        textposition="outside", text=[f"{val:+.1f}" for val in impacts] + [""], y=impacts + [sum(impacts)],
        connector={"line": {"color": "rgba(255,255,255,0.2)", "width": 1, "dash": "dot"}}, 
        decreasing={"marker": {"color": "rgba(255,255,255,0.15)", "line": {"color": "rgba(255,255,255,0.3)", "width": 1}}}, 
        increasing={"marker": {"color": "#3B82F6", "line": {"color": "#60A5FA", "width": 1}}},
        totals={"marker": {"color": "#F8FAFC", "line": {"color": "rgba(255,255,255,0.5)", "width": 1}}}
    ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=15, b=0), height=200, # Reduced height
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickangle=-40, 
            gridcolor="rgba(0,0,0,0)", 
            linecolor="rgba(255,255,255,0.2)", 
            tickfont=dict(color="#E2E8F0", size=9, family="Poppins")
        ),
        yaxis=dict(
            title="Impact", 
            gridcolor="rgba(255,255,255,0.1)", 
            linecolor="rgba(255,255,255,0.2)", 
            title_font=dict(color="#94A3B8", size=10), 
            tickfont=dict(color="#94A3B8", size=9)
        )
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_cohort_distribution(df):
    grade_counts = df['final_grade'].value_counts().reindex(['A', 'B', 'C', 'D', 'F'])
    color_sequence = ['#3B82F6', '#2563EB', '#1D4ED8', '#1E3A8A', '#0F172A']
    
    fig = px.bar(
        x=grade_counts.index, y=grade_counts.values,
        color=grade_counts.index, color_discrete_sequence=color_sequence
    )
    
    fig.update_traces(marker_line_color='rgba(255,255,255,0.2)', marker_line_width=1)
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(t=10, l=0, r=0, b=0),
        height=250, # Set matching height for table side-by-side
        xaxis=dict(
            gridcolor="rgba(0,0,0,0)", 
            linecolor="rgba(255,255,255,0.2)",
            title="Projected Grade", 
            title_font=dict(color="#94A3B8", size=11), 
            tickfont=dict(color="#E2E8F0", size=11)
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.1)", 
            linecolor="rgba(255,255,255,0.2)",
            title="Number of Students", 
            title_font=dict(color="#94A3B8", size=11), 
            tickfont=dict(color="#94A3B8", size=10)
        )
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})