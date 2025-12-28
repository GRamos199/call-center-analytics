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
        super().__init__(title="Weekly Analytics", icon="📆")
        self.report = WeeklyReport()

    def render(self) -> None:
        """Render the weekly analytics dashboard."""
        self.render_header()

        # Get available weeks
        current_week = self.report.get_current_week()
        previous_week = self.report.get_previous_week(current_week)

        # Week selection UI
        col1, col2 = st.columns(2)
        with col1:
            available_weeks = self.report.get_available_weeks()
            week_options = available_weeks["week_start"].dt.strftime("Week of %b %d, %Y").tolist()
            selected_idx = st.selectbox(
                "Select Week",
                range(len(week_options)),
                format_func=lambda x: week_options[x],
                key="weekly_selector"
            )
            selected_week = available_weeks.iloc[selected_idx]["week_start"]

        with col2:
            st.write("")
            st.write("")
            refresh_btn = st.button("🔄 Refresh Data", key="weekly_refresh")
            if refresh_btn:
                self.report.refresh_data()
                st.rerun()

        # Get previous week for comparison
        prev_week = self.report.get_previous_week(selected_week)

        # Get metrics from report logic
        current_metrics = self.report.get_productivity_metrics(selected_week)
        previous_metrics = self.report.get_productivity_metrics(prev_week) if prev_week else {}
        deltas = self.report.get_deltas(current_metrics, previous_metrics)

        # Render UI components
        self._render_kpi_section(current_metrics, deltas)
        self._render_channel_breakdown(selected_week)
        self._render_daily_breakdown(selected_week)
        self._render_agent_comparison(selected_week)

    def _render_kpi_section(self, current: dict, deltas: dict) -> None:
        """Render KPI metrics section."""
        st.subheader("📊 Weekly Performance Indicators")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            delta_val = deltas.get("total_interactions", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "Total Interactions",
                f"{current.get('total_interactions', 0):,}",
                delta=delta_str
            )

        with col2:
            delta_val = deltas.get("avg_handle_time", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "Avg Handle Time",
                f"{current.get('avg_handle_time', 0):.1f} min",
                delta=delta_str,
                delta_color="inverse"
            )

        with col3:
            delta_val = deltas.get("customer_satisfaction_score", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "CSAT Score",
                f"{current.get('customer_satisfaction_score', 0):.2f}/5",
                delta=delta_str
            )

        with col4:
            delta_val = deltas.get("cost_per_interaction", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "Cost/Interaction",
                f"${current.get('cost_per_interaction', 0):.2f}",
                delta=delta_str,
                delta_color="inverse"
            )

        # Second row of metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Calls", f"{current.get('total_calls', 0):,}")

        with col2:
            st.metric("Total Emails", f"{current.get('total_emails', 0):,}")

        with col3:
            st.metric("Total Chats", f"{current.get('total_chats', 0):,}")

        with col4:
            st.metric("Total WhatsApp", f"{current.get('total_whatsapp', 0):,}")

    def _render_channel_breakdown(self, week_date) -> None:
        """Render channel breakdown section."""
        st.subheader("📞 Channel Performance")

        try:
            channel_df = self.report.get_channel_metrics(week_date)
            
            if channel_df.empty:
                st.warning("No channel data available for this period.")
                return

            col1, col2 = st.columns(2)

            with col1:
                # Channel volume bar chart
                fig = px.bar(
                    channel_df,
                    x="channel",
                    y="total_interactions",
                    title="Interactions by Channel",
                    color="channel",
                    color_discrete_sequence=self.CHART_COLORS["palette"]
                )
                fig.update_layout(
                    xaxis_title="Channel",
                    yaxis_title="Interactions",
                    showlegend=False,
                    plot_bgcolor=self.COLORS["light_bg"],
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Channel metrics table
                st.write("**Channel Metrics**")
                display_df = channel_df.copy()
                display_df["resolution_rate"] = (display_df["resolution_rate"] * 100).round(1).astype(str) + "%"
                display_df["avg_handle_time_minutes"] = display_df["avg_handle_time_minutes"].round(1).astype(str) + " min"
                display_df["total_cost"] = display_df["total_cost"].apply(lambda x: f"${x:,.2f}")
                display_df = display_df.rename(columns={
                    "channel": "Channel",
                    "total_interactions": "Interactions",
                    "avg_handle_time_minutes": "Avg Time",
                    "resolution_rate": "Resolution",
                    "customer_satisfaction_score": "CSAT",
                    "total_cost": "Cost"
                })
                st.dataframe(
                    display_df[["Channel", "Interactions", "Avg Time", "Resolution", "CSAT", "Cost"]],
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as e:
            st.error(f"Error loading channel metrics: {str(e)}")

    def _render_daily_breakdown(self, week_date) -> None:
        """Render daily breakdown section."""
        st.subheader("📅 Daily Breakdown")

        try:
            daily_df = self.report.get_daily_breakdown(week_date)

            if daily_df.empty:
                st.warning("No daily data available for this period.")
                return

            col1, col2 = st.columns(2)

            with col1:
                # Daily calls chart
                daily_df["day_name"] = pd.to_datetime(daily_df["date"]).dt.strftime("%a")
                fig = px.bar(
                    daily_df,
                    x="day_name",
                    y="total_calls",
                    title="Calls by Day",
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
                # Resolution rate by day
                fig = px.line(
                    daily_df,
                    x="day_name",
                    y="resolution_rate",
                    title="Resolution Rate by Day",
                    markers=True,
                    color_discrete_sequence=[self.COLORS["secondary"]]
                )
                fig.update_layout(
                    xaxis_title="Day",
                    yaxis_title="Resolution Rate",
                    plot_bgcolor=self.COLORS["light_bg"],
                    yaxis_tickformat=".0%"
                )
                st.plotly_chart(fig, use_container_width=True)

            # Daily summary table
            st.write("**Daily Summary**")
            display_df = daily_df.copy()
            display_df["date"] = pd.to_datetime(display_df["date"]).dt.strftime("%a, %b %d")
            display_df["resolution_rate"] = (display_df["resolution_rate"] * 100).round(1).astype(str) + "%"
            display_df["avg_duration"] = display_df["avg_duration"].round(1).astype(str) + " min"
            display_df["avg_satisfaction"] = display_df["avg_satisfaction"].round(2)
            display_df = display_df.rename(columns={
                "date": "Date",
                "total_calls": "Calls",
                "avg_duration": "Avg Duration",
                "agents_active": "Agents",
                "resolution_rate": "Resolution",
                "avg_satisfaction": "CSAT"
            })
            st.dataframe(
                display_df[["Date", "Calls", "Avg Duration", "Agents", "Resolution", "CSAT"]],
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:
            st.error(f"Error loading daily breakdown: {str(e)}")

    def _render_agent_comparison(self, week_date) -> None:
        """Render agent comparison metrics."""
        st.subheader("👥 Agent Performance")

        try:
            agent_metrics = self.report.get_agent_metrics(week_date)

            if agent_metrics.empty:
                st.warning("No agent data available for this period.")
                return

            col1, col2 = st.columns(2)

            with col1:
                # Interactions per agent
                fig = px.bar(
                    agent_metrics.sort_values("total_interactions", ascending=False).head(8),
                    x="agent_name",
                    y="total_interactions",
                    title="Top Agents by Interactions",
                    color="total_interactions",
                    color_continuous_scale="Blues",
                )
                fig.update_layout(
                    xaxis_title="Agent",
                    yaxis_title="Total Interactions",
                    plot_bgcolor=self.COLORS["light_bg"],
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Cost efficiency
                fig = px.bar(
                    agent_metrics.sort_values("cost_per_interaction").head(8),
                    x="agent_name",
                    y="cost_per_interaction",
                    title="Most Cost-Efficient Agents",
                    color="cost_per_interaction",
                    color_continuous_scale="Greens_r",
                )
                fig.update_layout(
                    xaxis_title="Agent",
                    yaxis_title="Cost per Interaction ($)",
                    plot_bgcolor=self.COLORS["light_bg"],
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)

            # Agent summary table
            st.write("**Agent Summary**")
            display_df = agent_metrics.copy()
            display_df["total_cost"] = display_df["total_cost"].apply(lambda x: f"${x:,.2f}")
            display_df["cost_per_interaction"] = display_df["cost_per_interaction"].apply(lambda x: f"${x:.2f}")
            display_df = display_df.rename(columns={
                "agent_name": "Agent",
                "department": "Dept",
                "total_interactions": "Interactions",
                "hours_worked": "Hours",
                "total_cost": "Cost",
                "cost_per_interaction": "Cost/Int"
            })
            st.dataframe(
                display_df[["Agent", "Dept", "Interactions", "Hours", "Cost", "Cost/Int"]],
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:
            st.error(f"Error loading agent metrics: {str(e)}")
