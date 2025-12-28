"""
Agent Performance content tab.
Displays agent-specific metrics and comparisons.
"""

from typing import Any, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from .base_content import BaseContent


class AgentContent(BaseContent):
    """Renders agent performance metrics and visualizations."""

    def _get_date_column(self) -> str:
        """Get the appropriate date column based on period type."""
        return "month" if self.period_type == "monthly" else "week_start"

    def _get_period_label(self, df: pd.DataFrame) -> str:
        """Get the period label column, creating it if necessary for weekly data."""
        if self.period_type == "monthly":
            return "month_name"
        else:
            if "week_label" not in df.columns:
                df["week_label"] = df["week_start"].dt.strftime("%b %d %Y")
            return "week_label"

    def render(self, selected_period: Any, previous_period: Any = None) -> None:
        """Render the agent performance content."""
        self._render_tab_header(
            "👥",
            "Agent Performance",
            "Individual agent metrics and efficiency rankings",
            self.COLORS["warning"],
        )
        try:
            # Load all agent data
            agent_df = self.report.data_loader.load_agent_data()

            if agent_df.empty:
                st.warning("No agent data available.")
                return

            # Add period label for weekly data
            date_col = self._get_date_column()
            if self.period_type == "weekly":
                agent_df["week_label"] = agent_df["week_start"].dt.strftime("%b %d %Y")

            # Filter to last 12 periods
            recent_periods = agent_df[date_col].drop_duplicates().nlargest(12)
            agent_df = agent_df[agent_df[date_col].isin(recent_periods)]

            # Agent filter
            selected_agent = self._render_agent_filter(agent_df)

            # Filter data by agent if selected
            filtered_df = self._filter_by_agent(agent_df, selected_agent)

            # Get latest period for default table view
            latest_period = filtered_df[date_col].max()

            # Render components
            self._render_agent_table(filtered_df, selected_period, latest_period)
            self._render_department_donuts(filtered_df, selected_period, latest_period)
            self._render_efficiency_rankings(
                filtered_df, selected_period, latest_period
            )

        except Exception as e:
            st.error(f"Error loading agent data: {str(e)}")

    def _render_agent_filter(self, agent_df: pd.DataFrame) -> str:
        """Render agent filter dropdown."""
        agents = ["All Agents"] + sorted(agent_df["agent_name"].unique().tolist())

        selected_agent = st.selectbox(
            "Filter by Agent", options=agents, index=0, key="agent_performance_filter"
        )

        return selected_agent

    def _filter_by_agent(
        self, agent_df: pd.DataFrame, selected_agent: str
    ) -> pd.DataFrame:
        """Filter agent data by selected agent."""
        if selected_agent == "All Agents":
            return agent_df
        return agent_df[agent_df["agent_name"] == selected_agent]

    def _get_period_data(
        self, df: pd.DataFrame, selected_period: Any, latest_period: Any
    ) -> pd.DataFrame:
        """Get data for the selected period or latest period."""
        date_col = self._get_date_column()
        # Use selected_period if available, otherwise use latest
        if selected_period is not None:
            period_df = df[df[date_col] == selected_period]
            if not period_df.empty:
                return period_df
        # Fall back to latest period
        return df[df[date_col] == latest_period]

    def _render_agent_table(
        self, agent_df: pd.DataFrame, selected_period: Any, latest_period: Any
    ) -> None:
        """Render table chart with agent data."""
        # Get data for the period
        period_df = self._get_period_data(agent_df, selected_period, latest_period)

        if period_df.empty:
            st.warning("No data available for the selected period.")
            return

        # Prepare display dataframe
        display_df = period_df.copy()
        label_col = self._get_period_label(display_df)
        period_header = "Month" if self.period_type == "monthly" else "Week"

        # Select and rename columns
        display_df = display_df[
            [
                label_col,
                "agent_name",
                "department",
                "total_interactions",
                "avg_handle_time_minutes",
                "resolution_rate",
                "customer_satisfaction_score",
                "hours_worked",
                "total_cost",
            ]
        ].copy()

        # Format columns
        display_df["resolution_rate"] = (display_df["resolution_rate"] * 100).round(
            2
        ).astype(str) + "%"
        display_df["avg_handle_time_minutes"] = (
            display_df["avg_handle_time_minutes"].round(1).astype(str) + " min"
        )
        display_df["customer_satisfaction_score"] = display_df[
            "customer_satisfaction_score"
        ].round(2)
        display_df["hours_worked"] = (
            display_df["hours_worked"].round(1).astype(str) + " hrs"
        )
        display_df["total_cost"] = display_df["total_cost"].apply(
            lambda x: f"${x:,.2f}"
        )

        display_df = display_df.rename(
            columns={
                label_col: period_header,
                "agent_name": "Agent Name",
                "department": "Department",
                "total_interactions": "Total Interactions",
                "avg_handle_time_minutes": "AHT",
                "resolution_rate": "RT",
                "customer_satisfaction_score": "CSAT",
                "hours_worked": "Hours Worked",
                "total_cost": "Total Cost",
            }
        )

        st.dataframe(display_df, use_container_width=True, hide_index=True, height=300)

    def _render_department_donuts(
        self, agent_df: pd.DataFrame, selected_period: Any, latest_period: Any
    ) -> None:
        """Render donut charts for interactions and cost by department."""
        # Get data for the period
        period_df = self._get_period_data(agent_df, selected_period, latest_period)

        if period_df.empty:
            return

        # Aggregate by department
        dept_summary = (
            period_df.groupby("department")
            .agg({"total_interactions": "sum", "total_cost": "sum"})
            .reset_index()
        )

        col1, col2 = st.columns(2)

        with col1:
            # Interactions by department
            fig = px.pie(
                dept_summary,
                values="total_interactions",
                names="department",
                title="📊 Interactions by Department",
                color_discrete_sequence=self.CHART_COLORS["palette"],
                hole=0.5,
            )
            fig.update_traces(
                textposition="inside", textinfo="percent+label", textfont_size=14
            )
            fig.update_layout(
                height=350,
                margin=dict(t=50, b=50),
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5
                ),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Cost by department
            fig = px.pie(
                dept_summary,
                values="total_cost",
                names="department",
                title="💰 Cost by Department",
                color_discrete_sequence=self.CHART_COLORS["palette"],
                hole=0.5,
            )
            fig.update_traces(
                textposition="inside", textinfo="percent+label", textfont_size=14
            )
            fig.update_layout(
                height=350,
                margin=dict(t=50, b=50),
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5
                ),
            )
            st.plotly_chart(fig, use_container_width=True)

    def _render_efficiency_rankings(
        self, agent_df: pd.DataFrame, selected_period: Any, latest_period: Any
    ) -> None:
        """Render 4 efficiency ranking containers."""
        # Get data for the period
        period_df = self._get_period_data(agent_df, selected_period, latest_period)

        if period_df.empty:
            return

        st.markdown("### 🏆 Efficiency Rankings")

        # Calculate rankings
        # Most Efficient (lowest cost per interaction)
        most_efficient = period_df.loc[period_df["cost_per_interaction"].idxmin()]

        # Most Hours Worked
        most_hours = period_df.loc[period_df["hours_worked"].idxmax()]

        # Most Interactions
        most_interactions = period_df.loc[period_df["total_interactions"].idxmax()]

        # Best CSAT
        best_csat = period_df.loc[period_df["customer_satisfaction_score"].idxmax()]

        # Render 4 containers in 2 rows of 2
        col1, col2 = st.columns(2)

        with col1:
            self._render_ranking_card(
                "🎯 Most Efficient",
                most_efficient["agent_name"],
                most_efficient["department"],
                f"${most_efficient['cost_per_interaction']:.2f}/interaction",
                "#83F63B",
            )

        with col2:
            self._render_ranking_card(
                "⏰ Most Hours Worked",
                most_hours["agent_name"],
                most_hours["department"],
                f"{most_hours['hours_worked']:.1f} hours",
                "#3B82F6",
            )

        col3, col4 = st.columns(2)

        with col3:
            self._render_ranking_card(
                "📈 Most Interactions",
                most_interactions["agent_name"],
                most_interactions["department"],
                f"{int(most_interactions['total_interactions']):,} interactions",
                "#F63B83",
            )

        with col4:
            self._render_ranking_card(
                "⭐ Best CSAT",
                best_csat["agent_name"],
                best_csat["department"],
                f"{best_csat['customer_satisfaction_score']:.2f}/5",
                "#F6B83B",
            )

    def _render_ranking_card(
        self, title: str, agent_name: str, department: str, value: str, color: str
    ) -> None:
        """Render a single ranking card."""
        html_content = f"""<div style="background: linear-gradient(135deg, {color}15, {color}05); border-left: 4px solid {color}; border-radius: 8px; padding: 20px; margin-bottom: 15px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 10px;">{title}</div>
<div style="font-size: 22px; font-weight: bold; color: {color}; margin-bottom: 5px;">{agent_name}</div>
<div style="font-size: 12px; color: #666; margin-bottom: 8px;">{department}</div>
<div style="font-size: 18px; font-weight: bold; color: {color};">{value}</div>
</div>"""

        st.markdown(html_content, unsafe_allow_html=True)
