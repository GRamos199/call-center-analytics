"""
Monthly Report Logic Module
Contains all data processing and metrics calculation for monthly reports.
"""
from datetime import datetime, timedelta
import sys
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
        self.data_loader = DataLoader()
        self.metric_loader = MetricLoader(self.data_loader)

    def get_current_month_range(self) -> tuple:
        """Get the current month date range."""
        today = datetime.now()
        month_start = datetime(year=today.year, month=today.month, day=1)
        month_end = (month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        return month_start, month_end

    def get_previous_month_range(self) -> tuple:
        """Get the previous month date range."""
        today = datetime.now()
        month_start = datetime(year=today.year, month=today.month, day=1)
        previous_month_end = month_start - timedelta(days=1)
        previous_month_start = datetime(
            year=previous_month_end.year,
            month=previous_month_end.month,
            day=1
        )
        return previous_month_start, previous_month_end

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
