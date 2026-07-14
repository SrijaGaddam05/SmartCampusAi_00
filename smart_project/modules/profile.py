"""
Profile management module for SmartCampusAI.
Allows users to view/edit profile details and change passwords securely.
"""
import streamlit as st
from utils.database import load_json, update
from utils.security import hash_password, verify_password
from utils.validators import is_valid_email, validate_password_strength
from modules.helpers import log_activity, render_header

def render_profile() -> None:
    """Render the user profile details and settings page."""
    render_header(
        title="👤 User Profile Management",
        subtitle="Manage your personal details and security configuration"
    )
    
    user = st.session_state.user
    
    # Reload freshest user data from database
    all_users = load_json("users")
    user_db_entry = next((u for u in all_users if u["id"] == user["id"]), None)
    
    if not user_db_entry:
        st.error("User record not found in the database.")
        return
        
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📋 Account Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Username:** @{user_db_entry['username']}")
        st.write(f"**Account Role:** {user_db_entry['role']}")
    with col2:
        st.write(f"**Registered Date:** {user_db_entry.get('created_at', 'N/A')}")
        st.write(f"**User ID:** {user_db_entry['id']}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Edit profile details
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("✏️ Edit Profile Details")
    
    with st.form("edit_profile_form"):
        new_name = st.text_input("Full Name", value=user_db_entry.get("name", ""))
        new_email = st.text_input("Email Address", value=user_db_entry.get("email", ""))
        
        save_details = st.form_submit_button("Update Details")
        
        if save_details:
            if not new_name or not new_email:
                st.error("Full Name and Email Address cannot be blank.")
            elif not is_valid_email(new_email):
                st.error("Please enter a valid email address.")
            else:
                # Update user in DB
                updated_fields = {
                    "name": new_name.strip(),
                    "email": new_email.strip().lower()
                }
                if update("users", "id", user["id"], updated_fields):
                    # Also sync with student/faculty profiles if they exist
                    if user_db_entry["role"] == "Student":
                        update("students", "id", user["id"], {"name": new_name, "email": new_email})
                    elif user_db_entry["role"] == "Faculty":
                        update("faculty", "id", user["id"], {"name": new_name, "email": new_email})
                        
                    # Sync session state
                    st.session_state.user["name"] = new_name
                    st.session_state.user["email"] = new_email
                    
                    log_activity(user_db_entry["username"], "Profile Update", "Updated personal name or email details.")
                    st.success("Profile details updated successfully! Please reload the page if changes don't appear.")
                else:
                    st.error("Failed to save changes to the database.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Password Change Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔒 Security & Password Update")
    
    with st.form("password_change_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password (Min. 8 characters)", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        change_pass = st.form_submit_button("Update Password")
        
        if change_pass:
            if not current_password or not new_password or not confirm_password:
                st.error("All password fields are required.")
            elif not verify_password(current_password, user_db_entry["password"]):
                st.error("The current password you entered is incorrect.")
            elif new_password != confirm_password:
                st.error("New passwords do not match.")
            else:
                is_valid, msg = validate_password_strength(new_password)
                if not is_valid:
                    st.error(msg)
                else:
                    # Update password hash in DB
                    new_hash = hash_password(new_password)
                    if update("users", "id", user["id"], {"password": new_hash}):
                        log_activity(user_db_entry["username"], "Password Reset", "Updated secure password hash.")
                        st.success("Password changed successfully!")
                    else:
                        st.error("Failed to update database record.")
                        
    st.markdown("</div>", unsafe_allow_html=True)
