"""
Helper utilities for UI rendering and activity logging in SmartCampusAI.
"""
import os
import streamlit as st
import datetime
import uuid
from typing import Union
from utils.database import insert

def load_global_styles() -> None:
    """Load assets/styles.css stylesheet and inject into the Streamlit app."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("CSS asset file missing. Defaulting to system styles.")

def render_header(title: str, subtitle: str = "") -> None:
    """Render a gradient glassmorphism title header."""
    st.markdown(f"""
    <div style="margin-bottom: 25px;">
        <h1 class="header-gradient" style="margin: 0; font-size: 2.8rem; font-weight: 800; letter-spacing: -0.025em;">{title}</h1>
        {f'<p style="color: #94a3b8; font-size: 1.1rem; margin-top: 5px; font-weight: 400;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def render_stat_card(value: Union[str, int], label: str, icon: str = "📈") -> None:
    """Render a beautiful stat card with rounded border and glowing gradient values."""
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 1.8rem; margin-bottom: 5px;">{icon}</div>
        <div class="stat-val">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def log_activity(username: str, action: str, details: str = "") -> bool:
    """
    Log user activity to database/activity.json.
    """
    activity_item = {
        "id": str(uuid.uuid4()),
        "username": username,
        "action": action,
        "details": details,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return insert("activity", activity_item)
