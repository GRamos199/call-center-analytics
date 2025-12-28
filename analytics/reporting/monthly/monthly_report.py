"""
Monthly Report Logic Module
Contains all data processing and metrics calculation for monthly reports.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.data_loader import DataLoader
from utils.metric_loader import MetricLoader


class MonthlyReport:
    """Handles all logic for monthly report calculations and data retrieval."""

    def __init__(self):
        """Initialize MonthlyReport with data and metric loaders."""
        self.data_loader = DataLoader(period="monthly")
        self.metric_loader = MetricLoader(self.data_loader)

    def get_available_months(self) -> pd.DataFrame:
        """Get all available months from the data."""
        return self.metric_loader.get_available_periods()

    def get_current_month(self) -> datetime:
        """Get the most recent month available in the data."""
        overall_df = self.data_loader.load_overall_data()
        return overall_df["month"].max()

    def get_previous_month(self, current_month: datetime) -> datetime:
        """Get the month before the given month."""
        overall_df = self.data_loader.load_overall_data()
        months = overall_df["month"].sort_values(ascending=False).unique()
        current_idx = list(months).index(pd.Timestamp(current_month))
        if current_idx + 1 < len(months):
            return months[current_idx + 1]
        return None

    def get_productivity_metrics(self, month_date: datetime = None) -> dict:
        """Get productivity metrics for the given month."""
        return self.metric_loader.calculate_productivity_metrics(month_date)

    def get_deltas(self, current_metrics: dict, previous_metrics: dict) -> dict:
        """Calculate metric deltas between two periods."""
        return self.metric_loader.calculate_deltas(current_metrics, previous_metrics)

    def get_agent_metrics(self, month_date: datetime = None) -> pd.DataFrame:
        """Get cost per agent metrics."""
        return self.metric_loader.calculate_cost_per_agent(month_date)

    def get_channel_metrics(self, month_date: datetime = None) -> pd.DataFrame:
        """Get channel performance metrics."""
        return self.metric_loader.calculate_channel_performance(month_date)

    def get_daily_breakdown(self, month_date: datetime = None) -> pd.DataFrame:
        """Get daily breakdown of calls within the month."""
        return self.metric_loader.get_daily_breakdown(month_date)

    def get_hourly_distribution(self, month_date: datetime = None) -> pd.DataFrame:
        """Get hourly distribution of calls."""
        return self.metric_loader.get_hourly_distribution(month_date)

    def get_trend_data(self, metric_name: str, num_months: int = 12) -> pd.DataFrame:
        """Get trend data for a metric over multiple months."""
        return self.metric_loader.get_trend_data(metric_name, num_months)

    def refresh_data(self):
        """Clear cache and reload data."""
        self.data_loader.clear_cache()
