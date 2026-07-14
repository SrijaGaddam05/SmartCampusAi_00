"""
Timetable scheduler view component for SmartCampusAI.
"""
import streamlit as st
import pandas as pd
import uuid
from modules.helpers import log_activity, render_header
from utils.database import load_json, save_json, insert, delete

def render_timetable() -> None:
    """Render scheduling grid UI."""
    user = st.session_state.user
    is_admin_or_faculty = user.get("role") in ["Admin", "Faculty"]

    render_header("📖 Academic Timetable Scheduler", "Browse and structure weekly course agendas")

    # 1. Filters Row
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    col_dept, col_sem = st.columns(2)
    with col_dept:
        selected_dept = st.selectbox("Department", ["Computer Science", "Electrical Eng.", "Business Admin", "Mechanical Eng.", "Liberal Arts"])
    with col_sem:
        selected_sem = st.selectbox("Semester", ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5", "Semester 6", "Semester 7", "Semester 8"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Load database
    timetable = load_json("timetable")
    filtered_slots = [
        t for t in timetable 
        if t.get("department") == selected_dept and t.get("semester") == selected_sem
    ]

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # 2. Render schedule
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader(f"📅 Weekly Schedule for {selected_dept} ({selected_sem})")

    if filtered_slots:
        sorted_slots = sorted(filtered_slots, key=lambda x: (days_order.index(x.get("day", "Monday")), x.get("time", "")))
        
        for day in days_order:
            day_slots = [s for s in sorted_slots if s["day"] == day]
            if day_slots:
                st.markdown(f"#### 📅 {day}")
                slot_cols = st.columns(len(day_slots) if len(day_slots) <= 4 else 4)
                for idx, slot in enumerate(day_slots):
                    col_idx = idx % len(slot_cols)
                    with slot_cols[col_idx]:
                        st.markdown(f"""
                        <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                            <span style="font-size: 0.8rem; font-weight: 600; color: #a78bfa;">{slot['time']}</span><br>
                            <b style="font-size: 1rem; color: #ffffff;">{slot['subject']}</b><br>
                            <span style="font-size: 0.85rem; color: #94a3b8;">👨‍🏫 {slot['instructor']}</span><br>
                            <span style="font-size: 0.85rem; color: #94a3b8;">🚪 {slot['room']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if is_admin_or_faculty:
                            if st.button(f"🗑️ Delete ID {slot['id'][:4]}", key=f"del_{slot['id']}"):
                                if delete("timetable", "id", slot["id"]):
                                    log_activity(user["username"], "Delete Timetable Slot", f"Removed slot: {slot['subject']}")
                                    st.success("Schedule slot deleted!")
                                    st.experimental_rerun()
                                else:
                                    st.error("Error deleting slot.")
                st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 10px 0;'>", unsafe_allow_html=True)
    else:
        st.info("No classes are currently scheduled for this department and semester selection.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Add Schedule Slot (Admin/Faculty only)
    if is_admin_or_faculty:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("➕ Schedule a New Class Slot")
        
        with st.form("add_slot_form"):
            col1, col2 = st.columns(2)
            with col1:
                n_subject = st.text_input("Course Subject", placeholder="e.g. Machine Learning")
                n_instructor = st.text_input("Instructor Name", placeholder="e.g. Dr. Grace Hopper")
                n_room = st.text_input("Room / Laboratory Location", placeholder="e.g. Lab 402 or Room 102")
            with col2:
                n_day = st.selectbox("Day of the Week", days_order)
                time_options = [
                    "09:00 AM - 10:30 AM",
                    "10:30 AM - 12:00 PM",
                    "12:00 PM - 01:30 PM",
                    "02:00 PM - 03:30 PM",
                    "03:30 PM - 05:00 PM"
                ]
                n_time = st.selectbox("Class Time Slot", time_options)
                
            slot_submit = st.form_submit_button("Add to Semester Timetable")
            
            if slot_submit:
                if not n_subject or not n_instructor or not n_room:
                    st.error("All schedule fields are required.")
                else:
                    slot_item = {
                        "id": str(uuid.uuid4()),
                        "department": selected_dept,
                        "semester": selected_sem,
                        "day": n_day,
                        "time": n_time,
                        "subject": n_subject.strip(),
                        "instructor": n_instructor.strip(),
                        "room": n_room.strip()
                    }
                    if insert("timetable", slot_item):
                        log_activity(user["username"], "Add Timetable Slot", f"Scheduled course slot: {n_subject}")
                        st.success(f"Successfully added class slot: {n_subject}!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to write class slot to database.")
        st.markdown("</div>", unsafe_allow_html=True)
