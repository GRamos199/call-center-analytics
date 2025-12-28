"""
Base content class for dashboard tab sections.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Literal

import pandas as pd
import streamlit as st


class BaseContent(ABC):
    """Base class for content sections within main tabs."""

    # Color scheme - Main project colors
    COLORS = {
        "primary": "#3B82F6",  # Blue
        "secondary": "#F63B83",  # Pink/Magenta
        "success": "#83F63B",  # Green/Lime
        "warning": "#F6B83B",  # Orange (derived)
        "danger": "#F63B3B",  # Red (derived)
        "info": "#3BF6F6",  # Cyan (derived)
        "light_bg": "#F8F9FA",
        "dark_text": "#2D3436",
        "light_text": "#636E72",
    }

    # Chart color palette - based on 3 main colors
    CHART_COLORS = {
        "palette": [
            "#3B82F6",  # Blue
            "#F63B83",  # Pink/Magenta
            "#83F63B",  # Green/Lime
            "#F6B83B",  # Orange (derived)
            "#3BF6F6",  # Cyan (derived)
            "#B83BF6",  # Purple (derived)
        ],
        "gradient_start": "#3B82F6",
        "gradient_end": "#83F63B",
    }

    def __init__(self, report: Any, period_type: Literal["monthly", "weekly"]):
        """
        Initialize BaseContent.

        Args:
            report: The report instance (MonthlyReport or WeeklyReport)
            period_type: Either "monthly" or "weekly"
        """
        self.report = report
        self.period_type = period_type

    @abstractmethod
    def render(self, selected_period: Any, previous_period: Any = None) -> None:
        """
        Render the content section.

        Args:
            selected_period: The currently selected period date
            previous_period: The previous period for comparison (optional)
        """
        pass

    def get_period_column(self) -> str:
        """Get the period column name based on period type."""
        return "month" if self.period_type == "monthly" else "week_start"

    def format_currency(self, value: float) -> str:
        """Format a value as currency."""
        return f"${value:,.2f}"

    def format_percentage(self, value: float, multiply: bool = True) -> str:
        """Format a value as percentage."""
        if multiply:
            return f"{value * 100:.1f}%"
        return f"{value:.1f}%"

    def format_number(self, value: float, decimals: int = 0) -> str:
        """Format a number with thousand separators."""
        if decimals == 0:
            return f"{int(value):,}"
        return f"{value:,.{decimals}f}"

    def _render_tab_header(
        self, icon: str, title: str, subtitle: str, color: str
    ) -> None:
        """Render an animated tab header matching main header style."""
        period_label = "Monthly" if self.period_type == "monthly" else "Weekly"
        # Use secondary color for gradient end
        color2 = (
            self.COLORS["secondary"]
            if color != self.COLORS["secondary"]
            else self.COLORS["primary"]
        )
        header_html = f"""
<style>
.tab-header-{title.replace(' ', '-').lower()} {{
    position: relative;
    background: linear-gradient(135deg, {color} 0%, {color2} 100%);
    border-radius: 10px;
    padding: 12px 20px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 4px 15px {color}40;
}}
.tab-header-{title.replace(' ', '-').lower()}::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    animation: tab-shimmer-{title.replace(' ', '-').lower()} 3s infinite linear;
}}
@keyframes tab-shimmer-{title.replace(' ', '-').lower()} {{
    0% {{ transform: translateX(-100%) rotate(45deg); }}
    100% {{ transform: translateX(100%) rotate(45deg); }}
}}
.tab-header-content-{title.replace(' ', '-').lower()} {{
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.tab-icon-{title.replace(' ', '-').lower()} {{
    font-size: 24px;
    animation: bounce-tab-{title.replace(' ', '-').lower()} 2s ease-in-out infinite;
}}
@keyframes bounce-tab-{title.replace(' ', '-').lower()} {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-3px); }}
}}
.tab-title-{title.replace(' ', '-').lower()} {{
    font-size: 16px;
    font-weight: 700;
    color: white;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    margin: 0;
}}
.tab-subtitle-{title.replace(' ', '-').lower()} {{
    font-size: 11px;
    color: rgba(255,255,255,0.85);
    margin-top: 2px;
}}
.tab-dots-{title.replace(' ', '-').lower()} {{
    display: flex;
    gap: 6px;
    margin-left: auto;
}}
.tab-dot-{title.replace(' ', '-').lower()} {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255,255,255,0.6);
    animation: float-dot-{title.replace(' ', '-').lower()} 1.5s ease-in-out infinite;
}}
.tab-dot-{title.replace(' ', '-').lower()}:nth-child(2) {{ animation-delay: 0.2s; }}
.tab-dot-{title.replace(' ', '-').lower()}:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes float-dot-{title.replace(' ', '-').lower()} {{
    0%, 100% {{ transform: translateY(0); opacity: 0.6; }}
    50% {{ transform: translateY(-4px); opacity: 1; }}
}}
.tab-bubble-{title.replace(' ', '-').lower()} {{
    position: absolute;
    border-radius: 50%;
    background: rgba(255,255,255,0.2);
    animation: pulse-tab-{title.replace(' ', '-').lower()} 3s ease-in-out infinite;
}}
.tab-bubble-1-{title.replace(' ', '-').lower()} {{ width: 40px; height: 40px; top: -15px; right: -10px; }}
.tab-bubble-2-{title.replace(' ', '-').lower()} {{ width: 25px; height: 25px; bottom: -10px; right: 15%; animation-delay: 1s; }}
@keyframes pulse-tab-{title.replace(' ', '-').lower()} {{
    0%, 100% {{ transform: scale(1); opacity: 0.2; }}
    50% {{ transform: scale(1.1); opacity: 0.35; }}
}}
</style>
<div class="tab-header-{title.replace(' ', '-').lower()}">
<div class="tab-bubble-{title.replace(' ', '-').lower()} tab-bubble-1-{title.replace(' ', '-').lower()}"></div>
<div class="tab-bubble-{title.replace(' ', '-').lower()} tab-bubble-2-{title.replace(' ', '-').lower()}"></div>
<div class="tab-header-content-{title.replace(' ', '-').lower()}">
<span class="tab-icon-{title.replace(' ', '-').lower()}">{icon}</span>
<div>
<h3 class="tab-title-{title.replace(' ', '-').lower()}">{period_label} {title}</h3>
<p class="tab-subtitle-{title.replace(' ', '-').lower()}">{subtitle}</p>
</div>
<div class="tab-dots-{title.replace(' ', '-').lower()}">
<div class="tab-dot-{title.replace(' ', '-').lower()}"></div>
<div class="tab-dot-{title.replace(' ', '-').lower()}"></div>
<div class="tab-dot-{title.replace(' ', '-').lower()}"></div>
</div>
</div>
</div>
"""
        st.markdown(header_html, unsafe_allow_html=True)
