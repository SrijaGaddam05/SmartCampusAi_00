"""
Student directory view component for SmartCampusAI.
"""
import streamlit as st
import pandas as pd
import uuid
import datetime
from modules.helpers import log_activity, render_header
from utils.database import load_json, insert, update, delete

def render_students() -> None:
    """Render the student management UI."""
    user = st.session_state.user
    is_admin_or_faculty = user.get("role") in ["Admin", "Faculty"]

    render_header("👨‍🎓 Student Management Directory", "Manage active campus enrollment profiles")

    # Search and Filter
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    col_search, col_dept = st.columns([2, 1])
    with col_search:
        search_q = st.text_input("Search student profiles...", placeholder="Type name or email to search")
    with col_dept:
        selected_dept = st.selectbox("Department Filter", ["All", "Computer Science", "Electrical Eng.", "Business Admin", "Mechanical Eng.", "Liberal Arts"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Load database
    students = load_json("students")

    # Perform search / filter
    filtered_students = students
    if search_q:
        filtered_students = [s for s in filtered_students if search_q.lower() in s.get("name", "").lower() or search_q.lower() in s.get("email", "").lower()]
    if selected_dept != "All":
        filtered_students = [s for s in filtered_students if s.get("department") == selected_dept]

    # Show records
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📋 Student Listings")

    if filtered_students:
        df = pd.DataFrame(filtered_students)[["id", "name", "email", "department", "enrollment_date", "status"]]
        df["Display ID"] = df["id"].apply(lambda x: x[:8] if isinstance(x, str) else str(x))
        df = df[["Display ID", "name", "email", "department", "enrollment_date", "status", "id"]]
        
        st.dataframe(
            df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )
        
        # Update and Delete tools (Admin/Faculty only)
        if is_admin_or_faculty:
            st.markdown("<hr style='border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
            st.subheader("⚙️ Actions")
            
            act_col1, act_col2 = st.columns(2)
            
            with act_col1:
                st.write("**Edit Student Details**")
                edit_id = st.selectbox("Select Student to Edit", options=[s["id"] for s in filtered_students], format_func=lambda x: next(s["name"] for s in students if s["id"] == x))
                
                student_to_edit = next(s for s in students if s["id"] == edit_id)
                
                with st.form("edit_student_form"):
                    e_name = st.text_input("Name", value=student_to_edit["name"])
                    e_email = st.text_input("Email", value=student_to_edit["email"])
                    e_dept = st.selectbox("Department", ["Computer Science", "Electrical Eng.", "Business Admin", "Mechanical Eng.", "Liberal Arts"], index=["Computer Science", "Electrical Eng.", "Business Admin", "Mechanical Eng.", "Liberal Arts"].index(student_to_edit.get("department", "Computer Science")))
                    e_status = st.selectbox("Status", ["Active", "Inactive", "Suspended"], index=["Active", "Inactive", "Suspended"].index(student_to_edit.get("status", "Active")))
                    
                    edit_submit = st.form_submit_button("Save Student Changes")
                    if edit_submit:
                        updated_data = {
                            "name": e_name.strip(),
                            "email": e_email.strip(),
                            "department": e_dept,
                            "status": e_status
                        }
                        if update("students", "id", edit_id, updated_data):
                            log_activity(user["username"], "Edit Student", f"Updated student profile: {e_name} ({edit_id[:8]})")
                            st.success("Student details updated successfully!")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to update student database entry.")
                            
            with act_col2:
                st.write("**Remove Student Profile**")
                delete_id = st.selectbox("Select Student to Delete", options=[s["id"] for s in filtered_students], format_func=lambda x: next(s["name"] for s in students if s["id"] == x), key="del_sel")
                
                student_to_delete = next(s for s in students if s["id"] == delete_id)
                
                confirm_del = st.checkbox(f"Confirm permanent deletion of {student_to_delete['name']}", key="conf_del_box")
                del_btn = st.button("❌ Delete Student Profile")
                
                if del_btn:
                    if not confirm_del:
                        st.warning("Please confirm deletion by checking the confirmation box.")
                    else:
                        if delete("students", "id", delete_id):
                            log_activity(user["username"], "Delete Student", f"Deleted student: {student_to_delete['name']}")
                            st.success("Student removed successfully.")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to delete database entry.")
    else:
        st.info("No matching student records found.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Create Student Panel (Admin/Faculty only)
    if is_admin_or_faculty:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("➕ Enroll New Student")
        
        with st.form("add_student_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                n_name = st.text_input("Full Name", placeholder="e.g. Michael Scott")
                n_email = st.text_input("Email Address", placeholder="e.g. michael@university.edu")
            with col_f2:
                n_dept = st.selectbox("Academic Department", ["Computer Science", "Electrical Eng.", "Business Admin", "Mechanical Eng.", "Liberal Arts"])
                n_status = st.selectbox("Enrollment Status", ["Active", "Inactive"])
                
            add_submit = st.form_submit_button("Register Student")
            
            if add_submit:
                if not n_name or not n_email:
                    st.error("Name and Email address are required fields.")
                else:
                    student_item = {
                        "id": str(uuid.uuid4()),
                        "name": n_name.strip(),
                        "email": n_email.strip(),
                        "department": n_dept,
                        "enrollment_date": datetime.date.today().strftime("%Y-%m-%d"),
                        "status": n_status
                    }
                    if insert("students", student_item):
                        log_activity(user["username"], "Add Student", f"Added student profile: {n_name}")
                        st.success(f"Successfully registered student {n_name}!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to save student profile to database.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-card' style='border-color: rgba(239, 68, 68, 0.2);'>", unsafe_allow_html=True)
        st.subheader("➕ Enroll New Student")
        st.warning("⚠️ Only Faculty and Administrator roles have permissions to modify enrollment details.")
        st.markdown("</div>", unsafe_allow_html=True)
