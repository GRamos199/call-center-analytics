"""
Channel Performance content tab.
Displays channel-specific metrics in individual containers.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Any, Optional

from .base_content import BaseContent


class ChannelContent(BaseContent):
    """Renders channel performance metrics in individual containers."""

    # Channel icons mapping
    CHANNEL_ICONS = {
        "Phone": "📞",
        "Email": "📧",
        "Chat": "💬",
        "WhatsApp": "📱"
    }

    # Channel colors mapping
    CHANNEL_COLORS = {
        "Phone": "#3B82F6",
        "Email": "#F63B83",
        "Chat": "#83F63B",
        "WhatsApp": "#F6B83B"
    }

    def render(self, selected_period: Any, previous_period: Any = None) -> None:
        """Render the channel performance content."""
        try:
            channel_df = self.report.get_channel_metrics(selected_period)
            
            # Get previous period data for deltas
            prev_channel_df = None
            if previous_period is not None:
                try:
                    prev_channel_df = self.report.get_channel_metrics(previous_period)
                except:
                    prev_channel_df = None
            
            if channel_df.empty:
                st.warning("No channel data available for this period.")
                return
            
            self._render_channel_cards(channel_df, prev_channel_df)
            
        except Exception as e:
            st.error(f"Error loading channel data: {str(e)}")

    def _render_channel_cards(self, channel_df: pd.DataFrame, prev_channel_df: Optional[pd.DataFrame] = None) -> None:
        """Render a card for each channel with metrics."""
        # Get unique channels
        channels = channel_df["channel"].unique()
        
        # Render each channel card one below another
        for channel in channels:
            channel_data = channel_df[channel_df["channel"] == channel].iloc[0]
            
            # Get previous period data for this channel
            prev_data = None
            if prev_channel_df is not None and not prev_channel_df.empty:
                prev_channel_rows = prev_channel_df[prev_channel_df["channel"] == channel]
                if not prev_channel_rows.empty:
                    prev_data = prev_channel_rows.iloc[0]
            
            self._render_single_channel_card(channel, channel_data, prev_data)

    def _calculate_delta(self, current: float, previous: Optional[float], is_percentage: bool = False) -> tuple:
        """Calculate delta and return (delta_value, delta_color, delta_arrow)."""
        if previous is None or previous == 0:
            return (None, "", "")
        
        delta = ((current - previous) / abs(previous)) * 100
        
        if delta > 0:
            delta_color = "#28a745"  # Green
            delta_arrow = "▲"
        elif delta < 0:
            delta_color = "#dc3545"  # Red
            delta_arrow = "▼"
        else:
            delta_color = "#666"
            delta_arrow = "―"
        
        return (delta, delta_color, delta_arrow)

    def _render_single_channel_card(self, channel: str, data: pd.Series, prev_data: Optional[pd.Series] = None) -> None:
        """Render a single channel card with all metrics inside."""
        icon = self.CHANNEL_ICONS.get(channel, "📊")
        color = self.CHANNEL_COLORS.get(channel, self.COLORS["primary"])
        
        # Get current metrics
        total_interactions = int(data["total_interactions"])
        aht = float(data["avg_handle_time_minutes"])
        resolution_rate = float(data["resolution_rate"])
        csat = float(data["customer_satisfaction_score"])
        total_cost = float(data["total_cost"])
        
        # Get previous metrics and calculate deltas
        if prev_data is not None:
            prev_interactions = int(prev_data["total_interactions"])
            prev_aht = float(prev_data["avg_handle_time_minutes"])
            prev_resolution = float(prev_data["resolution_rate"])
            prev_csat = float(prev_data["customer_satisfaction_score"])
            prev_cost = float(prev_data["total_cost"])
            
            delta_interactions = self._calculate_delta(total_interactions, prev_interactions)
            delta_aht = self._calculate_delta(aht, prev_aht)
            # For AHT, lower is better, so invert colors
            if delta_aht[0] is not None:
                aht_color = "#dc3545" if delta_aht[0] > 0 else "#28a745" if delta_aht[0] < 0 else "#666"
                delta_aht = (delta_aht[0], aht_color, delta_aht[2])
            
            delta_resolution = self._calculate_delta(resolution_rate, prev_resolution)
            delta_csat = self._calculate_delta(csat, prev_csat)
            delta_cost = self._calculate_delta(total_cost, prev_cost)
            # For cost, lower is better, so invert colors
            if delta_cost[0] is not None:
                cost_color = "#dc3545" if delta_cost[0] > 0 else "#28a745" if delta_cost[0] < 0 else "#666"
                delta_cost = (delta_cost[0], cost_color, delta_cost[2])
        else:
            delta_interactions = (None, "", "")
            delta_aht = (None, "", "")
            delta_resolution = (None, "", "")
            delta_csat = (None, "", "")
            delta_cost = (None, "", "")
        
        # Helper to format delta HTML
        def format_delta(delta_tuple):
            if delta_tuple[0] is None:
                return ""
            return f'<div style="font-size: 14px; font-weight: bold; color: {delta_tuple[1]}; margin-top: 5px;">{delta_tuple[2]} {abs(delta_tuple[0]):.1f}%</div>'
        
        # Channel header outside container
        st.markdown(f'<h3 style="margin: 20px 0 10px 0; color: {color};">{icon} {channel}</h3>', unsafe_allow_html=True)
        
        # Build HTML content for metrics container
        html_content = f'''<div style="background: linear-gradient(135deg, {color}15, {color}05); border-left: 4px solid {color}; border-radius: 8px; padding: 20px; margin-bottom: 10px;">
<div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
<div style="text-align: center; flex: 1; min-width: 120px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">Total Interactions</div>
<div style="font-size: 28px; font-weight: bold; color: {color};">{total_interactions:,}</div>
{format_delta(delta_interactions)}
</div>
<div style="text-align: center; flex: 1; min-width: 120px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">AHT (min)</div>
<div style="font-size: 28px; font-weight: bold; color: {color};">{aht:.1f}</div>
{format_delta(delta_aht)}
</div>
<div style="text-align: center; flex: 1; min-width: 120px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">Resolution Rate</div>
<div style="font-size: 28px; font-weight: bold; color: {color};">{resolution_rate * 100:.2f}%</div>
{format_delta(delta_resolution)}
</div>
<div style="text-align: center; flex: 1; min-width: 120px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">CSAT</div>
<div style="font-size: 28px; font-weight: bold; color: {color};">{csat:.2f}/5</div>
{format_delta(delta_csat)}
</div>
<div style="text-align: center; flex: 1; min-width: 120px;">
<div style="font-size: 14px; font-weight: bold; color: #444; margin-bottom: 8px;">Total Cost</div>
<div style="font-size: 28px; font-weight: bold; color: {color};">${total_cost:,.0f}</div>
{format_delta(delta_cost)}
</div>
</div>
</div>'''
        
        st.markdown(html_content, unsafe_allow_html=True)
