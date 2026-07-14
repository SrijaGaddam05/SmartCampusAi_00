"""
Sidebar navigation module for SmartCampusAI.
Renders the custom sidebar with user details and the option menu.
"""
import streamlit as st
import os
from streamlit_option_menu import option_menu
from modules.authentication import logout

# Map options to page file names (relative to the pages/ directory or app root)
PAGE_ROUTING = {
    "Dashboard": "pages/Home.py",
    "Students": "pages/Students.py",
    "Faculty": "pages/Faculty.py",
    "Attendance": "pages/Attendance.py",
    "Timetable": "pages/Timetable.py",
    "AI Assistant": "pages/AI_Assistant.py",
    "Analytics": "pages/Analytics.py",
    "Profile": "pages/Profile.py",
    "Settings": "pages/Settings.py"
}

def render_sidebar(active_name: str) -> None:
    """
    Renders the sidebar navigation panel.
    Args:
        active_name (str): The name of the active page to select in the menu.
    """
    # 1. Check database setup/session status
    if "user" not in st.session_state or not st.session_state.logged_in:
        return
        
    user = st.session_state.user
    
    with st.sidebar:
        # Display logo
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)
            
        st.markdown(f"""
        <div style="padding: 10px 0; margin-bottom: 10px;">
            <h3 style="margin: 0; font-weight: 700; font-size: 1.3rem; color: #ffffff;">SmartCampusAI</h3>
            <span style="color: #6366f1; font-size: 0.85rem; font-weight: 600;">{user.get('role', 'Member')} Portal</span>
        </div>
        """, unsafe_allow_html=True)
        
        # User details card in sidebar
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 10px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Welcome,</div>
            <div style="font-weight: 600; color: #f3f4f6; font-size: 1rem; margin-top: 2px;">{user.get('name', 'User')}</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 1px;">@{user.get('username', 'user')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Options
        options = [
            "Dashboard", "Students", "Faculty", "Attendance", "Timetable", 
            "AI Assistant", "Analytics", "Profile", "Settings", "Logout"
        ]
        
        icons = [
            "house", "mortarboard", "person-workspace", "calendar-check", "calendar-week", 
            "robot", "graph-up-arrow", "person-bounding-box", "gear", "box-arrow-right"
        ]
        
        # Resolve active page index
        default_index = 0
        if active_name in options:
            default_index = options.index(active_name)
            
        selected = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            menu_icon="cast",
            default_index=default_index,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#94a3b8", "font-size": "15px"},
                "nav-link": {
                    "font-size": "14px", 
                    "text-align": "left", 
                    "margin": "0px", 
                    "color": "#f3f4f6", 
                    "background-color": "transparent",
                    "font-weight": "400",
                    "padding": "10px 15px",
                    "border-radius": "8px"
                },
                "nav-link-selected": {"background-color": "rgba(99, 102, 241, 0.2)", "font-weight": "600", "border-left": "3px solid #6366f1"},
            }
        )
        
        # Process redirection
        if selected == "Logout":
            logout()
        elif selected != active_name:
            st.session_state.current_page = selected
            st.experimental_rerun()
