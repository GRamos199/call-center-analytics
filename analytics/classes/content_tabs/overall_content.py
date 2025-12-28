"""
Overall Performance content tab.
Displays trends and general performance metrics.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Any

from .base_content import BaseContent


class OverallContent(BaseContent):
    """Renders overall performance metrics and trends."""

    def render(self, selected_period: Any, previous_period: Any = None) -> None:
        """Render the overall performance content."""
        self._render_interactions_chart()
        self._render_aht_fcr_chart()
        self._render_cost_csat_charts()

    def _render_interactions_chart(self) -> None:
        """Render full-width bar chart of interactions by period."""
        trend_data = self.report.get_trend_data("total_interactions", 12)
        
        if trend_data.empty:
            st.warning("No interaction data available.")
            return
        
        period_col = self.get_period_column()
        
        # Sort by period (oldest to newest, left to right)
        trend_data = trend_data.sort_values(by=period_col, ascending=True)
        
        fig = px.bar(
            trend_data,
            x=period_col,
            y="total_interactions",
            title="📊 Total Interactions by Period",
            color_discrete_sequence=[self.COLORS["primary"]],
            text="total_interactions"
        )
        
        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )
        
        fig.update_layout(
            hovermode="x unified",
            plot_bgcolor=self.COLORS["light_bg"],
            xaxis_title="Period",
            yaxis_title="Total Interactions",
            height=400,
            margin=dict(t=50, b=50),
            xaxis=dict(categoryorder='array', categoryarray=trend_data[period_col].tolist())
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _render_aht_fcr_chart(self) -> None:
        """Render full-width line chart of AHT and FCR Rate over time."""
        # Get both metrics
        aht_data = self.report.get_trend_data("avg_handle_time_minutes", 12)
        fcr_data = self.report.get_trend_data("first_call_resolution_rate", 12)
        
        if aht_data.empty and fcr_data.empty:
            st.warning("No AHT/FCR data available.")
            return
        
        period_col = self.get_period_column()
        
        # Merge data on period
        if not aht_data.empty and not fcr_data.empty:
            merged_data = aht_data.merge(fcr_data, on=period_col, how='outer')
        elif not aht_data.empty:
            merged_data = aht_data
        else:
            merged_data = fcr_data
        
        # Sort by period (oldest to newest)
        merged_data = merged_data.sort_values(by=period_col, ascending=True)
        
        # Create figure with secondary y-axis
        fig = go.Figure()
        
        # AHT line (primary y-axis)
        if "avg_handle_time_minutes" in merged_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=merged_data[period_col],
                    y=merged_data["avg_handle_time_minutes"],
                    name="Avg Handle Time (AHT)",
                    mode="lines+markers",
                    line=dict(color=self.COLORS["primary"], width=3),
                    marker=dict(size=8),
                    yaxis="y"
                )
            )
        
        # FCR Rate line (secondary y-axis)
        if "first_call_resolution_rate" in merged_data.columns:
            # Convert to percentage for display
            fcr_pct = merged_data["first_call_resolution_rate"] * 100
            fig.add_trace(
                go.Scatter(
                    x=merged_data[period_col],
                    y=fcr_pct,
                    name="First Call Resolution (FCR)",
                    mode="lines+markers",
                    line=dict(color=self.COLORS["success"], width=3),
                    marker=dict(size=8),
                    yaxis="y2"
                )
            )
        
        fig.update_layout(
            title="📈 AHT & First Call Resolution Rate Trend",
            hovermode="x unified",
            plot_bgcolor=self.COLORS["light_bg"],
            height=400,
            margin=dict(t=50, b=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                title="Period",
                categoryorder='array',
                categoryarray=merged_data[period_col].tolist()
            ),
            yaxis=dict(
                title=dict(text="AHT (minutes)", font=dict(color=self.COLORS["primary"])),
                tickfont=dict(color=self.COLORS["primary"]),
                side="left"
            ),
            yaxis2=dict(
                title=dict(text="FCR Rate (%)", font=dict(color=self.COLORS["success"])),
                tickfont=dict(color=self.COLORS["success"]),
                anchor="x",
                overlaying="y",
                side="right",
                range=[0, 100]
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _render_cost_csat_charts(self) -> None:
        """Render side-by-side charts for Costs and CSAT."""
        col1, col2 = st.columns(2)
        
        period_col = self.get_period_column()
        
        with col1:
            self._render_cost_chart(period_col)
        
        with col2:
            self._render_csat_chart(period_col)

    def _render_cost_chart(self, period_col: str) -> None:
        """Render cost trend chart."""
        cost_data = self.report.get_trend_data("total_cost", 12)
        cpi_data = self.report.get_trend_data("cost_per_interaction", 12)
        
        if cost_data.empty:
            st.warning("No cost data available.")
            return
        
        # Merge data
        if not cpi_data.empty:
            merged_data = cost_data.merge(cpi_data, on=period_col, how='outer')
        else:
            merged_data = cost_data
        
        # Sort by period
        merged_data = merged_data.sort_values(by=period_col, ascending=True)
        
        fig = go.Figure()
        
        # Total Cost as bars
        fig.add_trace(
            go.Bar(
                x=merged_data[period_col],
                y=merged_data["total_cost"],
                name="Total Cost",
                marker_color=self.COLORS["secondary"],
                yaxis="y"
            )
        )
        
        # Cost per Interaction as line on secondary axis
        if "cost_per_interaction" in merged_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=merged_data[period_col],
                    y=merged_data["cost_per_interaction"],
                    name="Cost/Interaction",
                    mode="lines+markers",
                    line=dict(color=self.COLORS["warning"], width=3),
                    marker=dict(size=8),
                    yaxis="y2"
                )
            )
        
        fig.update_layout(
            title="💰 Cost Analysis",
            hovermode="x unified",
            plot_bgcolor=self.COLORS["light_bg"],
            height=350,
            margin=dict(t=50, b=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                title="Period",
                categoryorder='array',
                categoryarray=merged_data[period_col].tolist()
            ),
            yaxis=dict(
                title=dict(text="Total Cost ($)", font=dict(color=self.COLORS["secondary"])),
                side="left"
            ),
            yaxis2=dict(
                title=dict(text="Cost/Interaction ($)", font=dict(color=self.COLORS["warning"])),
                anchor="x",
                overlaying="y",
                side="right"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _render_csat_chart(self, period_col: str) -> None:
        """Render CSAT trend chart."""
        csat_data = self.report.get_trend_data("customer_satisfaction_score", 12)
        
        if csat_data.empty:
            st.warning("No CSAT data available.")
            return
        
        # Sort by period
        csat_data = csat_data.sort_values(by=period_col, ascending=True)
        
        fig = go.Figure()
        
        # CSAT as line with area fill
        fig.add_trace(
            go.Scatter(
                x=csat_data[period_col],
                y=csat_data["customer_satisfaction_score"],
                name="CSAT Score",
                mode="lines+markers",
                line=dict(color=self.COLORS["success"], width=3),
                marker=dict(size=10),
                fill='tozeroy',
                fillcolor=f"rgba(40, 167, 69, 0.2)"
            )
        )
        
        # Add target line at 4.0
        fig.add_hline(
            y=4.0,
            line_dash="dash",
            line_color=self.COLORS["danger"],
            annotation_text="Target: 4.0",
            annotation_position="right"
        )
        
        fig.update_layout(
            title="😊 Customer Satisfaction (CSAT)",
            hovermode="x unified",
            plot_bgcolor=self.COLORS["light_bg"],
            height=350,
            margin=dict(t=50, b=50),
            xaxis=dict(
                title="Period",
                categoryorder='array',
                categoryarray=csat_data[period_col].tolist()
            ),
            yaxis=dict(
                title="CSAT Score",
                range=[1, 5],
                dtick=0.5
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
