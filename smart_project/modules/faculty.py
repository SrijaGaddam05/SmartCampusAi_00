"""
Faculty directory view component for SmartCampusAI.
"""
import streamlit as st
import pandas as pd
import uuid
from modules.helpers import log_activity, render_header
from utils.database import load_json, insert, update, delete

def render_faculty() -> None:
    """Render faculty directory UI."""
    user = st.session_state.user
    is_admin = user.get("role") == "Admin"

    render_header("👨‍🏫 Faculty Directory", "Manage university professors and staff registries")

    # Search and filter UI
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    col_search, col_dept = st.columns([2, 1])
    with col_search:
        search_q = st.text_input("Search faculty members...", placeholder="Type name or email to search")
    with col_dept:
        selected_dept = st.selectbox("Department Filter", ["All", "Computer Science", "Electrical Eng.", "Business Admin", "Mechanical Eng.", "Liberal Arts"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Load faculty database
    faculty = load_json("faculty")

    # Filter results
    filtered_faculty = faculty
    if search_q:
        filtered_faculty = [f for f in filtered_faculty if search_q.lower() in f.get("name", "").lower() or search_q.lower() in f.get("email", "").lower()]
    if selected_dept != "All":
        filtered_faculty = [f for f in filtered_faculty if f.get("department") == selected_dept]

    # Render Faculty directory
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📋 Faculty Listings")

    if filtered_faculty:
        df = pd.DataFrame(filtered_faculty)[["id", "name", "email", "department", "designation", "status"]]
        df["Display ID"] = df["id"].apply(lambda x: x[:8] if isinstance(x, str) else str(x))
        df = df[["Display ID", "name", "email", "department", "designation", "status", "id"]]
        
        st.dataframe(
            df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )
        
        # Edit / Delete actions (Admin only)
        if is_admin:
            st.markdown("<hr style='border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
            st.subheader("⚙️ Actions")
            
            act_col1, act_col2 = st.columns(2)
            
            with act_col1:
                st.write("**Edit Faculty Details**")
                edit_id = st.selectbox("Select Member to Edit", options=[f["id"] for f in filtered_faculty], format_func=lambda x: next(fac["name"] for fac in faculty if fac["id"] == x))
                
                faculty_to_edit = next(f for f in faculty if f["id"] == edit_id)
                
                with st.form("edit_faculty_form"):
                    e_name = st.text_input("Name", value=faculty_to_edit["name"])
                    e_email = st.text_input("Email", value=faculty_to_edit["email"])
                    e_des = st.text_input("Designation", value=faculty_to_edit.get("designation", "Professor"))
                    e_dept = st.selectbox("Department", ["Computer Science", "Electrical Eng.", "Business Admin", "Mechanical Eng.", "Liberal Arts"], index=["Computer Science", "Electrical Eng.", "Business Admin", "Mechanical Eng.", "Liberal Arts"].index(faculty_to_edit.get("department", "Computer Science")))
                    e_status = st.selectbox("Status", ["Active", "Inactive"], index=["Active", "Inactive"].index(faculty_to_edit.get("status", "Active")))
                    
                    edit_submit = st.form_submit_button("Save Faculty Changes")
                    if edit_submit:
                        updated_data = {
                            "name": e_name.strip(),
                            "email": e_email.strip(),
                            "designation": e_des.strip(),
                            "department": e_dept,
                            "status": e_status
                        }
                        if update("faculty", "id", edit_id, updated_data):
                            log_activity(user["username"], "Edit Faculty", f"Updated faculty member: {e_name} ({edit_id[:8]})")
                            st.success("Faculty details updated successfully!")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to update database record.")
                            
            with act_col2:
                st.write("**Remove Faculty Profile**")
                delete_id = st.selectbox("Select Member to Delete", options=[f["id"] for f in filtered_faculty], format_func=lambda x: next(fac["name"] for fac in faculty if fac["id"] == x), key="del_sel_fac")
                
                faculty_to_delete = next(f for f in faculty if f["id"] == delete_id)
                
                confirm_del = st.checkbox(f"Confirm permanent deletion of {faculty_to_delete['name']}", key="conf_del_fac_box")
                del_btn = st.button("❌ Delete Faculty Profile")
                
                if del_btn:
                    if not confirm_del:
                        st.warning("Please confirm deletion by checking the confirmation box.")
                    else:
                        if delete("faculty", "id", delete_id):
                            log_activity(user["username"], "Delete Faculty", f"Deleted faculty member: {faculty_to_delete['name']}")
                            st.success("Faculty member removed successfully.")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to delete database entry.")
    else:
        st.info("No matching faculty records found.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Add Faculty Panel (Admin only)
    if is_admin:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("➕ Register New Faculty Member")
        
        with st.form("add_faculty_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                n_name = st.text_input("Full Name", placeholder="e.g. Dr. Jane Foster")
                n_email = st.text_input("Email Address", placeholder="e.g. jane@university.edu")
                n_des = st.text_input("Academic Designation", placeholder="e.g. Associate Professor")
            with col_f2:
                n_dept = st.selectbox("Academic Department", ["Computer Science", "Electrical Eng.", "Business Admin", "Mechanical Eng.", "Liberal Arts"])
                n_status = st.selectbox("Employment Status", ["Active", "Inactive"])
                
            add_submit = st.form_submit_button("Register Faculty Profile")
            
            if add_submit:
                if not n_name or not n_email or not n_des:
                    st.error("Name, email, and designation are required fields.")
                else:
                    faculty_item = {
                        "id": str(uuid.uuid4()),
                        "name": n_name.strip(),
                        "email": n_email.strip(),
                        "designation": n_des.strip(),
                        "department": n_dept,
                        "status": n_status
                    }
                    if insert("faculty", faculty_item):
                        log_activity(user["username"], "Add Faculty", f"Added faculty profile: {n_name}")
                        st.success(f"Successfully registered faculty member {n_name}!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to save faculty profile to database.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-card' style='border-color: rgba(239, 68, 68, 0.2);'>", unsafe_allow_html=True)
        st.subheader("➕ Register New Faculty Member")
        st.warning("⚠️ Only Administrator roles have authorization to register or modify faculty credentials.")
        st.markdown("</div>", unsafe_allow_html=True)
