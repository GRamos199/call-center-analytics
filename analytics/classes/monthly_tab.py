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
        super().__init__(title="Monthly Analytics", icon="📅")
        self.report = MonthlyReport()

    def render(self) -> None:
        """Render the monthly analytics dashboard."""
        self.render_header()
        
        # Get available months
        current_month = self.report.get_current_month()
        previous_month = self.report.get_previous_month(current_month)

        # Month selection UI
        col1, col2 = st.columns(2)
        with col1:
            available_months = self.report.get_available_months()
            month_options = available_months["month"].dt.strftime("%B %Y").tolist()
            selected_idx = st.selectbox(
                "Select Month",
                range(len(month_options)),
                format_func=lambda x: month_options[x],
                key="monthly_selector"
            )
            selected_month = available_months.iloc[selected_idx]["month"]

        with col2:
            st.write("")
            st.write("")
            refresh_btn = st.button("🔄 Refresh Data", key="monthly_refresh")
            if refresh_btn:
                self.report.refresh_data()
                st.rerun()

        # Get previous month for comparison
        prev_month = self.report.get_previous_month(selected_month)

        # Get metrics from report logic
        current_metrics = self.report.get_productivity_metrics(selected_month)
        previous_metrics = self.report.get_productivity_metrics(prev_month) if prev_month else {}
        deltas = self.report.get_deltas(current_metrics, previous_metrics)

        # Render UI components
        self._render_kpi_section(current_metrics, deltas)
        self._render_channel_breakdown(selected_month)
        self._render_agent_metrics(selected_month)
        self._render_charts(selected_month)

    def _render_kpi_section(self, current: dict, deltas: dict) -> None:
        """Render KPI metrics section."""
        st.subheader("📊 Key Performance Indicators")
        
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
            fcr = current.get("first_call_resolution_rate", 0) * 100
            st.metric("First Call Resolution", f"{fcr:.1f}%")

        with col2:
            st.metric("Total Cost", f"${current.get('total_cost', 0):,.2f}")

        with col3:
            st.metric("Active Agents", f"{current.get('unique_agents', 0)}")

        with col4:
            st.metric("Interactions/Agent", f"{current.get('interactions_per_agent', 0):.0f}")

    def _render_channel_breakdown(self, month_date) -> None:
        """Render channel breakdown section."""
        st.subheader("📞 Channel Performance")

        try:
            channel_df = self.report.get_channel_metrics(month_date)
            
            if channel_df.empty:
                st.warning("No channel data available for this period.")
                return

            col1, col2 = st.columns(2)

            with col1:
                # Channel volume pie chart
                fig = px.pie(
                    channel_df,
                    values="total_interactions",
                    names="channel",
                    title="Interactions by Channel",
                    color_discrete_sequence=self.CHART_COLORS["palette"]
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
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

    def _render_agent_metrics(self, month_date) -> None:
        """Render agent metrics tables."""
        st.subheader("👥 Agent Performance")

        try:
            agent_metrics = self.report.get_agent_metrics(month_date)
            
            if agent_metrics.empty:
                st.warning("No agent data available for this period.")
                return

            col1, col2 = st.columns([2, 2])

            with col1:
                st.write("**Top Performers (by interactions)**")
                top_agents = agent_metrics.nlargest(5, "total_interactions")[
                    ["agent_name", "department", "total_interactions", "hours_worked", "cost_per_interaction"]
                ].copy()
                top_agents["cost_per_interaction"] = top_agents["cost_per_interaction"].apply(lambda x: f"${x:.2f}")
                top_agents = top_agents.rename(columns={
                    "agent_name": "Agent",
                    "department": "Dept",
                    "total_interactions": "Interactions",
                    "hours_worked": "Hours",
                    "cost_per_interaction": "Cost/Int"
                })
                st.dataframe(top_agents, use_container_width=True, hide_index=True)

            with col2:
                st.write("**Cost Summary**")
                cost_summary = pd.DataFrame({
                    "Metric": ["Total Cost", "Avg Cost/Agent", "Min Cost", "Max Cost"],
                    "Value": [
                        f"${agent_metrics['total_cost'].sum():,.2f}",
                        f"${agent_metrics['total_cost'].mean():,.2f}",
                        f"${agent_metrics['total_cost'].min():,.2f}",
                        f"${agent_metrics['total_cost'].max():,.2f}",
                    ]
                })
                st.dataframe(cost_summary, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error loading agent metrics: {str(e)}")

    def _render_charts(self, month_date) -> None:
        """Render visualization charts."""
        st.subheader("📈 Trends & Analysis")

        try:
            # Trend data
            trend_data = self.report.get_trend_data("total_interactions", 12)
            
            if not trend_data.empty:
                col1, col2 = st.columns(2)

                with col1:
                    # Interactions trend
                    fig = px.line(
                        trend_data,
                        x="month",
                        y="total_interactions",
                        title="Monthly Interactions Trend",
                        markers=True,
                        color_discrete_sequence=[self.COLORS["primary"]]
                    )
                    fig.update_layout(
                        hovermode="x unified",
                        plot_bgcolor=self.COLORS["light_bg"],
                        xaxis_title="Month",
                        yaxis_title="Total Interactions",
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Cost trend
                    cost_trend = self.report.get_trend_data("total_cost", 12)
                    if not cost_trend.empty:
                        fig = px.area(
                            cost_trend,
                            x="month",
                            y="total_cost",
                            title="Monthly Cost Trend",
                            color_discrete_sequence=[self.COLORS["secondary"]]
                        )
                        fig.update_layout(
                            hovermode="x unified",
                            plot_bgcolor=self.COLORS["light_bg"],
                            xaxis_title="Month",
                            yaxis_title="Cost ($)",
                        )
                        st.plotly_chart(fig, use_container_width=True)

            # Agent cost distribution
            agent_metrics = self.report.get_agent_metrics(month_date)
            if not agent_metrics.empty:
                fig = px.bar(
                    agent_metrics.sort_values("total_cost", ascending=False).head(10),
                    x="agent_name",
                    y="total_cost",
                    title="Agent Cost Distribution",
                    color="total_cost",
                    color_continuous_scale="Blues",
                )
                fig.update_layout(
                    xaxis_title="Agent",
                    yaxis_title="Total Cost ($)",
                    plot_bgcolor=self.COLORS["light_bg"],
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error rendering charts: {str(e)}")
