"""
Style Manager module.
Centralizes all CSS styling and page configuration for the Streamlit dashboard.
"""
import streamlit as st


class StyleManager:
    """Manages all styling and theming for the dashboard."""

    # Color scheme - Main project colors
    COLORS = {
        "primary": "#3B82F6",      # Blue
        "secondary": "#F63B83",    # Pink/Magenta
        "accent": "#83F63B",       # Green/Lime
        "primary_hover": "#2563eb",
        "background": "#F2F2F2",
        "text_dark": "#333333",
        "white": "#ffffff",
    }

    # Page configuration
    PAGE_CONFIG = {
        "page_title": "Call Center Analytics",
        "page_icon": "📊",
        "layout": "wide",
        "initial_sidebar_state": "expanded",
    }

    @classmethod
    def setup_page_config(cls) -> None:
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=cls.PAGE_CONFIG["page_title"],
            page_icon=cls.PAGE_CONFIG["page_icon"],
            layout=cls.PAGE_CONFIG["layout"],
            initial_sidebar_state=cls.PAGE_CONFIG["initial_sidebar_state"],
        )

    @classmethod
    def get_main_css(cls) -> str:
        """
        Get the main CSS styles for the application.
        
        Returns:
            CSS string with all main styles.
        """
        return f"""
        <style>
        /* Reduce top padding and margins */
        .main {{
            padding-top: 0rem;
        }}
        
        [data-testid="stAppViewContainer"] {{
            padding-top: 1rem;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {cls.COLORS["background"]};
        }}
        
        /* Sidebar text styling */
        [data-testid="stSidebar"] .css-1d391kg {{
            color: {cls.COLORS["text_dark"]};
        }}
        
        [data-testid="stSidebar"] h2 {{
            color: {cls.COLORS["text_dark"]};
        }}
        
        [data-testid="stSidebar"] p {{
            color: {cls.COLORS["text_dark"]};
        }}
        
        /* Button styling - default state */
        [data-testid="stSidebar"] button {{
            background-color: {cls.COLORS["white"]} !important;
            color: {cls.COLORS["text_dark"]} !important;
            border: 2px solid {cls.COLORS["primary"]} !important;
            font-weight: 500 !important;
        }}
        
        /* Button hover state */
        [data-testid="stSidebar"] button:hover {{
            background-color: {cls.COLORS["primary_hover"]} !important;
            color: {cls.COLORS["white"]} !important;
            border: 2px solid {cls.COLORS["primary_hover"]} !important;
        }}
        
        /* Button active/focus state - when selected */
        [data-testid="stSidebar"] button:active,
        [data-testid="stSidebar"] button:focus {{
            background-color: {cls.COLORS["primary_hover"]} !important;
            color: {cls.COLORS["white"]} !important;
            border: 2px solid {cls.COLORS["primary_hover"]} !important;
        }}
        
        /* Ensure text stays white on pressed/visited buttons */
        [data-testid="stSidebar"] button:focus:not(:focus-visible) {{
            background-color: {cls.COLORS["primary_hover"]} !important;
            color: {cls.COLORS["white"]} !important;
        }}
        
        /* Button text color override for all states */
        [data-testid="stSidebar"] button p,
        [data-testid="stSidebar"] button span,
        [data-testid="stSidebar"] button:hover p,
        [data-testid="stSidebar"] button:hover span,
        [data-testid="stSidebar"] button:active p,
        [data-testid="stSidebar"] button:active span,
        [data-testid="stSidebar"] button:focus p,
        [data-testid="stSidebar"] button:focus span {{
            color: inherit !important;
        }}
        
        /* Metric styling */
        [data-testid="stMetricValue"] {{
            font-size: 32px;
        }}
        
        [data-testid="stMetricLabel"] {{
            font-size: 16px;
        }}
        </style>
        """

    @classmethod
    def apply_styling(cls) -> None:
        """Apply all custom CSS styling to the application."""
        st.markdown(cls.get_main_css(), unsafe_allow_html=True)

    @classmethod
    def setup(cls) -> None:
        """
        Complete setup: configure page and apply all styles.
        Call this method at the start of your app.
        """
        cls.setup_page_config()
        cls.apply_styling()
