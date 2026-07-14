"""
Analytics module for SmartCampusAI.
Renders comprehensive reports and interactive data charts.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.database import load_json
from modules.helpers import render_header

def render_analytics() -> None:
    """Render the detailed analytics dashboards."""
    render_header(
        title="📊 Campus Analytics & Reports",
        subtitle="Detailed visualizations and administrative metrics"
    )
    
    # Load databases
    students = load_json("students")
    faculty = load_json("faculty")
    
    # Fallback to rich mock data if empty
    if not students:
        students = [
            {"id": "1", "name": "Alice Smith", "department": "Computer Science", "status": "Active"},
            {"id": "2", "name": "Bob Jones", "department": "Computer Science", "status": "Active"},
            {"id": "3", "name": "Charlie Brown", "department": "Electrical Eng.", "status": "Active"},
            {"id": "4", "name": "Diana Prince", "department": "Electrical Eng.", "status": "Inactive"},
            {"id": "5", "name": "Ethan Hunt", "department": "Business Admin", "status": "Active"},
            {"id": "6", "name": "Fiona Gallagher", "department": "Business Admin", "status": "Active"},
            {"id": "7", "name": "George Clark", "department": "Mechanical Eng.", "status": "Active"},
            {"id": "8", "name": "Hannah Abbott", "department": "Liberal Arts", "status": "Active"}
        ]
        
    if not faculty:
        faculty = [
            {"id": "f1", "name": "Dr. Alan Turing", "department": "Computer Science"},
            {"id": "f2", "name": "Dr. Grace Hopper", "department": "Computer Science"},
            {"id": "f3", "name": "Prof. Nikola Tesla", "department": "Electrical Eng."},
            {"id": "f4", "name": "Dr. Adam Smith", "department": "Business Admin"},
            {"id": "f5", "name": "Prof. Albert Einstein", "department": "Mechanical Eng."}
        ]
        
    df_students = pd.DataFrame(students)
    df_faculty = pd.DataFrame(faculty)
    
    # --- SECTION 1: ENROLLMENT & RATIOS ---
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("👥 Student vs. Faculty Ratios by Department")
    
    # Count students by department
    stud_dept = df_students.groupby("department").size().reset_index(name="Students")
    fac_dept = df_faculty.groupby("department").size().reset_index(name="Faculty")
    
    # Merge
    ratio_df = pd.merge(stud_dept, fac_dept, on="department", how="outer").fillna(0)
    
    # Bar Chart
    fig_bar = go.Figure(data=[
        go.Bar(name='Students', x=ratio_df['department'], y=ratio_df['Students'], marker_color='#6366f1'),
        go.Bar(name='Faculty', x=ratio_df['department'], y=ratio_df['Faculty'], marker_color='#a78bfa')
    ])
    fig_bar.update_layout(
        barmode='group',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f3f4f6"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        margin=dict(l=20, r=20, t=10, b=20),
        height=300
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- SECTION 2: COMPARATIVE DISTRIBUTIONS ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🎓 Student Status Breakdown")
        
        status_counts = df_students["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        
        fig_status = px.pie(
            status_counts, values="Count", names="Status",
            color_discrete_sequence=px.colors.sequential.Agsunset
        )
        fig_status.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f3f4f6"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=250
        )
        st.plotly_chart(fig_status, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📆 Attendance Rates by Semester")
        
        semesters = ["Fall 24", "Spring 25", "Summer 25", "Fall 25"]
        perf = [91.2, 93.5, 94.6, 92.8]
        df_sem = pd.DataFrame({"Semester": semesters, "Attendance Rate %": perf})
        
        fig_sem = px.bar(
            df_sem, x="Semester", y="Attendance Rate %",
            color="Attendance Rate %",
            color_continuous_scale="Viridis"
        )
        fig_sem.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f3f4f6"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", range=[80, 100]),
            margin=dict(l=10, r=10, t=10, b=10),
            height=250,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_sem, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # --- SECTION 3: REPORT EXPORT GENERATION ---
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📥 Export Administrative Reports")
    st.write("Generate and download reports for audit and administrative review.")
    
    rep_col1, rep_col2 = st.columns(2)
    with rep_col1:
        # Student Directory CSV
        csv_students = df_students.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Student Directory CSV",
            data=csv_students,
            file_name="student_directory_report.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    with rep_col2:
        # Faculty Directory CSV
        csv_faculty = df_faculty.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Faculty Directory CSV",
            data=csv_faculty,
            file_name="faculty_directory_report.csv",
            mime="text/csv",
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
