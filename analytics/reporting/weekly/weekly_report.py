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
        self.data_loader = DataLoader()
        self.metric_loader = MetricLoader(self.data_loader)

    def get_current_week_range(self) -> tuple:
        """Get the current week date range (Monday to Sunday)."""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        return week_start, week_end

    def get_previous_week_range(self) -> tuple:
        """Get the previous week date range."""
        current_start, _ = self.get_current_week_range()
        week_end = current_start - timedelta(days=1)
        week_start = week_end - timedelta(days=6)
        return week_start, week_end

    def get_productivity_metrics(self, date_from, date_to) -> dict:
        """Get productivity metrics for the given date range."""
        return self.metric_loader.calculate_productivity_metrics(date_from, date_to)

    def get_deltas(self, current_period, previous_period) -> dict:
        """Calculate metric deltas between two periods."""
        return self.metric_loader.calculate_deltas(current_period, previous_period)

    def get_agent_metrics(self, date_from, date_to) -> pd.DataFrame:
        """Get cost per agent metrics."""
        return self.metric_loader.calculate_cost_per_agent(date_from, date_to)

    def get_daily_metrics(self, date_from, date_to) -> pd.DataFrame:
        """Get daily aggregated metrics."""
        return self.metric_loader.get_daily_metrics(date_from, date_to)

    def refresh_data(self):
        """Clear cache and reload data."""
        self.data_loader.clear_cache()
