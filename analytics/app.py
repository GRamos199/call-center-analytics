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


def render_sidebar():
    """Render sidebar navigation and settings."""
    st.sidebar.title("Call Center Analytics")
    st.sidebar.markdown("---")
    
    # Initialize session state for report selection
    if "report_type" not in st.session_state:
        st.session_state.report_type = "Monthly Report"
    
    # Create buttons stacked vertically
    if st.sidebar.button(
        "Monthly Report",
        key="btn_monthly",
        use_container_width=True,
    ):
        st.session_state.report_type = "Monthly Report"
    
    if st.sidebar.button(
        "Weekly Report",
        key="btn_weekly",
        use_container_width=True,
    ):
        st.session_state.report_type = "Weekly Report"
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("About")
    st.sidebar.markdown("""
    **Call Center Analytics Dashboard**
    
    Version: 1.0.0
    
    This dashboard provides comprehensive analytics for call center operations including:
    - Cost per agent analysis
    - Cost per client metrics
    - Productivity indicators
    - Agent performance tracking
    """)
    
    return st.session_state.report_type


def render_main_dashboard(report_type):
    """Render the main dashboard content."""
    st.markdown("# Call Center Analytics Dashboard")
    
    if report_type == "Monthly Report":
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
