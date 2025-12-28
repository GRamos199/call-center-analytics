"""
Base content class for dashboard tab sections.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Literal
import streamlit as st
import pandas as pd


class BaseContent(ABC):
    """Base class for content sections within main tabs."""

    # Color scheme - Main project colors
    COLORS = {
        "primary": "#3B82F6",      # Blue
        "secondary": "#F63B83",    # Pink/Magenta
        "success": "#83F63B",      # Green/Lime
        "warning": "#F6B83B",      # Orange (derived)
        "danger": "#F63B3B",       # Red (derived)
        "info": "#3BF6F6",         # Cyan (derived)
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
