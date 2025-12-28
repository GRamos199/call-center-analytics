"""
Base content class for dashboard tab sections.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Literal
import streamlit as st
import pandas as pd


class BaseContent(ABC):
    """Base class for content sections within main tabs."""

    # Color scheme
    COLORS = {
        "primary": "#FF6B6B",
        "secondary": "#4ECDC4",
        "success": "#95E1D3",
        "warning": "#FFD93D",
        "danger": "#FF6B6B",
        "info": "#6C5CE7",
        "light_bg": "#F8F9FA",
        "dark_text": "#2D3436",
        "light_text": "#636E72",
    }

    # Chart color palette
    CHART_COLORS = {
        "palette": [
            "#FF6B6B",
            "#4ECDC4",
            "#45B7D1",
            "#96CEB4",
            "#FFEAA7",
            "#DDA15E",
            "#BC6C25",
        ],
        "gradient_start": "#FF6B6B",
        "gradient_end": "#4ECDC4",
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
