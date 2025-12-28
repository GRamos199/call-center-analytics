"""
Base tab class module.
Defines the structure and styling for dashboard tabs.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

import streamlit as st


class BaseTab(ABC):
    """Abstract base class for dashboard tabs."""

    # Color scheme (using Streamlit compatible colors)
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

    def __init__(self, title: str, icon: str = "📊"):
        """
        Initialize BaseTab.

        Args:
            title: Tab title
            icon: Tab icon
        """
        self.title = title
        self.icon = icon

    @abstractmethod
    def render(self) -> None:
        """Render the tab content. Must be implemented by subclasses."""
        pass

    def render_header(self) -> None:
        """Render tab header with title and icon."""
        st.markdown(f"## {self.icon} {self.title}")
        st.divider()

    def render_metric(
        self,
        label: str,
        value: Any,
        delta: float = None,
        icon: str = "📊",
        format_string: str = None,
    ) -> None:
        """
        Render a metric card.

        Args:
            label: Metric label
            value: Metric value
            delta: Delta value for trend indicator
            icon: Metric icon
            format_string: Format string for value
        """
        col1, col2 = st.columns([3, 1])

        with col1:
            formatted_value = self._format_value(value, format_string)
            st.metric(label, formatted_value, delta=delta)

        with col2:
            st.markdown(
                f"<div style='font-size: 2em; text-align: center;'>{icon}</div>",
                unsafe_allow_html=True,
            )

    @staticmethod
    def _format_value(value: Any, format_string: str = None) -> str:
        """
        Format a value for display.

        Args:
            value: Value to format
            format_string: Format string (e.g., '.2f' for currency)

        Returns:
            Formatted value
        """
        if format_string is None:
            return str(value)

        if isinstance(value, (int, float)):
            if format_string == "currency":
                return f"${value:,.2f}"
            elif format_string == "percentage":
                return f"{value:.2f}%"
            elif format_string == "hours":
                return f"{value:.1f}h"
            else:
                return format(value, format_string)

        return str(value)

    def render_divider(self) -> None:
        """Render a visual divider."""
        st.divider()

    def render_success_message(self, message: str) -> None:
        """Render a success message."""
        st.success(message)

    def render_warning_message(self, message: str) -> None:
        """Render a warning message."""
        st.warning(message)

    def render_error_message(self, message: str) -> None:
        """Render an error message."""
        st.error(message)

    def render_info_message(self, message: str) -> None:
        """Render an info message."""
        st.info(message)
