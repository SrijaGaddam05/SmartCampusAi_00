"""
Attendance view component for SmartCampusAI.
"""
import streamlit as st
import pandas as pd
import datetime
import uuid
from modules.helpers import log_activity, render_header
from utils.database import load_json, save_json, insert, search

def render_attendance() -> None:
    """Render class attendance logging UI."""
    user = st.session_state.user
    is_admin_or_faculty = user.get("role") in ["Admin", "Faculty"]

    render_header("📅 Student Attendance Tracker", "Log and monitor daily class attendance records")

    # 1. Filters Row
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    col_date, col_dept = st.columns(2)
    with col_date:
        selected_date = st.date_input("Attendance Logging Date", value=datetime.date.today())
        selected_date_str = selected_date.strftime("%Y-%m-%d")
    with col_dept:
        selected_dept = st.selectbox("Department", ["Computer Science", "Electrical Eng.", "Business Admin", "Mechanical Eng.", "Liberal Arts"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Load databases
    students = load_json("students")
    all_attendance = load_json("attendance")

    # Filter students
    dept_students = [s for s in students if s.get("department") == selected_dept]

    if not dept_students:
        st.info(f"No student profiles are registered under the {selected_dept} department.")
    else:
        date_attendance = {
            a["student_id"]: a["status"] 
            for a in all_attendance 
            if a.get("date") == selected_date_str and a.get("department") == selected_dept
        }
        
        # 2. Statistics
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader(f"📊 Attendance Summary - {selected_dept} on {selected_date_str}")
        
        if date_attendance:
            total_marked = len(dept_students)
            present_count = sum(1 for status in date_attendance.values() if status == "Present")
            absent_count = total_marked - present_count
            rate = (present_count / total_marked) * 100 if total_marked > 0 else 0
            
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("Total Present", f"{present_count} students")
            with stat_col2:
                st.metric("Total Absent", f"{absent_count} students")
            with stat_col3:
                st.metric("Attendance Rate", f"{rate:.1f}%")
        else:
            st.info("Attendance has not been logged yet for this group on the selected date.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 3. Sheet Mark
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📝 Record Attendance sheet")
        
        if not is_admin_or_faculty:
            st.warning("⚠️ You are logged in with a Student role. Attendance logs are view-only.")
            display_data = []
            for s in dept_students:
                status = date_attendance.get(s["id"], "Unmarked")
                display_data.append({
                    "Student Name": s["name"],
                    "Email": s["email"],
                    "Attendance Status": status
                })
            st.dataframe(pd.DataFrame(display_data), use_container_width=True, hide_index=True)
            
        else:
            with st.form("attendance_sheet_form"):
                st.write("Toggle checkmark if the student is Present:")
                checkboxes = {}
                
                for s in dept_students:
                    default_present = date_attendance.get(s["id"], "Present") == "Present"
                    checkboxes[s["id"]] = st.checkbox(s["name"], value=default_present, help=s["email"])
                    
                submit_attendance = st.form_submit_button("Submit Attendance Sheet")
                
                if submit_attendance:
                    updated_attendance = [a for a in all_attendance if not (a.get("date") == selected_date_str and a.get("department") == selected_dept)]
                    
                    for s in dept_students:
                        status = "Present" if checkboxes[s["id"]] else "Absent"
                        att_item = {
                            "id": str(uuid.uuid4()),
                            "student_id": s["id"],
                            "student_name": s["name"],
                            "department": selected_dept,
                            "date": selected_date_str,
                            "status": status,
                            "marked_by": user["username"]
                        }
                        updated_attendance.append(att_item)
                        
                    if save_json("attendance", updated_attendance):
                        log_activity(user["username"], "Log Attendance", f"Logged attendance for {selected_dept} on {selected_date_str}.")
                        st.success("Attendance sheet recorded successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to commit attendance updates to database.")
        st.markdown("</div>", unsafe_allow_html=True)
