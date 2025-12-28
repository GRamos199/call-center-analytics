"""
Call Center Analytics Dashboard
Main application entry point for the Streamlit dashboard.
"""
import streamlit as st
from pathlib import Path
import sys

# Add analytics folder to path for imports
analytics_dir = Path(__file__).parent
sys.path.insert(0, str(analytics_dir))

from classes.monthly_tab import MonthlyTab
from classes.weekly_tab import WeeklyTab
from classes.style_manager import StyleManager
from reporting.welcome_page import WelcomePage


def render_sidebar_header():
    """Render animated sidebar header."""
    header_html = """
<style>
.sidebar-header {
    position: relative;
    background: linear-gradient(135deg, #3B82F6 0%, #F63B83 50%, #83F63B 100%);
    border-radius: 16px;
    padding: 20px;
    margin: -1rem -1rem 1.5rem -1rem;
    overflow: hidden;
    text-align: center;
}
.sidebar-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.15) 50%, transparent 70%);
    animation: sidebar-shimmer 4s infinite linear;
}
@keyframes sidebar-shimmer {
    0% { transform: translateX(-100%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}
.sidebar-logo {
    position: relative;
    z-index: 2;
    font-size: 48px;
    margin-bottom: 10px;
    animation: logo-pulse 2s ease-in-out infinite;
}
@keyframes logo-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}
.sidebar-title {
    position: relative;
    z-index: 2;
    color: white;
    font-size: 18px;
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
.sidebar-subtitle {
    position: relative;
    z-index: 2;
    color: rgba(255,255,255,0.9);
    font-size: 11px;
    margin-top: 5px;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.sidebar-dots {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 15px;
}
.sidebar-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255,255,255,0.5);
    animation: dot-bounce 1.5s ease-in-out infinite;
}
.sidebar-dot:nth-child(1) { animation-delay: 0s; }
.sidebar-dot:nth-child(2) { animation-delay: 0.2s; }
.sidebar-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes dot-bounce {
    0%, 100% { transform: translateY(0); opacity: 0.5; }
    50% { transform: translateY(-5px); opacity: 1; }
}
</style>
<div class="sidebar-header">
    <div class="sidebar-logo">📊</div>
    <h2 class="sidebar-title">Call Center Analytics</h2>
    <p class="sidebar-subtitle">Performance Dashboard</p>
    <div class="sidebar-dots">
        <div class="sidebar-dot"></div>
        <div class="sidebar-dot"></div>
        <div class="sidebar-dot"></div>
    </div>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)


def render_nav_section():
    """Render navigation section with styled label."""
    nav_label = """
<div style="
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    padding: 8px 12px;
    background: rgba(59, 130, 246, 0.1);
    border-radius: 8px;
    border-left: 3px solid #3B82F6;
">
    <span style="font-size: 14px;">🧭</span>
    <span style="color: rgba(255,255,255,0.9); font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">Navigation</span>
</div>
"""
    st.markdown(nav_label, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar navigation and settings."""
    with st.sidebar:
        # Animated header
        render_sidebar_header()
        
        # Navigation section
        render_nav_section()
        
        # Initialize session state for report selection
        if "report_type" not in st.session_state:
            st.session_state.report_type = "Welcome"
        
        # Create buttons stacked vertically
        if st.button(
            "🏠 Home",
            key="btn_home",
            use_container_width=True,
        ):
            st.session_state.report_type = "Welcome"
        
        if st.button(
            "📅 Monthly Report",
            key="btn_monthly",
            use_container_width=True,
        ):
            st.session_state.report_type = "Monthly Report"
        
        if st.button(
            "📆 Weekly Report",
            key="btn_weekly",
            use_container_width=True,
        ):
            st.session_state.report_type = "Weekly Report"
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # About section with styled header
        about_label = """
<div style="
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    padding: 8px 12px;
    background: rgba(246, 59, 131, 0.1);
    border-radius: 8px;
    border-left: 3px solid #F63B83;
">
    <span style="font-size: 14px;">ℹ️</span>
    <span style="color: rgba(255,255,255,0.9); font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">About</span>
</div>
"""
        st.markdown(about_label, unsafe_allow_html=True)
        
        # About content with styled container
        about_content = """
<div style="
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.1);
">
    <p style="color: #3B82F6; font-weight: 700; font-size: 13px; margin-bottom: 8px;">
        Call Center Analytics Dashboard
    </p>
    <p style="color: rgba(255,255,255,0.6); font-size: 11px; margin-bottom: 12px;">
        Version 1.0.0
    </p>
    <div style="display: flex; flex-direction: column; gap: 6px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #83F63B; font-size: 12px;">●</span>
            <span style="color: rgba(255,255,255,0.8); font-size: 11px;">Cost per agent analysis</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #F63B83; font-size: 12px;">●</span>
            <span style="color: rgba(255,255,255,0.8); font-size: 11px;">Cost per client metrics</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #3B82F6; font-size: 12px;">●</span>
            <span style="color: rgba(255,255,255,0.8); font-size: 11px;">Productivity indicators</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #83F63B; font-size: 12px;">●</span>
            <span style="color: rgba(255,255,255,0.8); font-size: 11px;">Agent performance tracking</span>
        </div>
    </div>
</div>
"""
        st.markdown(about_content, unsafe_allow_html=True)
    
    return st.session_state.report_type


def render_main_dashboard(report_type):
    """Render the main dashboard content."""
    if report_type == "Welcome":
        welcome_page = WelcomePage()
        welcome_page.render()
    elif report_type == "Monthly Report":
        monthly_tab = MonthlyTab()
        monthly_tab.render()
    else:
        weekly_tab = WeeklyTab()
        weekly_tab.render()


def main():
    """Main application entry point."""
    StyleManager.setup()
    report_type = render_sidebar()
    render_main_dashboard(report_type)


if __name__ == "__main__":
    main()
