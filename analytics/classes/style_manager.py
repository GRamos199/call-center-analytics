"""
Style Manager module.
Centralizes all CSS styling and page configuration for the Streamlit dashboard.
"""

import streamlit as st


class StyleManager:
    """Manages all styling and theming for the dashboard."""

    # Color scheme - Main project colors
    COLORS = {
        "primary": "#3B82F6",  # Blue
        "secondary": "#F63B83",  # Pink/Magenta
        "accent": "#83F63B",  # Green/Lime
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
        /* ========== MAIN LAYOUT ========== */
        .main {{
            padding-top: 0rem;
        }}
        
        [data-testid="stAppViewContainer"] {{
            padding-top: 0.5rem;
        }}
        
        /* Reduce block container padding */
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }}
        
        /* ========== SIDEBAR STYLING ========== */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        }}
        
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 0 !important;
        }}
        
        /* Sidebar text styling */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            color: white !important;
            text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }}
        
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] li,
        [data-testid="stSidebar"] span {{
            color: rgba(255, 255, 255, 0.85) !important;
        }}
        
        [data-testid="stSidebar"] strong {{
            color: {cls.COLORS["primary"]} !important;
        }}
        
        /* Sidebar divider */
        [data-testid="stSidebar"] hr {{
            border-color: rgba(255, 255, 255, 0.1) !important;
            margin: 1rem 0 !important;
        }}
        
        /* ========== SIDEBAR BUTTONS ========== */
        [data-testid="stSidebar"] button {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(246, 59, 131, 0.1) 100%) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 12px 20px !important;
            margin-bottom: 8px !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        [data-testid="stSidebar"] button:hover {{
            background: linear-gradient(135deg, {cls.COLORS["primary"]} 0%, {cls.COLORS["secondary"]} 100%) !important;
            color: white !important;
            border: 1px solid transparent !important;
            transform: translateX(5px);
            box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4) !important;
        }}
        
        [data-testid="stSidebar"] button:active,
        [data-testid="stSidebar"] button:focus {{
            background: linear-gradient(135deg, {cls.COLORS["primary"]} 0%, {cls.COLORS["secondary"]} 100%) !important;
            color: white !important;
            box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4) !important;
        }}
        
        [data-testid="stSidebar"] button p,
        [data-testid="stSidebar"] button span {{
            color: white !important;
        }}
        
        /* ========== SIDEBAR SELECTBOX ========== */
        [data-testid="stSidebar"] [data-testid="stSelectbox"] {{
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
            padding: 5px !important;
        }}
        
        [data-testid="stSidebar"] [data-testid="stSelectbox"] label {{
            color: rgba(255, 255, 255, 0.9) !important;
        }}
        
        /* ========== METRIC CARDS ========== */
        [data-testid="stMetricValue"] {{
            font-size: 28px !important;
            font-weight: 700 !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            font-size: 14px !important;
            font-weight: 500 !important;
        }}
        
        [data-testid="stMetricDelta"] {{
            font-size: 12px !important;
        }}
        
        /* ========== TABS STYLING ========== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: linear-gradient(90deg, rgba(59, 130, 246, 0.05), rgba(246, 59, 131, 0.05), rgba(131, 246, 59, 0.05));
            border-radius: 12px;
            padding: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px !important;
            padding: 10px 20px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background: rgba(59, 130, 246, 0.1) !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {cls.COLORS["primary"]}, {cls.COLORS["secondary"]}) !important;
            color: white !important;
        }}
        
        /* ========== CARDS & CONTAINERS ========== */
        [data-testid="stExpander"] {{
            border: 1px solid rgba(59, 130, 246, 0.2) !important;
            border-radius: 12px !important;
            background: rgba(59, 130, 246, 0.02) !important;
        }}
        
        [data-testid="stExpander"]:hover {{
            border-color: {cls.COLORS["primary"]} !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1) !important;
        }}
        
        /* ========== DATAFRAMES ========== */
        [data-testid="stDataFrame"] {{
            border-radius: 12px !important;
            overflow: hidden !important;
        }}
        
        /* ========== SCROLLBAR ========== */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.05);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {cls.COLORS["primary"]}, {cls.COLORS["secondary"]});
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, {cls.COLORS["secondary"]}, {cls.COLORS["accent"]});
        }}
        
        /* ========== ANIMATIONS ========== */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .element-container {{
            animation: fadeIn 0.3s ease-out;
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
