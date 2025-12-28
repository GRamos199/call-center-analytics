"""
Metrics loader module.
Handles calculation of KPIs and metrics for call center analytics.
"""
from typing import Dict, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from .data_loader import DataLoader


class MetricLoader:
    """Calculates and manages call center metrics."""

    def __init__(self, data_loader: DataLoader):
        """
        Initialize MetricLoader.
        
        Args:
            data_loader: DataLoader instance for accessing data
        """
        self.data_loader = data_loader

    def calculate_cost_per_agent(self, date_from, date_to) -> pd.DataFrame:
        """
        Calculate cost per agent for a given date range.
        
        Args:
            date_from: Start date (datetime, date, or Timestamp)
            date_to: End date (datetime, date, or Timestamp)
            
        Returns:
            DataFrame with cost per agent
        """
        # Convert to pandas Timestamp and normalize for proper comparison
        date_from = pd.Timestamp(date_from).normalize()
        date_to = pd.Timestamp(date_to).normalize() + timedelta(days=1)
        
        calls_df = self.data_loader.load_calls_data()
        agents_df = self.data_loader.load_agents_data()
        costs_df = self.data_loader.load_costs_data()
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(calls_df["date"]):
            calls_df["date"] = pd.to_datetime(calls_df["date"])

        # Filter by date range
        calls_filtered = calls_df[
            (calls_df["date"] >= date_from) & (calls_df["date"] < date_to)
        ].copy()

        # Get average hourly rate
        hourly_rate = costs_df[costs_df["cost_type"] == "hourly_rate"]["amount"].mean()

        # Group by agent and calculate metrics
        agent_metrics = calls_filtered.groupby("agent_id").agg({
            "call_id": "count",
            "duration_minutes": ["sum", "mean"],
        }).reset_index()

        agent_metrics.columns = ["agent_id", "total_calls", "total_duration_minutes", "avg_call_duration"]

        # Calculate hours worked and cost
        agent_metrics["hours_worked"] = agent_metrics["total_duration_minutes"] / 60
        agent_metrics["cost"] = agent_metrics["hours_worked"] * hourly_rate

        # Merge with agent names
        agent_metrics = agent_metrics.merge(agents_df[["agent_id", "agent_name"]], on="agent_id")

        return agent_metrics[["agent_id", "agent_name", "total_calls", "hours_worked", "cost"]]

    def calculate_cost_per_client(self, date_from: datetime, date_to: datetime) -> pd.DataFrame:
        """
        Calculate cost per client for a given date range.
        
        Args:
            date_from: Start date
            date_to: End date
            
        Returns:
            DataFrame with cost per client
        """
        # Convert to pandas Timestamp and normalize for proper comparison
        date_from = pd.Timestamp(date_from).normalize()
        date_to = pd.Timestamp(date_to).normalize() + timedelta(days=1)
        
        calls_df = self.data_loader.load_calls_data()
        costs_df = self.data_loader.load_costs_data()
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(calls_df["date"]):
            calls_df["date"] = pd.to_datetime(calls_df["date"])

        # Filter by date range
        calls_filtered = calls_df[
            (calls_df["date"] >= date_from) & (calls_df["date"] < date_to)
        ].copy()

        # Get average hourly rate
        hourly_rate = costs_df[costs_df["cost_type"] == "hourly_rate"]["amount"].mean()

        # Group by client and calculate metrics
        client_metrics = calls_filtered.groupby("client_id").agg({
            "call_id": "count",
            "duration_minutes": "sum",
        }).reset_index()

        client_metrics.columns = ["client_id", "total_calls", "total_duration_minutes"]

        # Calculate cost
        client_metrics["hours_used"] = client_metrics["total_duration_minutes"] / 60
        client_metrics["cost_per_client"] = client_metrics["hours_used"] * hourly_rate

        return client_metrics

    def calculate_productivity_metrics(self, date_from: datetime, date_to: datetime) -> Dict:
        """
        Calculate productivity metrics.
        
        Args:
            date_from: Start date
            date_to: End date
            
        Returns:
            Dictionary with productivity metrics
        """
        # Convert to pandas Timestamp and normalize to midnight for proper comparison
        date_from = pd.Timestamp(date_from).normalize()
        date_to = pd.Timestamp(date_to).normalize() + timedelta(days=1)
        
        calls_df = self.data_loader.load_calls_data()
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(calls_df["date"]):
            calls_df["date"] = pd.to_datetime(calls_df["date"])
        
        # Filter by date range
        calls_filtered = calls_df[
            (calls_df["date"] >= date_from) & (calls_df["date"] < date_to)
        ].copy()

        unique_agents = calls_filtered["agent_id"].nunique() if len(calls_filtered) > 0 else 0
        
        # Avoid division by zero
        calls_per_agent = len(calls_filtered) / unique_agents if unique_agents > 0 else 0

        metrics = {
            "total_calls": len(calls_filtered),
            "avg_call_duration": calls_filtered["duration_minutes"].mean() if len(calls_filtered) > 0 else 0,
            "total_call_minutes": calls_filtered["duration_minutes"].sum() if len(calls_filtered) > 0 else 0,
            "unique_agents": unique_agents,
            "unique_clients": calls_filtered["client_id"].nunique() if len(calls_filtered) > 0 else 0,
            "calls_per_agent": calls_per_agent,
        }

        return metrics

    def calculate_deltas(
        self, 
        current_period: Dict, 
        previous_period: Dict
    ) -> Dict:
        """
        Calculate deltas (changes) between two periods.
        
        Args:
            current_period: Metrics for current period
            previous_period: Metrics for previous period
            
        Returns:
            Dictionary with delta values and percentages
        """
        deltas = {}

        for key in current_period:
            if key in previous_period and previous_period[key] != 0:
                delta = current_period[key] - previous_period[key]
                delta_pct = (delta / previous_period[key]) * 100
                deltas[key] = {
                    "value": delta,
                    "percentage": delta_pct,
                    "trend": "up" if delta > 0 else "down" if delta < 0 else "flat",
                }
            else:
                deltas[key] = {
                    "value": current_period.get(key, 0),
                    "percentage": 0,
                    "trend": "flat",
                }

        return deltas

    def get_daily_metrics(self, date_from, date_to) -> pd.DataFrame:
        """
        Get daily aggregated metrics.
        
        Args:
            date_from: Start date (datetime, date, or Timestamp)
            date_to: End date (datetime, date, or Timestamp)
            
        Returns:
            DataFrame with daily metrics
        """
        # Convert to pandas Timestamp and normalize for proper comparison
        date_from = pd.Timestamp(date_from).normalize()
        date_to = pd.Timestamp(date_to).normalize() + timedelta(days=1)
        
        calls_df = self.data_loader.load_calls_data()
        costs_df = self.data_loader.load_costs_data()
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(calls_df["date"]):
            calls_df["date"] = pd.to_datetime(calls_df["date"])

        # Filter by date range
        calls_filtered = calls_df[
            (calls_df["date"] >= date_from) & (calls_df["date"] < date_to)
        ].copy()

        # Get hourly rate
        hourly_rate = costs_df[costs_df["cost_type"] == "hourly_rate"]["amount"].mean()

        # Group by date
        daily_metrics = calls_filtered.groupby(calls_filtered["date"].dt.date).agg({
            "call_id": "count",
            "duration_minutes": ["sum", "mean"],
            "agent_id": "nunique",
            "client_id": "nunique",
        }).reset_index()

        daily_metrics.columns = [
            "date", "total_calls", "total_duration_minutes", 
            "avg_duration", "agents_active", "unique_clients"
        ]

        # Calculate cost
        daily_metrics["cost"] = (daily_metrics["total_duration_minutes"] / 60) * hourly_rate

        return daily_metrics

    def get_agent_daily_metrics(self, agent_id: int, date_from, date_to) -> pd.DataFrame:
        """
        Get daily metrics for a specific agent.
        
        Args:
            agent_id: Agent ID
            date_from: Start date (datetime, date, or Timestamp)
            date_to: End date (datetime, date, or Timestamp)
            
        Returns:
            DataFrame with agent daily metrics
        """
        # Convert to pandas Timestamp and normalize for proper comparison
        date_from = pd.Timestamp(date_from).normalize()
        date_to = pd.Timestamp(date_to).normalize() + timedelta(days=1)
        
        calls_df = self.data_loader.load_calls_data()
        costs_df = self.data_loader.load_costs_data()
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(calls_df["date"]):
            calls_df["date"] = pd.to_datetime(calls_df["date"])

        # Filter by agent and date range
        calls_filtered = calls_df[
            (calls_df["agent_id"] == agent_id) &
            (calls_df["date"] >= date_from) & 
            (calls_df["date"] < date_to)
        ].copy()

        # Get hourly rate
        hourly_rate = costs_df[costs_df["cost_type"] == "hourly_rate"]["amount"].mean()

        # Group by date
        daily_metrics = calls_filtered.groupby(calls_filtered["date"].dt.date).agg({
            "call_id": "count",
            "duration_minutes": ["sum", "mean"],
            "client_id": "nunique",
        }).reset_index()

        daily_metrics.columns = [
            "date", "calls", "total_duration", "avg_duration", "unique_clients"
        ]

        # Calculate cost
        daily_metrics["cost"] = (daily_metrics["total_duration"] / 60) * hourly_rate

        return daily_metrics
