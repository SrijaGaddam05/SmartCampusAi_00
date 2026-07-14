"""
Main entry point for SmartCampusAI.
Operates as a dynamic single-page portal router for backward compatibility with all Streamlit runtimes.
"""
import streamlit as st

# Set global page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="SmartCampusAI - Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State values
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

def main():
    # If not logged in, render authentication page
    if not st.session_state.logged_in:
        from modules.authentication import render_auth_page
        render_auth_page()
    else:
        # Load global styles
        from modules.helpers import load_global_styles
        load_global_styles()
        
        # Load sidebar navigation
        from modules.sidebar import render_sidebar
        render_sidebar(st.session_state.current_page)
        
        # Resolve active page layout
        page = st.session_state.current_page
        
        if page == "Dashboard":
            from modules.dashboard import render_dashboard
            render_dashboard()
        elif page == "Students":
            from modules.students import render_students
            render_students()
        elif page == "Faculty":
            from modules.faculty import render_faculty
            render_faculty()
        elif page == "Attendance":
            from modules.attendance import render_attendance
            render_attendance()
        elif page == "Timetable":
            from modules.timetable import render_timetable
            render_timetable()
        elif page == "AI Assistant":
            from modules.chatbot import render_chatbot
            render_chatbot()
        elif page == "Analytics":
            from modules.analytics import render_analytics
            render_analytics()
        elif page == "Profile":
            from modules.profile import render_profile
            render_profile()
        elif page == "Settings":
            from modules.settings import render_settings
            render_settings()

if __name__ == "__main__":
    main()
