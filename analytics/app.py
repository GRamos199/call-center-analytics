"""
Call Center Analytics Dashboard
Main application entry point for the Streamlit dashboard.
"""
import streamlit as st
from pathlib import Path
import sys
import os

# Set working directory to the analytics folder
analytics_dir = Path(__file__).parent
os.chdir(analytics_dir)

# Add analytics to path
sys.path.insert(0, str(analytics_dir))

from classes.monthly_tab import MonthlyTab
from classes.weekly_tab import WeeklyTab


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Call Center Analytics",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def setup_styling():
    """Apply custom CSS styling with blue sidebar."""
    st.markdown("""
    <style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1e3a8a;
    }
    
    /* Sidebar text styling */
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    [data-testid="stSidebar"] h2 {
        color: white;
    }
    
    [data-testid="stSidebar"] p {
        color: white;
    }
    
    [data-testid="stSidebar"] button {
        background-color: #3b82f6;
        color: white;
        border: none;
    }
    
    [data-testid="stSidebar"] button:hover {
        background-color: #2563eb;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 32px;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar navigation and settings."""
    st.sidebar.title("Call Center Analytics")
    st.sidebar.markdown("---")
    
    # Report selection
    report_type = st.sidebar.radio(
        "Select Report",
        options=["Monthly Report", "Weekly Report"],
        index=0,
    )
    
    st.sidebar.markdown("---")
    
    # Data refresh option
    if st.sidebar.button("Refresh All Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
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
    
    return report_type


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
    setup_page_config()
    setup_styling()
    report_type = render_sidebar()
    render_main_dashboard(report_type)


if __name__ == "__main__":
    main()
