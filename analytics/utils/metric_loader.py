"""
Metrics loader module.
Handles calculation of KPIs and metrics for call center analytics.
"""

from datetime import datetime, timedelta
from typing import Dict, Literal, Optional, Tuple

import numpy as np
import pandas as pd

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

    def get_overall_metrics(self, period_date: Optional[datetime] = None) -> Dict:
        """
        Get overall metrics for a specific period or all periods.

        Args:
            period_date: Specific period date (month or week_start).
                        If None, returns the most recent period.

        Returns:
            Dictionary with overall metrics
        """
        overall_df = self.data_loader.load_overall_data()

        if period_date is not None:
            period_date = pd.Timestamp(period_date).normalize()
            date_col = "month" if self.data_loader.period == "monthly" else "week_start"
            row = overall_df[overall_df[date_col] == period_date]
            if row.empty:
                return {}
            return row.iloc[0].to_dict()
        else:
            # Return the most recent period
            date_col = "month" if self.data_loader.period == "monthly" else "week_start"
            overall_df = overall_df.sort_values(date_col, ascending=False)
            return overall_df.iloc[0].to_dict()

    def get_agent_metrics(
        self, period_date: Optional[datetime] = None, agent_id: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Get agent metrics for a specific period.

        Args:
            period_date: Specific period date. If None, returns the most recent period.
            agent_id: Specific agent ID. If None, returns all agents.

        Returns:
            DataFrame with agent metrics
        """
        agent_df = self.data_loader.load_agent_data()
        date_col = "month" if self.data_loader.period == "monthly" else "week_start"

        if period_date is not None:
            period_date = pd.Timestamp(period_date).normalize()
            agent_df = agent_df[agent_df[date_col] == period_date]
        else:
            # Get the most recent period
            latest_period = agent_df[date_col].max()
            agent_df = agent_df[agent_df[date_col] == latest_period]

        if agent_id is not None:
            agent_df = agent_df[agent_df["agent_id"] == agent_id]

        return agent_df

    def get_channel_metrics(
        self, period_date: Optional[datetime] = None, channel: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get channel metrics for a specific period.

        Args:
            period_date: Specific period date. If None, returns the most recent period.
            channel: Specific channel. If None, returns all channels.

        Returns:
            DataFrame with channel metrics
        """
        channel_df = self.data_loader.load_channel_data()
        date_col = "month" if self.data_loader.period == "monthly" else "week_start"

        if period_date is not None:
            period_date = pd.Timestamp(period_date).normalize()
            channel_df = channel_df[channel_df[date_col] == period_date]
        else:
            # Get the most recent period
            latest_period = channel_df[date_col].max()
            channel_df = channel_df[channel_df[date_col] == latest_period]

        if channel is not None:
            channel_df = channel_df[channel_df["channel"] == channel]

        return channel_df

    def get_calls_data(self, period_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get detailed calls data for a specific period.

        Args:
            period_date: Specific period date. If None, returns all data.

        Returns:
            DataFrame with calls data
        """
        calls_df = self.data_loader.load_calls_data()
        date_col = "month" if self.data_loader.period == "monthly" else "week_start"

        if period_date is not None:
            period_date = pd.Timestamp(period_date).normalize()
            calls_df = calls_df[calls_df[date_col] == period_date]

        return calls_df

    def calculate_productivity_metrics(
        self, period_date: Optional[datetime] = None
    ) -> Dict:
        """
        Calculate productivity metrics for a period.

        Args:
            period_date: Specific period date. If None, uses the most recent period.

        Returns:
            Dictionary with productivity metrics
        """
        overall = self.get_overall_metrics(period_date)
        agent_df = self.get_agent_metrics(period_date)

        if not overall:
            return {
                "total_interactions": 0,
                "avg_handle_time": 0,
                "avg_wait_time": 0,
                "first_call_resolution_rate": 0,
                "customer_satisfaction_score": 0,
                "total_cost": 0,
                "cost_per_interaction": 0,
                "unique_agents": 0,
                "interactions_per_agent": 0,
            }

        unique_agents = agent_df["agent_id"].nunique() if not agent_df.empty else 0
        interactions_per_agent = (
            overall.get("total_interactions", 0) / unique_agents
            if unique_agents > 0
            else 0
        )

        return {
            "total_interactions": overall.get("total_interactions", 0),
            "total_calls": overall.get("total_calls", 0),
            "total_emails": overall.get("total_emails", 0),
            "total_chats": overall.get("total_chats", 0),
            "total_whatsapp": overall.get("total_whatsapp", 0),
            "avg_handle_time": overall.get("avg_handle_time_minutes", 0),
            "avg_wait_time": overall.get("avg_wait_time_minutes", 0),
            "first_call_resolution_rate": overall.get("first_call_resolution_rate", 0),
            "customer_satisfaction_score": overall.get(
                "customer_satisfaction_score", 0
            ),
            "total_cost": overall.get("total_cost", 0),
            "cost_per_interaction": overall.get("cost_per_interaction", 0),
            "unique_agents": unique_agents,
            "interactions_per_agent": round(interactions_per_agent, 2),
        }

    def calculate_cost_per_agent(
        self, period_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Calculate cost per agent for a given period.

        Args:
            period_date: Specific period date. If None, uses the most recent period.

        Returns:
            DataFrame with cost per agent metrics
        """
        agent_df = self.get_agent_metrics(period_date)

        if agent_df.empty:
            return pd.DataFrame(
                columns=[
                    "agent_id",
                    "agent_name",
                    "department",
                    "total_interactions",
                    "hours_worked",
                    "total_cost",
                    "cost_per_interaction",
                ]
            )

        return agent_df[
            [
                "agent_id",
                "agent_name",
                "department",
                "total_interactions",
                "hours_worked",
                "total_cost",
                "cost_per_interaction",
            ]
        ]

    def calculate_channel_performance(
        self, period_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Calculate channel performance for a given period.

        Args:
            period_date: Specific period date. If None, uses the most recent period.

        Returns:
            DataFrame with channel performance metrics
        """
        channel_df = self.get_channel_metrics(period_date)

        if channel_df.empty:
            return pd.DataFrame(
                columns=[
                    "channel",
                    "total_interactions",
                    "avg_handle_time_minutes",
                    "resolution_rate",
                    "customer_satisfaction_score",
                    "total_cost",
                    "cost_per_interaction",
                ]
            )

        return channel_df[
            [
                "channel",
                "total_interactions",
                "avg_handle_time_minutes",
                "resolution_rate",
                "customer_satisfaction_score",
                "total_cost",
                "cost_per_interaction",
            ]
        ]

    def calculate_deltas(self, current_metrics: Dict, previous_metrics: Dict) -> Dict:
        """
        Calculate deltas (changes) between two periods.

        Args:
            current_metrics: Metrics for current period
            previous_metrics: Metrics for previous period

        Returns:
            Dictionary with delta values and percentages
        """
        deltas = {}

        for key in current_metrics:
            current_val = current_metrics.get(key, 0)
            previous_val = previous_metrics.get(key, 0)

            # Skip non-numeric values
            if not isinstance(current_val, (int, float)) or not isinstance(
                previous_val, (int, float)
            ):
                continue

            if previous_val != 0:
                delta = current_val - previous_val
                delta_pct = (delta / previous_val) * 100
                deltas[key] = {
                    "value": delta,
                    "percentage": round(delta_pct, 2),
                    "trend": "up" if delta > 0 else "down" if delta < 0 else "flat",
                }
            else:
                deltas[key] = {
                    "value": current_val,
                    "percentage": 0,
                    "trend": "flat",
                }

        return deltas

    def get_trend_data(self, metric_name: str, num_periods: int = 12) -> pd.DataFrame:
        """
        Get trend data for a specific metric over multiple periods.

        Args:
            metric_name: Name of the metric to track
            num_periods: Number of periods to include

        Returns:
            DataFrame with period and metric value
        """
        overall_df = self.data_loader.load_overall_data()
        date_col = "month" if self.data_loader.period == "monthly" else "week_start"

        if metric_name not in overall_df.columns:
            return pd.DataFrame()

        # Sort and limit
        overall_df = overall_df.sort_values(date_col, ascending=False).head(num_periods)
        overall_df = overall_df.sort_values(date_col, ascending=True)

        return overall_df[[date_col, metric_name]]

    def get_agent_trend_data(
        self, agent_id: int, metric_name: str, num_periods: int = 12
    ) -> pd.DataFrame:
        """
        Get trend data for a specific agent and metric.

        Args:
            agent_id: Agent ID
            metric_name: Name of the metric to track
            num_periods: Number of periods to include

        Returns:
            DataFrame with period and metric value
        """
        agent_df = self.data_loader.load_agent_data()
        date_col = "month" if self.data_loader.period == "monthly" else "week_start"

        agent_df = agent_df[agent_df["agent_id"] == agent_id]

        if metric_name not in agent_df.columns:
            return pd.DataFrame()

        # Sort and limit
        agent_df = agent_df.sort_values(date_col, ascending=False).head(num_periods)
        agent_df = agent_df.sort_values(date_col, ascending=True)

        return agent_df[[date_col, metric_name]]

    def get_daily_breakdown(
        self, period_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get daily breakdown of calls within a period.

        Args:
            period_date: Specific period date. If None, uses the most recent period.

        Returns:
            DataFrame with daily aggregated metrics
        """
        calls_df = self.get_calls_data(period_date)

        if calls_df.empty:
            return pd.DataFrame()

        daily = (
            calls_df.groupby("date")
            .agg(
                {
                    "call_id": "count",
                    "duration_minutes": ["sum", "mean"],
                    "agent_id": "nunique",
                    "resolved": "sum",
                    "customer_satisfaction": "mean",
                }
            )
            .reset_index()
        )

        daily.columns = [
            "date",
            "total_calls",
            "total_duration",
            "avg_duration",
            "agents_active",
            "calls_resolved",
            "avg_satisfaction",
        ]

        daily["resolution_rate"] = daily["calls_resolved"] / daily["total_calls"]

        return daily

    def get_hourly_distribution(
        self, period_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get hourly distribution of calls within a period.

        Args:
            period_date: Specific period date. If None, uses the most recent period.

        Returns:
            DataFrame with hourly aggregated metrics
        """
        calls_df = self.get_calls_data(period_date)

        if calls_df.empty:
            return pd.DataFrame()

        hourly = (
            calls_df.groupby("hour")
            .agg(
                {
                    "call_id": "count",
                    "duration_minutes": "mean",
                    "resolved": "mean",
                }
            )
            .reset_index()
        )

        hourly.columns = ["hour", "total_calls", "avg_duration", "resolution_rate"]

        return hourly

    def get_available_periods(self) -> pd.DataFrame:
        """
        Get all available periods from the data.

        Returns:
            DataFrame with available periods
        """
        return self.data_loader.get_periods()
