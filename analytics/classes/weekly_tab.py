"""
Weekly tab class module.
Handles rendering and presentation of weekly analytics dashboard.
"""
from datetime import datetime, timedelta
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from classes.base_tab import BaseTab
from reporting.weekly.weekly_report import WeeklyReport


class WeeklyTab(BaseTab):
    """Weekly analytics view - handles rendering and UI presentation only."""

    def __init__(self):
        """Initialize WeeklyTab."""
        super().__init__(title="Weekly Analytics", icon="")
        self.report = WeeklyReport()

    def render(self) -> None:
        """Render the weekly analytics dashboard."""
        self.render_header()

        # Get date ranges from report logic
        current_week_start, current_week_end = self.report.get_current_week_range()
        previous_week_start, previous_week_end = self.report.get_previous_week_range()

        # Date selection UI
        col1, col2 = st.columns(2)
        with col1:
            selected_date = st.date_input(
                "Select Week Starting",
                value=current_week_start,
                key="weekly_date"
            )
            week_start = selected_date - timedelta(days=selected_date.weekday())
            week_end = week_start + timedelta(days=6)

        with col2:
            st.write("")
            st.write("")
            refresh_btn = st.button("Refresh Data", key="weekly_refresh")
            if refresh_btn:
                self.report.refresh_data()
                st.rerun()

        # Get metrics from report logic
        current_metrics = self.report.get_productivity_metrics(week_start, week_end)
        previous_metrics = self.report.get_productivity_metrics(previous_week_start, previous_week_end)
        deltas = self.report.get_deltas(current_metrics, previous_metrics)

        # Render UI components
        self._render_kpi_section(current_metrics, deltas)
        self._render_detailed_metrics(week_start, week_end)
        self._render_charts(week_start, week_end)
        self._render_agent_comparison(week_start, week_end)

    def _render_kpi_section(self, current: dict, deltas: dict) -> None:
        """Render KPI metrics section."""
        st.subheader("Weekly Performance Indicators")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            delta_value = f"{deltas['total_calls']['percentage']:.1f}%" if deltas['total_calls']['percentage'] != 0 else "-"
            st.metric(
                "Total Calls",
                f"{current['total_calls']:,}",
                delta=delta_value
            )

        with col2:
            delta_value = f"{deltas['avg_call_duration']['percentage']:.1f}%" if deltas['avg_call_duration']['percentage'] != 0 else "-"
            st.metric(
                "Avg Duration",
                f"{current['avg_call_duration']:.1f} min",
                delta=delta_value
            )

        with col3:
            delta_value = f"{deltas['unique_agents']['percentage']:.1f}%" if deltas['unique_agents']['percentage'] != 0 else "-"
            st.metric(
                "Active Agents",
                f"{current['unique_agents']:.0f}",
                delta=delta_value
            )

        with col4:
            delta_value = f"{deltas['unique_clients']['percentage']:.1f}%" if deltas['unique_clients']['percentage'] != 0 else "-"
            st.metric(
                "Unique Clients",
                f"{current['unique_clients']:.0f}",
                delta=delta_value
            )

    def _render_detailed_metrics(self, date_from, date_to) -> None:
        """Render detailed weekly metrics."""
        st.subheader("Weekly Breakdown")

        try:
            daily_metrics = self.report.get_daily_metrics(date_from, date_to)

            st.write("**Daily Summary**")
            display_df = daily_metrics.copy()
            display_df["date"] = pd.to_datetime(display_df["date"]).dt.strftime("%a, %b %d")
            display_df["cost"] = display_df["cost"].apply(lambda x: f"${x:,.2f}")
            display_df["avg_duration"] = display_df["avg_duration"].apply(lambda x: f"{x:.1f} min")

            st.dataframe(display_df, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error loading daily metrics: {str(e)}")

    def _render_charts(self, date_from, date_to) -> None:
        """Render visualization charts."""
        st.subheader("Weekly Visualizations")

        try:
            daily_metrics = self.report.get_daily_metrics(date_from, date_to)

            col1, col2 = st.columns(2)

            with col1:
                # Hourly calls distribution by day
                daily_metrics["date_str"] = pd.to_datetime(daily_metrics["date"]).dt.strftime("%a")
                fig = px.bar(
                    daily_metrics,
                    x="date_str",
                    y="total_calls",
                    title="Calls by Day of Week",
                    color="total_calls",
                    color_continuous_scale="Viridis",
                )
                fig.update_layout(
                    xaxis_title="Day",
                    yaxis_title="Total Calls",
                    plot_bgcolor=self.COLORS["light_bg"],
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Average call duration by day
                fig = px.line(
                    daily_metrics,
                    x="date_str",
                    y="avg_duration",
                    title="Average Call Duration by Day",
                    markers=True,
                    color_discrete_sequence=[self.COLORS["secondary"]]
                )
                fig.update_layout(
                    xaxis_title="Day",
                    yaxis_title="Duration (minutes)",
                    plot_bgcolor=self.COLORS["light_bg"],
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error rendering charts: {str(e)}")

    def _render_agent_comparison(self, date_from, date_to) -> None:
        """Render agent comparison metrics."""
        st.subheader("Agent Performance Comparison")

        try:
            agent_metrics = self.report.get_agent_metrics(date_from, date_to)

            if len(agent_metrics) > 0:
                col1, col2 = st.columns(2)

                with col1:
                    # Calls per agent
                    fig = px.bar(
                        agent_metrics.head(8),
                        x="agent_name",
                        y="total_calls",
                        title="Top Agents by Call Volume",
                        color="total_calls",
                        color_continuous_scale="Blues",
                    )
                    fig.update_layout(
                        xaxis_title="Agent",
                        yaxis_title="Total Calls",
                        plot_bgcolor=self.COLORS["light_bg"],
                        showlegend=False,
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Cost per agent
                    fig = px.bar(
                        agent_metrics.head(8),
                        x="agent_name",
                        y="cost",
                        title="Top Agents by Cost",
                        color="cost",
                        color_continuous_scale="Reds",
                    )
                    fig.update_layout(
                        xaxis_title="Agent",
                        yaxis_title="Cost ($)",
                        plot_bgcolor=self.COLORS["light_bg"],
                        showlegend=False,
                    )
                    st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error rendering agent comparison: {str(e)}")
