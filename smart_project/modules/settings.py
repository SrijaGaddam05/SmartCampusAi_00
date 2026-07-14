"""
Settings module for SmartCampusAI.
Manages global system settings, theme selections, and notification rules.
"""
import streamlit as st
from utils.database import load_json, save_json
from modules.helpers import log_activity, render_header

def render_settings() -> None:
    """Render system settings UI panel."""
    render_header(
        title="⚙️ Platform Settings",
        subtitle="Configure portal options and workspace behaviors"
    )
    
    user = st.session_state.user
    
    # Check permissions
    is_admin = user.get("role") == "Admin"
    
    # Load settings from db
    settings = load_json("settings")
    if not isinstance(settings, dict) or not settings:
        settings = {
            "theme": "Dark",
            "notifications_enabled": True,
            "maintenance_mode": False,
            "system_name": "SmartCampusAI"
        }
        
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🎨 Customization & Theme")
    
    # Theme configuration
    theme_options = ["Dark", "Light"]
    current_theme = settings.get("theme", "Dark")
    theme_idx = theme_options.index(current_theme) if current_theme in theme_options else 0
    
    selected_theme = st.selectbox(
        "Application Color Palette", 
        theme_options, 
        index=theme_idx,
        help="Select between Dark Mode or Light Mode theme environments."
    )
    
    # Toggle to mimic dark mode in-app
    if selected_theme != current_theme:
        settings["theme"] = selected_theme
        save_json("settings", settings)
        log_activity(user["username"], "Theme Change", f"Toggled theme environment to {selected_theme}.")
        st.success(f"Theme updated to {selected_theme}! Please refresh the page to apply changes.")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔔 Alerts & Notifications")
    
    notifs_enabled = st.toggle(
        "Enable Real-time Web Notifications", 
        value=settings.get("notifications_enabled", True)
    )
    
    if notifs_enabled != settings.get("notifications_enabled"):
        settings["notifications_enabled"] = notifs_enabled
        save_json("settings", settings)
        log_activity(user["username"], "Notifications Toggle", f"Notifications set to {notifs_enabled}.")
        st.info("Notification parameters saved.")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Admin settings
    if is_admin:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🛡️ Administrative Dashboard Controls")
        
        system_name = st.text_input("Campus System Name", value=settings.get("system_name", "SmartCampusAI"))
        maintenance_mode = st.toggle("Activate Portal Maintenance Mode", value=settings.get("maintenance_mode", False))
        
        save_admin = st.button("Apply Admin Parameters")
        
        if save_admin:
            settings["system_name"] = system_name.strip()
            settings["maintenance_mode"] = maintenance_mode
            if save_json("settings", settings):
                log_activity(user["username"], "Admin Settings Update", "Updated system name or maintenance state.")
                st.success("System configurations applied successfully.")
            else:
                st.error("Error committing admin changes to database.")
                
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-card' style='border-color: rgba(239, 68, 68, 0.2);'>", unsafe_allow_html=True)
        st.subheader("🛡️ Administrative Controls")
        st.warning("⚠️ Administrative dashboard settings are read-only for your current role status.")
        st.markdown("</div>", unsafe_allow_html=True)
