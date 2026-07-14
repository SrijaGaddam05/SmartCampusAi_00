"""
Authentication module for SmartCampusAI.
Handles login, registration, password verification, and page access control.
"""
import streamlit as st
import datetime
import uuid
import os
from utils.database import load_json, insert, search
from utils.security import hash_password, verify_password
from utils.validators import is_valid_email, validate_password_strength, is_username_taken, is_email_taken
from modules.helpers import log_activity, load_global_styles

def check_auth() -> None:
    """
    Gatekeeper function to prevent unauthorized page access.
    """
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("🔒 Access denied. Please login first.")
        st.stop()

def logout() -> None:
    """Clear login status and session state."""
    username = st.session_state.get("user", {}).get("username", "Unknown")
    log_activity(username, "Logout", "User logged out of session.")
    
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.current_page = "Dashboard"
    st.success("Successfully logged out.")
    st.experimental_rerun()

def render_login_form() -> None:
    """Render the login form panel."""
    st.markdown("<div style='text-align: center;'><h3>Sign In</h3></div>", unsafe_allow_html=True)
    
    username_or_email = st.text_input("Username or Email", key="login_username", placeholder="Enter username or email")
    password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        remember_me = st.checkbox("Remember Me", key="remember_me")
    with col2:
        forgot_clicked = st.button("Forgot Password?", key="forgot_pass", use_container_width=True)
        
    if forgot_clicked:
        st.session_state.auth_view = "forgot"
        st.experimental_rerun()
        
    submit = st.button("Login", key="login_submit")
    
    if submit:
        if not username_or_email or not password:
            st.error("Please enter both credentials.")
            return
            
        # Search user database
        users = load_json("users")
        target_user = None
        
        # Check if username or email matches
        for u in users:
            if u["username"].lower() == username_or_email.lower() or u["email"].lower() == username_or_email.lower():
                target_user = u
                break
                
        if target_user and verify_password(password, target_user["password"]):
            st.session_state.logged_in = True
            st.session_state.user = {
                "id": target_user["id"],
                "username": target_user["username"],
                "email": target_user["email"],
                "role": target_user.get("role", "Student"),
                "name": target_user.get("name", target_user["username"].capitalize())
            }
            log_activity(target_user["username"], "Login", "Successful login via auth portal.")
            st.success(f"Welcome back, {st.session_state.user['name']}!")
            st.session_state.current_page = "Dashboard"
            st.experimental_rerun()
        else:
            st.error("Invalid username/email or password.")

def render_register_form() -> None:
    """Render registration form with validators."""
    st.markdown("<div style='text-align: center;'><h3>Create Account</h3></div>", unsafe_allow_html=True)
    
    name = st.text_input("Full Name", placeholder="e.g. John Doe")
    username = st.text_input("Username", placeholder="e.g. johndoe")
    email = st.text_input("Email Address", placeholder="e.g. john@university.edu")
    password = st.text_input("Password", type="password", placeholder="Min. 8 characters")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
    
    role = st.selectbox("Role", ["Student", "Faculty", "Admin"])
    
    submit = st.button("Register", key="register_submit")
    
    if submit:
        # 1. Check blank fields
        if not name or not username or not email or not password or not confirm_password:
            st.error("All fields are required.")
            return
            
        # 2. Check passwords match
        if password != confirm_password:
            st.error("Passwords do not match.")
            return
            
        # 3. Check password length
        is_pass_valid, pass_msg = validate_password_strength(password)
        if not is_pass_valid:
            st.error(pass_msg)
            return
            
        # 4. Check email format
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return
            
        # 5. Check duplicate username
        if is_username_taken(username):
            st.error("Username is already taken.")
            return
            
        # 6. Check duplicate email
        if is_email_taken(email):
            st.error("An account with this email is already registered.")
            return
            
        # Register user
        hashed = hash_password(password)
        user_item = {
            "id": str(uuid.uuid4()),
            "name": name,
            "username": username.lower().strip(),
            "email": email.lower().strip(),
            "password": hashed,
            "role": role,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if insert("users", user_item):
            # Seed to matching student or faculty lists automatically
            if role == "Student":
                student_item = {
                    "id": user_item["id"],
                    "name": name,
                    "email": email,
                    "username": username,
                    "department": "Computer Science",
                    "enrollment_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "status": "Active"
                }
                insert("students", student_item)
            elif role == "Faculty":
                faculty_item = {
                    "id": user_item["id"],
                    "name": name,
                    "email": email,
                    "username": username,
                    "department": "Computer Science",
                    "designation": "Assistant Professor",
                    "status": "Active"
                }
                insert("faculty", faculty_item)
                
            log_activity(username, "Registration", f"New user account registered as {role}.")
            st.success("Account registered successfully! Logging you in...")
            
            # Automatic login
            st.session_state.logged_in = True
            st.session_state.user = {
                "id": user_item["id"],
                "username": user_item["username"],
                "email": user_item["email"],
                "role": user_item["role"],
                "name": user_item["name"]
            }
            st.session_state.current_page = "Dashboard"
            st.experimental_rerun()
        else:
            st.error("Failed to write account records to database. Please try again.")

def render_forgot_password() -> None:
    """Render password reset mockup form."""
    st.markdown("<div style='text-align: center;'><h3>Reset Password</h3></div>", unsafe_allow_html=True)
    
    email = st.text_input("Enter your registered Email", placeholder="e.g. john@university.edu")
    submit = st.button("Send Reset Link", key="forgot_submit")
    
    if submit:
        if not email:
            st.error("Email address is required.")
            return
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return
            
        # Search if email exists
        users = load_json("users")
        found = False
        for u in users:
            if u["email"].lower() == email.lower():
                found = True
                break
                
        if found:
            st.success("🔒 A secure password reset link has been dispatched to your email address (Mock).")
        else:
            st.error("No account found matching this email address.")
            
    if st.button("Return to Sign In"):
        st.session_state.auth_view = "login"
        st.experimental_rerun()

def render_auth_page() -> None:
    """Main rendering wrapper for the authentication screen."""
    load_global_styles()
    
    # Check current session view state
    if "auth_view" not in st.session_state:
        st.session_state.auth_view = "login"
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 3-column layout to center the login container
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown("<div class='glass-card' style='padding: 30px;'>", unsafe_allow_html=True)
        
        # Campus logo & welcome header
        logo_col, title_col = st.columns([1, 3])
        with logo_col:
            logo_path = os.path.join("assets", "logo.png")
            if os.path.exists(logo_path):
                st.image(logo_path, width=70)
        with title_col:
            st.markdown("<h2 style='margin:0; font-weight: 700;'>SmartCampusAI</h2><p style='color:#94a3b8; margin:0;'>AI-Powered Education Portal</p>", unsafe_allow_html=True)
            
        st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 20px 0;'>", unsafe_allow_html=True)
        
        if st.session_state.auth_view == "login":
            render_login_form()
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94a3b8;'>Don't have an account?</p>", unsafe_allow_html=True)
            if st.button("Register Account", use_container_width=True):
                st.session_state.auth_view = "register"
                st.experimental_rerun()
                
        elif st.session_state.auth_view == "register":
            render_register_form()
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94a3b8;'>Already have an account?</p>", unsafe_allow_html=True)
            if st.button("Sign In instead", use_container_width=True):
                st.session_state.auth_view = "login"
                st.experimental_rerun()
                
        elif st.session_state.auth_view == "forgot":
            render_forgot_password()
            
        st.markdown("</div>", unsafe_allow_html=True)
