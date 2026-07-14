"""
Dashboard module for SmartCampusAI.
Renders KPI panels, charts, recent activities, announcements, and quick actions.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from utils.database import load_json
from modules.helpers import render_stat_card, render_header

def get_dashboard_metrics() -> dict:
    """Retrieve dynamic metrics from database JSON files."""
    students = load_json("students")
    faculty = load_json("faculty")
    activities = load_json("activity")
    attendance = load_json("attendance")
    
    # Calculate counts
    total_students = len(students)
    total_faculty = len(faculty)
    
    # Fallback to realistic mock values if database is empty
    if total_students == 0:
        total_students = 1540
    if total_faculty == 0:
        total_faculty = 84
        
    # Today's attendance percentage
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    today_att = [a for a in attendance if a.get("date") == today_str]
    if today_att:
        p_count = sum(1 for a in today_att if a.get("status") == "Present")
        att_pct = f"{int((p_count / len(today_att)) * 100)}%"
    else:
        # Default mock attendance
        att_pct = "94.2%"
        
    # AI Requests count from activity log
    ai_reqs = sum(1 for act in activities if "AI" in act.get("action", ""))
    if ai_reqs == 0:
        ai_reqs = 342  # default mock value
        
    return {
        "students": total_students,
        "faculty": total_faculty,
        "attendance": att_pct,
        "ai_requests": ai_reqs
    }

def render_dashboard() -> None:
    """Main dashboard rendering function."""
    user = st.session_state.user
    
    # Header
    render_header(
        title=f"Welcome back, {user.get('name', 'User')}! 👋",
        subtitle=f"Here is what's happening at the campus today • {datetime.date.today().strftime('%A, %b %d, %Y')}"
    )
    
    # Load Metrics
    metrics = get_dashboard_metrics()
    
    # KPI Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_stat_card(metrics["students"], "Total Students", "👨‍🎓")
    with col2:
        render_stat_card(metrics["faculty"], "Total Faculty", "👨‍🏫")
    with col3:
        render_stat_card(metrics["attendance"], "Today's Attendance", "📅")
    with col4:
        render_stat_card(metrics["ai_requests"], "AI Requests", "🤖")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Section
    chart_col1, chart_col2 = st.columns([3, 2])
    
    with chart_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📈 Attendance Trends (Weekly)")
        
        # Weekly Mock Data
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        rates = [94.5, 95.2, 93.8, 94.2, 92.1, 85.0, 78.4]
        df_att = pd.DataFrame({"Day": days, "Attendance %": rates})
        
        fig_att = px.line(
            df_att, x="Day", y="Attendance %", 
            markers=True,
            color_discrete_sequence=["#6366f1"]
        )
        fig_att.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f3f4f6"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", range=[70, 100]),
            margin=dict(l=20, r=20, t=10, b=20),
            height=250
        )
        st.plotly_chart(fig_att, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with chart_col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Department Distribution")
        
        # Donut Chart Mock Data
        deps = ["Comp. Sci", "Engineering", "Business", "Arts", "Sciences"]
        counts = [450, 320, 290, 180, 300]
        df_dep = pd.DataFrame({"Department": deps, "Students": counts})
        
        fig_dep = px.pie(
            df_dep, values="Students", names="Department", 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Blues
        )
        fig_dep.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f3f4f6"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=250,
            showlegend=False
        )
        st.plotly_chart(fig_dep, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Lower Section
    lower_col1, lower_col2 = st.columns([3, 2])
    
    with lower_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🕒 Recent Activity Log")
        
        activities = load_json("activity")
        if activities:
            # Sort by timestamp descending
            sorted_act = sorted(activities, key=lambda x: x.get("timestamp", ""), reverse=True)[:5]
            df_act = pd.DataFrame(sorted_act)[["timestamp", "username", "action", "details"]]
            
            # Format dataframe column headers
            df_act.columns = ["Time", "User", "Action", "Details"]
            st.dataframe(
                df_act, 
                use_container_width=True, 
                hide_index=True
            )
        else:
            st.info("No activity records registered yet.")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("⚡ Quick Actions")
        qa_col1, qa_col2, qa_col3 = st.columns(3)
        with qa_col1:
            if st.button("➕ Add Student"):
                st.switch_page("pages/Students.py")
        with qa_col2:
            if st.button("📝 Log Attendance"):
                st.switch_page("pages/Attendance.py")
        with qa_col3:
            if st.button("🤖 Ask Assistant"):
                st.switch_page("pages/AI_Assistant.py")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with lower_col2:
        # Announcements
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📢 Announcements")
        st.markdown("""
        **🎓 Semester Registration Open**  
        <span style="color:#6366f1; font-size:0.8rem;">July 12 • Academic Office</span>  
        Registration for the Fall semester is open. Deadline is August 10.
        
        **💡 AI Hackathon 2026**  
        <span style="color:#6366f1; font-size:0.8rem;">July 10 • Tech Club</span>  
        Join our annual AI hackathon next weekend. Registrations close on Thursday.
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # System Calendar (Mock)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🗓️ Calendar & Events")
        
        current_date = datetime.date.today()
        # Renders a neat interactive calendar widget
        st.date_input("Select Event Date", value=current_date)
        
        # Events on selected date
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; font-size: 0.85rem; border-left: 3px solid #6366f1;">
            <b>Events on {current_date.strftime('%b %d')}:</b><br>
            • 10:00 AM - Faculty Board Meeting<br>
            • 02:00 PM - CS Lab Review
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
