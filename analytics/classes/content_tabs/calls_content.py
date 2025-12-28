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

    def _get_date_column(self) -> str:
        """Get the appropriate date column based on period type."""
        return "month" if self.period_type == "monthly" else "week_start"

    def _get_period_label(self, df: pd.DataFrame) -> str:
        """Get the period label column, creating it if necessary for weekly data."""
        if self.period_type == "monthly":
            return "month_name"
        else:
            # For weekly, create a label from week_start
            if "week_label" not in df.columns:
                df["week_label"] = df["week_start"].dt.strftime("%b %d %Y")
            return "week_label"

    def render(self, selected_period: Any, previous_period: Any = None) -> None:
        """Render the calls performance content."""
        try:
            # Load all calls data
            calls_df = self.report.data_loader.load_calls_data()
            
            if calls_df.empty:
                st.warning("No calls data available.")
                return
            
            # Add period label for weekly data
            if self.period_type == "weekly":
                calls_df["week_label"] = calls_df["week_start"].dt.strftime("%b %d %Y")
            
            # Filter to last 12 periods
            date_col = self._get_date_column()
            recent_periods = calls_df[date_col].drop_duplicates().nlargest(12)
            calls_df = calls_df[calls_df[date_col].isin(recent_periods)]
            
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
        """Render summary metrics container with RT Median, CSAT Avg, Best/Worst Period."""
        date_col = self._get_date_column()
        label_col = self._get_period_label(calls_df)
        period_label = "Month" if self.period_type == "monthly" else "Week"
        
        # Overall metrics
        # RT Median - median of period resolution rates
        rt_median = calls_df.groupby(date_col)["resolved"].mean().median() * 100
        
        # CSAT Average
        csat_avg = calls_df["customer_satisfaction"].mean()
        
        # Best and Worst Period
        period_resolution = calls_df.groupby([date_col, label_col])["resolved"].mean().reset_index()
        period_resolution.columns = [date_col, label_col, "resolution_rate"]
        period_resolution = period_resolution.sort_values(date_col)
        
        if not period_resolution.empty:
            best_period_row = period_resolution.loc[period_resolution["resolution_rate"].idxmax()]
            worst_period_row = period_resolution.loc[period_resolution["resolution_rate"].idxmin()]
            best_period = best_period_row[label_col]
            worst_period = worst_period_row[label_col]
            best_period_rt = best_period_row["resolution_rate"] * 100
            worst_period_rt = worst_period_row["resolution_rate"] * 100
        else:
            best_period = "N/A"
            worst_period = "N/A"
            best_period_rt = 0
            worst_period_rt = 0
        
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
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">Best {period_label}</div>
<div style="font-size: 20px; font-weight: bold; color: #28a745;">{best_period}</div>
<div style="font-size: 14px; font-weight: bold; color: #28a745;">{best_period_rt:.2f}% RT</div>
</div>
<div style="text-align: center; flex: 1; min-width: 150px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">Worst {period_label}</div>
<div style="font-size: 20px; font-weight: bold; color: #dc3545;">{worst_period}</div>
<div style="font-size: 14px; font-weight: bold; color: #dc3545;">{worst_period_rt:.2f}% RT</div>
</div>
</div>
</div>'''
        
        st.markdown(html_content, unsafe_allow_html=True)

    def _render_total_calls_chart(self, calls_df: pd.DataFrame) -> None:
        """Render bar chart of total calls by period."""
        date_col = self._get_date_column()
        label_col = self._get_period_label(calls_df)
        
        # Group by period
        period_calls = calls_df.groupby([date_col, label_col]).agg({
            "call_id": "count"
        }).reset_index()
        period_calls.columns = [date_col, label_col, "total_calls"]
        period_calls = period_calls.sort_values(date_col)
        
        title = "📞 Total Calls by Month" if self.period_type == "monthly" else "📞 Total Calls by Week"
        
        fig = px.bar(
            period_calls,
            x=label_col,
            y="total_calls",
            title=title,
            color_discrete_sequence=[self.COLORS["primary"]],
            text="total_calls"
        )
        
        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )
        
        fig.update_layout(
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Date",
            yaxis_title="Total Calls",
            height=400,
            margin=dict(t=50, b=50),
            xaxis=dict(
                categoryorder='array',
                categoryarray=period_calls[label_col].tolist(),
                showgrid=False
            ),
            yaxis=dict(showgrid=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _render_resolution_rate_chart(self, calls_df: pd.DataFrame) -> None:
        """Render line chart of RT (Median) by period."""
        date_col = self._get_date_column()
        label_col = self._get_period_label(calls_df)
        
        # Group by period and calculate resolution rate
        period_rt = calls_df.groupby([date_col, label_col]).agg({
            "resolved": "mean"
        }).reset_index()
        period_rt.columns = [date_col, label_col, "resolution_rate"]
        period_rt = period_rt.sort_values(date_col)
        period_rt["resolution_rate_pct"] = period_rt["resolution_rate"] * 100
        
        title = "📈 Resolution Rate (RT) by Month" if self.period_type == "monthly" else "📈 Resolution Rate (RT) by Week"
        
        fig = px.line(
            period_rt,
            x=label_col,
            y="resolution_rate_pct",
            title=title,
            markers=True,
            color_discrete_sequence=[self.COLORS["success"]]
        )
        
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=10)
        )
        
        fig.update_layout(
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Date",
            yaxis_title="Resolution Rate (%)",
            height=400,
            margin=dict(t=50, b=50),
            xaxis=dict(
                categoryorder='array',
                categoryarray=period_rt[label_col].tolist(),
                showgrid=False
            ),
            yaxis=dict(showgrid=False)
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
        """Render line chart of average duration in hours by period."""
        date_col = self._get_date_column()
        label_col = self._get_period_label(calls_df)
        # Group by period and calculate average duration in hours
        period_duration = calls_df.groupby([date_col, label_col]).agg({
            "duration_minutes": "mean"
        }).reset_index()
        period_duration.columns = [date_col, label_col, "avg_duration_min"]
        period_duration = period_duration.sort_values(date_col)
        period_duration["avg_duration_hours"] = period_duration["avg_duration_min"] / 60
        
        title = "⏱️ Average Call Duration (Hours) by Month" if self.period_type == "monthly" else "⏱️ Average Call Duration (Hours) by Week"
        
        fig = px.line(
            period_duration,
            x=label_col,
            y="avg_duration_hours",
            title=title,
            markers=True,
            color_discrete_sequence=[self.COLORS["secondary"]]
        )
        
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=10)
        )
        
        fig.update_layout(
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Date",
            yaxis_title="Avg Duration (Hours)",
            height=350,
            margin=dict(t=50, b=50),
            xaxis=dict(
                categoryorder='array',
                categoryarray=period_duration[label_col].tolist(),
                showgrid=False
            ),
            yaxis=dict(showgrid=False)
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
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
