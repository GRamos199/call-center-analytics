"""
Monthly tab class module.
Handles rendering and presentation of monthly analytics dashboard.
"""

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from classes.base_tab import BaseTab
from classes.content_tabs import (
    AgentContent,
    CallsContent,
    ChannelContent,
    OverallContent,
)
from reporting.monthly.monthly_report import MonthlyReport


class MonthlyTab(BaseTab):
    """Monthly analytics view - handles rendering and UI presentation only."""

    def __init__(self):
        """Initialize MonthlyTab."""
        super().__init__(title="Monthly Analytics", icon="📅")
        self.report = MonthlyReport()

        # Initialize content tabs
        self.overall_content = OverallContent(self.report, "monthly")
        self.channel_content = ChannelContent(self.report, "monthly")
        self.calls_content = CallsContent(self.report, "monthly")
        self.agent_content = AgentContent(self.report, "monthly")

    def render(self) -> None:
        """Render the monthly analytics dashboard."""
        # Render header/title section
        self._render_header_section()

        # Get selected period
        selected_month, prev_month = self._render_period_selector()

        # Render KPI cards
        self._render_kpi_cards(selected_month, prev_month)

        # Render content tabs
        self._render_content_tabs(selected_month, prev_month)

    def _render_header_section(self) -> None:
        """Render the animated header section with gradient and floating elements."""
        header_html = """
<style>
.monthly-header {
    position: relative;
    background: linear-gradient(135deg, #3B82F6 0%, #F63B83 50%, #83F63B 100%);
    border-radius: 16px;
    padding: 30px 40px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3);
}
.monthly-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    animation: shimmer 3s infinite linear;
}
@keyframes shimmer {
    0% { transform: translateX(-100%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}
.header-content {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header-title-section {
    display: flex;
    align-items: center;
    gap: 15px;
}
.header-icon {
    font-size: 48px;
    animation: bounce-icon 2s ease-in-out infinite;
}
@keyframes bounce-icon {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.header-title {
    font-size: 32px;
    font-weight: 700;
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    margin: 0;
}
.header-subtitle {
    font-size: 14px;
    color: rgba(255,255,255,0.9);
    margin-top: 5px;
}
.header-decoration {
    display: flex;
    gap: 10px;
}
.floating-circle {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    animation: float-circle 2s ease-in-out infinite;
}
.floating-circle:nth-child(1) {
    background: rgba(255,255,255,0.8);
    animation-delay: 0s;
}
.floating-circle:nth-child(2) {
    background: rgba(255,255,255,0.6);
    animation-delay: 0.3s;
}
.floating-circle:nth-child(3) {
    background: rgba(255,255,255,0.4);
    animation-delay: 0.6s;
}
@keyframes float-circle {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-10px) scale(1.2); }
}
.corner-bubble {
    position: absolute;
    border-radius: 50%;
    opacity: 0.3;
    animation: pulse-bubble 4s ease-in-out infinite;
}
.corner-bubble-1 {
    width: 80px;
    height: 80px;
    background: white;
    top: -20px;
    right: -20px;
    animation-delay: 0s;
}
.corner-bubble-2 {
    width: 50px;
    height: 50px;
    background: white;
    bottom: -15px;
    left: 10%;
    animation-delay: 1s;
}
.corner-bubble-3 {
    width: 30px;
    height: 30px;
    background: white;
    top: 20%;
    right: 15%;
    animation-delay: 2s;
}
@keyframes pulse-bubble {
    0%, 100% { transform: scale(1); opacity: 0.3; }
    50% { transform: scale(1.1); opacity: 0.5; }
}
</style>
<div class="monthly-header">
<div class="corner-bubble corner-bubble-1"></div>
<div class="corner-bubble corner-bubble-2"></div>
<div class="corner-bubble corner-bubble-3"></div>
<div class="header-content">
<div class="header-title-section">
<span class="header-icon">📅</span>
<div>
<h1 class="header-title">Monthly Report</h1>
<p class="header-subtitle">Comprehensive monthly analytics and insights</p>
</div>
</div>
<div class="header-decoration">
<div class="floating-circle"></div>
<div class="floating-circle"></div>
<div class="floating-circle"></div>
</div>
</div>
</div>
"""
        st.markdown(header_html, unsafe_allow_html=True)

    def _render_period_selector(self) -> tuple:
        """Render period selector and return selected and previous periods."""
        available_months = self.report.get_available_months()
        month_options = available_months["month"].dt.strftime("%B %Y").tolist()
        selected_idx = st.selectbox(
            "📆 Select Period",
            range(len(month_options)),
            format_func=lambda x: month_options[x],
            key="monthly_selector",
        )
        selected_month = available_months.iloc[selected_idx]["month"]

        # Get previous month for comparison
        prev_month = self.report.get_previous_month(selected_month)

        return selected_month, prev_month

    def _render_kpi_cards(self, selected_period, previous_period) -> None:
        """Render KPI metric cards at the top."""
        # Get metrics
        current_metrics = self.report.get_productivity_metrics(selected_period)
        previous_metrics = (
            self.report.get_productivity_metrics(previous_period)
            if previous_period
            else {}
        )
        deltas = self.report.get_deltas(current_metrics, previous_metrics)

        # First row of KPIs
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            delta_val = deltas.get("total_interactions", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "Total Interactions",
                f"{current_metrics.get('total_interactions', 0):,}",
                delta=delta_str,
            )

        with col2:
            delta_val = deltas.get("avg_handle_time", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "Avg Handle Time",
                f"{current_metrics.get('avg_handle_time', 0):.1f} min",
                delta=delta_str,
                delta_color="inverse",
            )

        with col3:
            delta_val = deltas.get("customer_satisfaction_score", {}).get(
                "percentage", 0
            )
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "CSAT Score",
                f"{current_metrics.get('customer_satisfaction_score', 0):.2f}/5",
                delta=delta_str,
            )

        with col4:
            delta_val = deltas.get("cost_per_interaction", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "Cost/Interaction",
                f"${current_metrics.get('cost_per_interaction', 0):.2f}",
                delta=delta_str,
                delta_color="inverse",
            )

        # Second row of KPIs
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            fcr = current_metrics.get("first_call_resolution_rate", 0) * 100
            st.metric("First Call Resolution", f"{fcr:.1f}%")

        with col2:
            st.metric("Total Cost", f"${current_metrics.get('total_cost', 0):,.2f}")

        with col3:
            st.metric("Active Agents", f"{current_metrics.get('unique_agents', 0)}")

        with col4:
            st.metric(
                "Interactions/Agent",
                f"{current_metrics.get('interactions_per_agent', 0):.0f}",
            )

        st.markdown("---")

    def _render_content_tabs(self, selected_period, previous_period) -> None:
        """Render the content tabs section."""
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📊 Overall Performance",
                "📞 Channel Performance",
                "📈 Calls Performance",
                "👥 Agent Performance",
            ]
        )

        with tab1:
            self.overall_content.render(selected_period, previous_period)

        with tab2:
            self.channel_content.render(selected_period, previous_period)

        with tab3:
            self.calls_content.render(selected_period, previous_period)

        with tab4:
            self.agent_content.render(selected_period, previous_period)
