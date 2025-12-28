"""
Weekly Report Logic Module
Contains all data processing and metrics calculation for weekly reports.
"""
from datetime import datetime, timedelta
import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.data_loader import DataLoader
from utils.metric_loader import MetricLoader


class WeeklyReport:
    """Handles all logic for weekly report calculations and data retrieval."""

    def __init__(self):
        """Initialize WeeklyReport with data and metric loaders."""
        self.data_loader = DataLoader(period="weekly")
        self.metric_loader = MetricLoader(self.data_loader)

    def get_available_weeks(self) -> pd.DataFrame:
        """Get all available weeks from the data."""
        return self.metric_loader.get_available_periods()

    def get_current_week(self) -> datetime:
        """Get the most recent week available in the data."""
        overall_df = self.data_loader.load_overall_data()
        return overall_df["week_start"].max()

    def get_previous_week(self, current_week: datetime) -> datetime:
        """Get the week before the given week."""
        overall_df = self.data_loader.load_overall_data()
        weeks = overall_df["week_start"].sort_values(ascending=False).unique()
        current_idx = list(weeks).index(pd.Timestamp(current_week))
        if current_idx + 1 < len(weeks):
            return weeks[current_idx + 1]
        return None

    def get_productivity_metrics(self, week_date: datetime = None) -> dict:
        """Get productivity metrics for the given week."""
        return self.metric_loader.calculate_productivity_metrics(week_date)

    def get_deltas(self, current_metrics: dict, previous_metrics: dict) -> dict:
        """Calculate metric deltas between two periods."""
        return self.metric_loader.calculate_deltas(current_metrics, previous_metrics)

    def get_agent_metrics(self, week_date: datetime = None) -> pd.DataFrame:
        """Get cost per agent metrics."""
        return self.metric_loader.calculate_cost_per_agent(week_date)

    def get_channel_metrics(self, week_date: datetime = None) -> pd.DataFrame:
        """Get channel performance metrics."""
        return self.metric_loader.calculate_channel_performance(week_date)

    def get_daily_breakdown(self, week_date: datetime = None) -> pd.DataFrame:
        """Get daily breakdown of calls within the week."""
        return self.metric_loader.get_daily_breakdown(week_date)

    def get_hourly_distribution(self, week_date: datetime = None) -> pd.DataFrame:
        """Get hourly distribution of calls."""
        return self.metric_loader.get_hourly_distribution(week_date)

    def get_trend_data(self, metric_name: str, num_weeks: int = 12) -> pd.DataFrame:
        """Get trend data for a metric over multiple weeks."""
        return self.metric_loader.get_trend_data(metric_name, num_weeks)

    def refresh_data(self):
        """Clear cache and reload data."""
        self.data_loader.clear_cache()
