"""
Data loader module.
Handles loading and initial processing of call center operational data.
"""
import os
from pathlib import Path
from typing import Optional

import pandas as pd
import duckdb


class DataLoader:
    """Handles loading and caching of call center data."""

    def __init__(self, data_dir: str = None):
        """
        Initialize DataLoader.
        
        Args:
            data_dir: Path to the data directory containing CSV files.
                     If None, uses the data directory in the same location as this file.
        """
        if data_dir is None:
            # Use the data directory relative to this file's location
            self.data_dir = Path(__file__).parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
        self._cache = {}

    def load_calls_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load calls operational data.
        
        Args:
            force_reload: Force reload from disk, ignoring cache
            
        Returns:
            DataFrame with calls data
        """
        if "calls" in self._cache and not force_reload:
            return self._cache["calls"]

        calls_file = self.data_dir / "calls.csv"
        if not calls_file.exists():
            raise FileNotFoundError(f"Calls data file not found: {calls_file}")

        df = pd.read_csv(calls_file)
        df["date"] = pd.to_datetime(df["date"])
        df["start_time"] = pd.to_datetime(df["start_time"])
        df["end_time"] = pd.to_datetime(df["end_time"])
        
        self._cache["calls"] = df
        return df

    def load_agents_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load agents information data.
        
        Args:
            force_reload: Force reload from disk, ignoring cache
            
        Returns:
            DataFrame with agents data
        """
        if "agents" in self._cache and not force_reload:
            return self._cache["agents"]

        agents_file = self.data_dir / "agents.csv"
        if not agents_file.exists():
            raise FileNotFoundError(f"Agents data file not found: {agents_file}")

        df = pd.read_csv(agents_file)
        self._cache["agents"] = df
        return df

    def load_costs_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load costs configuration data.
        
        Args:
            force_reload: Force reload from disk, ignoring cache
            
        Returns:
            DataFrame with costs data
        """
        if "costs" in self._cache and not force_reload:
            return self._cache["costs"]

        costs_file = self.data_dir / "costs.csv"
        if not costs_file.exists():
            raise FileNotFoundError(f"Costs data file not found: {costs_file}")

        df = pd.read_csv(costs_file)
        self._cache["costs"] = df
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

    @staticmethod
    def validate_data_integrity(df: pd.DataFrame, data_type: str) -> bool:
        """
        Validate data integrity for loaded datasets.
        
        Args:
            df: DataFrame to validate
            data_type: Type of data (calls, agents, costs)
            
        Returns:
            True if data is valid
            
        Raises:
            ValueError: If data integrity issues are found
        """
        required_columns = {
            "calls": ["call_id", "agent_id", "client_id", "date", "duration_minutes"],
            "agents": ["agent_id", "agent_name", "department"],
            "costs": ["cost_type", "hourly_rate", "amount"],
        }

        if data_type not in required_columns:
            raise ValueError(f"Unknown data type: {data_type}")

        missing_cols = set(required_columns[data_type]) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        if df.empty:
            raise ValueError(f"No data found for {data_type}")

        return True
