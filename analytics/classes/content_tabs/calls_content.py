"""
Calls Performance content tab.
Displays detailed call analytics and patterns.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Any, Optional

from .base_content import BaseContent


class CallsContent(BaseContent):
    """Renders calls performance metrics and visualizations."""

    def render(self, selected_period: Any, previous_period: Any = None) -> None:
        """Render the calls performance content."""
        try:
            # Load all calls data
            calls_df = self.report.data_loader.load_calls_data()
            
            if calls_df.empty:
                st.warning("No calls data available.")
                return
            
            # Agent filter
            selected_agent = self._render_agent_filter(calls_df)
            
            # Filter data by agent if selected
            filtered_df = self._filter_by_agent(calls_df, selected_agent)
            
            # Render components
            self._render_summary_metrics(filtered_df)
            self._render_total_calls_chart(filtered_df)
            self._render_resolution_rate_chart(filtered_df)
            self._render_duration_and_resolution_charts(filtered_df)
            
        except Exception as e:
            st.error(f"Error loading calls data: {str(e)}")

    def _render_agent_filter(self, calls_df: pd.DataFrame) -> str:
        """Render agent filter dropdown."""
        agents = ["All Agents"] + sorted(calls_df["agent_name"].unique().tolist())
        
        selected_agent = st.selectbox(
            "Filter by Agent",
            options=agents,
            index=0,
            key="calls_agent_filter"
        )
        
        return selected_agent

    def _filter_by_agent(self, calls_df: pd.DataFrame, selected_agent: str) -> pd.DataFrame:
        """Filter calls data by selected agent."""
        if selected_agent == "All Agents":
            return calls_df
        return calls_df[calls_df["agent_name"] == selected_agent]

    def _render_summary_metrics(self, calls_df: pd.DataFrame) -> None:
        """Render summary metrics container with RT Median, CSAT Avg, Best/Worst Month."""
        # Calculate metrics by month
        monthly_stats = calls_df.groupby("month_name").agg({
            "resolved": "mean",
            "customer_satisfaction": "mean",
            "call_id": "count"
        }).reset_index()
        monthly_stats.columns = ["month_name", "resolution_rate", "avg_csat", "total_calls"]
        
        # Overall metrics
        # RT Median - median of monthly resolution rates
        rt_median = calls_df.groupby("month")["resolved"].mean().median() * 100
        
        # CSAT Average
        csat_avg = calls_df["customer_satisfaction"].mean()
        
        # Best and Worst Month
        monthly_resolution = calls_df.groupby(["month", "month_name"])["resolved"].mean().reset_index()
        monthly_resolution.columns = ["month", "month_name", "resolution_rate"]
        monthly_resolution = monthly_resolution.sort_values("month")
        
        if not monthly_resolution.empty:
            best_month_row = monthly_resolution.loc[monthly_resolution["resolution_rate"].idxmax()]
            worst_month_row = monthly_resolution.loc[monthly_resolution["resolution_rate"].idxmin()]
            best_month = best_month_row["month_name"]
            worst_month = worst_month_row["month_name"]
            best_month_rt = best_month_row["resolution_rate"] * 100
            worst_month_rt = worst_month_row["resolution_rate"] * 100
        else:
            best_month = "N/A"
            worst_month = "N/A"
            best_month_rt = 0
            worst_month_rt = 0
        
        # Render container
        color = self.COLORS["primary"]
        html_content = f'''<div style="background: linear-gradient(135deg, {color}15, {color}05); border-left: 4px solid {color}; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
<div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
<div style="text-align: center; flex: 1; min-width: 150px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">RT (Median)</div>
<div style="font-size: 28px; font-weight: bold; color: {color};">{rt_median:.2f}%</div>
</div>
<div style="text-align: center; flex: 1; min-width: 150px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">CSAT (Avg)</div>
<div style="font-size: 28px; font-weight: bold; color: {color};">{csat_avg:.2f}/5</div>
</div>
<div style="text-align: center; flex: 1; min-width: 150px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">Best Month</div>
<div style="font-size: 20px; font-weight: bold; color: #28a745;">{best_month}</div>
<div style="font-size: 14px; font-weight: bold; color: #28a745;">{best_month_rt:.2f}% RT</div>
</div>
<div style="text-align: center; flex: 1; min-width: 150px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">Worst Month</div>
<div style="font-size: 20px; font-weight: bold; color: #dc3545;">{worst_month}</div>
<div style="font-size: 14px; font-weight: bold; color: #dc3545;">{worst_month_rt:.2f}% RT</div>
</div>
</div>
</div>'''
        
        st.markdown(html_content, unsafe_allow_html=True)

    def _render_total_calls_chart(self, calls_df: pd.DataFrame) -> None:
        """Render bar chart of total calls by month."""
        # Group by month
        monthly_calls = calls_df.groupby(["month", "month_name"]).agg({
            "call_id": "count"
        }).reset_index()
        monthly_calls.columns = ["month", "month_name", "total_calls"]
        monthly_calls = monthly_calls.sort_values("month")
        
        fig = px.bar(
            monthly_calls,
            x="month_name",
            y="total_calls",
            title="📞 Total Calls by Month",
            color_discrete_sequence=[self.COLORS["primary"]],
            text="total_calls"
        )
        
        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )
        
        fig.update_layout(
            hovermode="x unified",
            plot_bgcolor=self.COLORS["light_bg"],
            xaxis_title="Month",
            yaxis_title="Total Calls",
            height=400,
            margin=dict(t=50, b=50),
            xaxis=dict(categoryorder='array', categoryarray=monthly_calls["month_name"].tolist())
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _render_resolution_rate_chart(self, calls_df: pd.DataFrame) -> None:
        """Render line chart of RT (Median) by month."""
        # Group by month and calculate median resolution rate
        monthly_rt = calls_df.groupby(["month", "month_name"]).agg({
            "resolved": "mean"  # This gives us the resolution rate per month
        }).reset_index()
        monthly_rt.columns = ["month", "month_name", "resolution_rate"]
        monthly_rt = monthly_rt.sort_values("month")
        monthly_rt["resolution_rate_pct"] = monthly_rt["resolution_rate"] * 100
        
        fig = px.line(
            monthly_rt,
            x="month_name",
            y="resolution_rate_pct",
            title="📈 Resolution Rate (RT) by Month",
            markers=True,
            color_discrete_sequence=[self.COLORS["success"]]
        )
        
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=10)
        )
        
        fig.update_layout(
            hovermode="x unified",
            plot_bgcolor=self.COLORS["light_bg"],
            xaxis_title="Month",
            yaxis_title="Resolution Rate (%)",
            height=400,
            margin=dict(t=50, b=50),
            xaxis=dict(categoryorder='array', categoryarray=monthly_rt["month_name"].tolist())
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _render_duration_and_resolution_charts(self, calls_df: pd.DataFrame) -> None:
        """Render avg duration line chart and resolution donut chart side by side."""
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_avg_duration_chart(calls_df)
        
        with col2:
            self._render_resolution_donut_chart(calls_df)

    def _render_avg_duration_chart(self, calls_df: pd.DataFrame) -> None:
        """Render line chart of average duration in hours by month."""
        # Group by month and calculate average duration in hours
        monthly_duration = calls_df.groupby(["month", "month_name"]).agg({
            "duration_minutes": "mean"
        }).reset_index()
        monthly_duration.columns = ["month", "month_name", "avg_duration_min"]
        monthly_duration = monthly_duration.sort_values("month")
        monthly_duration["avg_duration_hours"] = monthly_duration["avg_duration_min"] / 60
        
        fig = px.line(
            monthly_duration,
            x="month_name",
            y="avg_duration_hours",
            title="⏱️ Average Call Duration (Hours) by Month",
            markers=True,
            color_discrete_sequence=[self.COLORS["secondary"]]
        )
        
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=10)
        )
        
        fig.update_layout(
            hovermode="x unified",
            plot_bgcolor=self.COLORS["light_bg"],
            xaxis_title="Month",
            yaxis_title="Avg Duration (Hours)",
            height=350,
            margin=dict(t=50, b=50),
            xaxis=dict(categoryorder='array', categoryarray=monthly_duration["month_name"].tolist())
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _render_resolution_donut_chart(self, calls_df: pd.DataFrame) -> None:
        """Render donut chart of resolved vs not resolved calls."""
        # Calculate totals
        total_resolved = calls_df["resolved"].sum()
        total_not_resolved = len(calls_df) - total_resolved
        
        resolution_data = pd.DataFrame({
            "Status": ["Resolved", "Not Resolved"],
            "Count": [total_resolved, total_not_resolved]
        })
        
        fig = px.pie(
            resolution_data,
            values="Count",
            names="Status",
            title="✅ Resolved vs Not Resolved",
            color_discrete_sequence=[self.COLORS["success"], self.COLORS["danger"]],
            hole=0.5
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=14
        )
        
        fig.update_layout(
            height=350,
            margin=dict(t=50, b=50),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
