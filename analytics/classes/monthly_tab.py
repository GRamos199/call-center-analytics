"""
Monthly tab class module.
Handles rendering and presentation of monthly analytics dashboard.
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
from reporting.monthly.monthly_report import MonthlyReport


class MonthlyTab(BaseTab):
    """Monthly analytics view - handles rendering and UI presentation only."""

    def __init__(self):
        """Initialize MonthlyTab."""
        super().__init__(title="Monthly Analytics", icon="")
        self.report = MonthlyReport()

    def render(self) -> None:
        """Render the monthly analytics dashboard."""
        self.render_header()
        
        # Get date ranges from report logic
        current_month_start, current_month_end = self.report.get_current_month_range()
        previous_month_start, previous_month_end = self.report.get_previous_month_range()

        # Date selection UI
        col1, col2 = st.columns(2)
        with col1:
            selected_month = st.date_input(
                "Select Month",
                value=current_month_start,
                key="monthly_date"
            )
            month_start = pd.Timestamp(year=selected_month.year, month=selected_month.month, day=1)
            month_end = (month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        with col2:
            st.write("")
            st.write("")
            refresh_btn = st.button("Refresh Data", key="monthly_refresh")
            if refresh_btn:
                self.report.refresh_data()
                st.rerun()

        # Get metrics from report logic
        current_metrics = self.report.get_productivity_metrics(month_start, month_end)
        previous_metrics = self.report.get_productivity_metrics(previous_month_start, previous_month_end)
        deltas = self.report.get_deltas(current_metrics, previous_metrics)

        # Render UI components
        self._render_kpi_section(current_metrics, deltas)
        self._render_detailed_metrics(month_start, month_end)
        self._render_charts(month_start, month_end)

    def _render_kpi_section(self, current: dict, deltas: dict) -> None:
        """Render KPI metrics section."""
        st.subheader("Key Performance Indicators")
        
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
            delta_value = f"{deltas['calls_per_agent']['percentage']:.1f}%" if deltas['calls_per_agent']['percentage'] != 0 else "-"
            st.metric(
                "Calls/Agent",
                f"{current['calls_per_agent']:.1f}",
                delta=delta_value
            )

    def _render_detailed_metrics(self, date_from, date_to) -> None:
        """Render detailed metrics tables."""
        st.subheader("Agent Metrics")

        try:
            agent_metrics = self.report.get_agent_metrics(date_from, date_to)
            
            col1, col2 = st.columns([2, 2])

            with col1:
                st.write("**Top Performers (by calls)**")
                top_agents = agent_metrics.nlargest(5, "total_calls")[
                    ["agent_name", "total_calls", "hours_worked", "cost"]
                ]
                st.dataframe(top_agents, use_container_width=True, hide_index=True)

            with col2:
                st.write("**Cost Analysis**")
                cost_summary = pd.DataFrame({
                    "Metric": ["Total Cost", "Avg Cost/Agent", "Min Cost", "Max Cost"],
                    "Value": [
                        f"${agent_metrics['cost'].sum():,.2f}",
                        f"${agent_metrics['cost'].mean():,.2f}",
                        f"${agent_metrics['cost'].min():,.2f}",
                        f"${agent_metrics['cost'].max():,.2f}",
                    ]
                })
                st.dataframe(cost_summary, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error loading agent metrics: {str(e)}")

    def _render_charts(self, date_from, date_to) -> None:
        """Render visualization charts."""
        st.subheader("Visualizations")

        try:
            daily_metrics = self.report.get_daily_metrics(date_from, date_to)

            col1, col2 = st.columns(2)

            with col1:
                # Calls trend
                fig = px.line(
                    daily_metrics,
                    x="date",
                    y="total_calls",
                    title="Daily Call Volume",
                    markers=True,
                    color_discrete_sequence=[self.COLORS["primary"]]
                )
                fig.update_layout(
                    hovermode="x unified",
                    plot_bgcolor=self.COLORS["light_bg"],
                    xaxis_title="Date",
                    yaxis_title="Number of Calls",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Cost trend
                fig = px.area(
                    daily_metrics,
                    x="date",
                    y="cost",
                    title="Daily Cost Trend",
                    color_discrete_sequence=[self.COLORS["secondary"]]
                )
                fig.update_layout(
                    hovermode="x unified",
                    plot_bgcolor=self.COLORS["light_bg"],
                    xaxis_title="Date",
                    yaxis_title="Cost ($)",
                )
                st.plotly_chart(fig, use_container_width=True)

            # Agent distribution
            agent_metrics = self.report.get_agent_metrics(date_from, date_to)
            fig = px.bar(
                agent_metrics.head(10),
                x="agent_name",
                y="cost",
                title="Top 10 Agents by Cost",
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
            st.error(f"Error rendering charts: {str(e)}")
