"""
Data loader module.
Handles loading and initial processing of call center operational data.
"""
import os
from pathlib import Path
from typing import Optional, Literal

import pandas as pd
import duckdb


class DataLoader:
    """Handles loading and caching of call center data."""

    def __init__(self, data_dir: str = None, period: Literal["monthly", "weekly"] = "monthly"):
        """
        Initialize DataLoader.
        
        Args:
            data_dir: Path to the data directory containing CSV files.
                     If None, uses the data directory in the same location as this file.
            period: The period type for data loading ("monthly" or "weekly")
        """
        if data_dir is None:
            # Use the data directory relative to this file's location
            base_dir = Path(__file__).parent.parent / "data"
        else:
            base_dir = Path(data_dir)
        
        self.period = period
        self.data_dir = base_dir / period
        self._cache = {}

    def set_period(self, period: Literal["monthly", "weekly"]) -> None:
        """
        Change the period and update data directory.
        
        Args:
            period: The period type ("monthly" or "weekly")
        """
        self.period = period
        base_dir = self.data_dir.parent
        self.data_dir = base_dir / period
        self.clear_cache()

    def load_overall_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load overall metrics data.
        
        Args:
            force_reload: Force reload from disk, ignoring cache
            
        Returns:
            DataFrame with overall metrics
        """
        cache_key = f"overall_{self.period}"
        if cache_key in self._cache and not force_reload:
            return self._cache[cache_key]

        overall_file = self.data_dir / "overall.csv"
        if not overall_file.exists():
            raise FileNotFoundError(f"Overall data file not found: {overall_file}")

        df = pd.read_csv(overall_file)
        
        # Parse date columns based on period
        if self.period == "monthly":
            df["month"] = pd.to_datetime(df["month"])
        else:
            df["week_start"] = pd.to_datetime(df["week_start"])
        
        self._cache[cache_key] = df
        return df

    def load_agent_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load agent performance data.
        
        Args:
            force_reload: Force reload from disk, ignoring cache
            
        Returns:
            DataFrame with agent data
        """
        cache_key = f"agent_{self.period}"
        if cache_key in self._cache and not force_reload:
            return self._cache[cache_key]

        agent_file = self.data_dir / "agent.csv"
        if not agent_file.exists():
            raise FileNotFoundError(f"Agent data file not found: {agent_file}")

        df = pd.read_csv(agent_file)
        
        # Parse date columns based on period
        if self.period == "monthly":
            df["month"] = pd.to_datetime(df["month"])
        else:
            df["week_start"] = pd.to_datetime(df["week_start"])
        
        self._cache[cache_key] = df
        return df

    def load_channel_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load channel metrics data.
        
        Args:
            force_reload: Force reload from disk, ignoring cache
            
        Returns:
            DataFrame with channel data
        """
        cache_key = f"channel_{self.period}"
        if cache_key in self._cache and not force_reload:
            return self._cache[cache_key]

        channel_file = self.data_dir / "channel.csv"
        if not channel_file.exists():
            raise FileNotFoundError(f"Channel data file not found: {channel_file}")

        df = pd.read_csv(channel_file)
        
        # Parse date columns based on period
        if self.period == "monthly":
            df["month"] = pd.to_datetime(df["month"])
        else:
            df["week_start"] = pd.to_datetime(df["week_start"])
        
        self._cache[cache_key] = df
        return df

    def load_calls_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load detailed calls data.
        
        Args:
            force_reload: Force reload from disk, ignoring cache
            
        Returns:
            DataFrame with calls data
        """
        cache_key = f"calls_{self.period}"
        if cache_key in self._cache and not force_reload:
            return self._cache[cache_key]

        calls_file = self.data_dir / "calls.csv"
        if not calls_file.exists():
            raise FileNotFoundError(f"Calls data file not found: {calls_file}")

        df = pd.read_csv(calls_file)
        df["date"] = pd.to_datetime(df["date"])
        
        # Parse period-specific date columns
        if self.period == "monthly":
            df["month"] = pd.to_datetime(df["month"])
        else:
            df["week_start"] = pd.to_datetime(df["week_start"])
        
        self._cache[cache_key] = df
        return df

    def clear_cache(self) -> None:
        """Clear the data cache."""
        self._cache.clear()

    def get_date_range(self) -> tuple:
        """
        Get the date range of available data.
        
        Returns:
            Tuple of (min_date, max_date)
        """
        calls_df = self.load_calls_data()
        return calls_df["date"].min(), calls_df["date"].max()

    def get_periods(self) -> pd.DataFrame:
        """
        Get available periods (months or weeks) from overall data.
        Sorted from most recent to oldest.
        
        Returns:
            DataFrame with period information
        """
        overall_df = self.load_overall_data()
        if self.period == "monthly":
            result = overall_df[["month", "month_name"]].copy()
            return result.sort_values("month", ascending=False).reset_index(drop=True)
        else:
            result = overall_df[["week_start"]].copy()
            return result.sort_values("week_start", ascending=False).reset_index(drop=True)

    @staticmethod
    def validate_data_integrity(df: pd.DataFrame, data_type: str) -> bool:
        """
        Validate data integrity for loaded datasets.
        
        Args:
            df: DataFrame to validate
            data_type: Type of data (overall, agent, channel, calls)
            
        Returns:
            True if data is valid
            
        Raises:
            ValueError: If data integrity issues are found
        """
        required_columns = {
            "overall": ["total_interactions", "total_cost"],
            "agent": ["agent_id", "agent_name", "total_interactions"],
            "channel": ["channel", "total_interactions"],
            "calls": ["call_id", "agent_id", "date", "duration_minutes"],
        }

        if data_type not in required_columns:
            raise ValueError(f"Unknown data type: {data_type}")

        missing_cols = set(required_columns[data_type]) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        if df.empty:
            raise ValueError(f"No data found for {data_type}")

        return True
