"""
Weekly tab class module.
Handles rendering and presentation of weekly analytics dashboard.
"""
from datetime import datetime
import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from classes.base_tab import BaseTab
from classes.content_tabs import OverallContent, ChannelContent, CallsContent, AgentContent
from reporting.weekly.weekly_report import WeeklyReport


class WeeklyTab(BaseTab):
    """Weekly analytics view - handles rendering and UI presentation only."""

    def __init__(self):
        """Initialize WeeklyTab."""
        super().__init__(title="Weekly Analytics", icon="📆")
        self.report = WeeklyReport()
        
        # Initialize content tabs
        self.overall_content = OverallContent(self.report, "weekly")
        self.channel_content = ChannelContent(self.report, "weekly")
        self.calls_content = CallsContent(self.report, "weekly")
        self.agent_content = AgentContent(self.report, "weekly")

    def render(self) -> None:
        """Render the weekly analytics dashboard."""
        # Render header/title section
        self._render_header_section()
        
        # Get selected period
        selected_week, prev_week = self._render_period_selector()
        
        # Render KPI cards
        self._render_kpi_cards(selected_week, prev_week)
        
        # Render content tabs
        self._render_content_tabs(selected_week, prev_week)

    def _render_header_section(self) -> None:
        """Render the animated header section with gradient and floating elements."""
        header_html = """
<style>
.weekly-header {
    position: relative;
    background: linear-gradient(135deg, #F63B83 0%, #3B82F6 50%, #83F63B 100%);
    border-radius: 16px;
    padding: 30px 40px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(246, 59, 131, 0.3);
}
.weekly-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    animation: shimmer-weekly 3s infinite linear;
}
@keyframes shimmer-weekly {
    0% { transform: translateX(-100%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}
.weekly-header-content {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.weekly-title-section {
    display: flex;
    align-items: center;
    gap: 15px;
}
.weekly-icon {
    font-size: 48px;
    animation: bounce-weekly 2s ease-in-out infinite;
}
@keyframes bounce-weekly {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.weekly-title {
    font-size: 32px;
    font-weight: 700;
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    margin: 0;
}
.weekly-subtitle {
    font-size: 14px;
    color: rgba(255,255,255,0.9);
    margin-top: 5px;
}
.weekly-decoration {
    display: flex;
    gap: 10px;
}
.weekly-floating-circle {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    animation: float-weekly 2s ease-in-out infinite;
}
.weekly-floating-circle:nth-child(1) {
    background: rgba(255,255,255,0.8);
    animation-delay: 0s;
}
.weekly-floating-circle:nth-child(2) {
    background: rgba(255,255,255,0.6);
    animation-delay: 0.3s;
}
.weekly-floating-circle:nth-child(3) {
    background: rgba(255,255,255,0.4);
    animation-delay: 0.6s;
}
@keyframes float-weekly {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-10px) scale(1.2); }
}
.weekly-corner-bubble {
    position: absolute;
    border-radius: 50%;
    opacity: 0.3;
    animation: pulse-weekly 4s ease-in-out infinite;
}
.weekly-bubble-1 {
    width: 80px;
    height: 80px;
    background: white;
    top: -20px;
    right: -20px;
    animation-delay: 0s;
}
.weekly-bubble-2 {
    width: 50px;
    height: 50px;
    background: white;
    bottom: -15px;
    left: 10%;
    animation-delay: 1s;
}
.weekly-bubble-3 {
    width: 30px;
    height: 30px;
    background: white;
    top: 20%;
    right: 15%;
    animation-delay: 2s;
}
@keyframes pulse-weekly {
    0%, 100% { transform: scale(1); opacity: 0.3; }
    50% { transform: scale(1.1); opacity: 0.5; }
}
</style>
<div class="weekly-header">
<div class="weekly-corner-bubble weekly-bubble-1"></div>
<div class="weekly-corner-bubble weekly-bubble-2"></div>
<div class="weekly-corner-bubble weekly-bubble-3"></div>
<div class="weekly-header-content">
<div class="weekly-title-section">
<span class="weekly-icon">📆</span>
<div>
<h1 class="weekly-title">Weekly Report</h1>
<p class="weekly-subtitle">Week-by-week performance tracking</p>
</div>
</div>
<div class="weekly-decoration">
<div class="weekly-floating-circle"></div>
<div class="weekly-floating-circle"></div>
<div class="weekly-floating-circle"></div>
</div>
</div>
</div>
"""
        st.markdown(header_html, unsafe_allow_html=True)

    def _render_period_selector(self) -> tuple:
        """Render period selector and return selected and previous periods."""
        available_weeks = self.report.get_available_weeks()
        week_options = available_weeks["week_start"].dt.strftime("%b %d, %Y").tolist()
        selected_idx = st.selectbox(
            "📆 Select Period",
            range(len(week_options)),
            format_func=lambda x: week_options[x],
            key="weekly_selector"
        )
        selected_week = available_weeks.iloc[selected_idx]["week_start"]
        
        # Get previous week for comparison
        prev_week = self.report.get_previous_week(selected_week)
        
        return selected_week, prev_week

    def _render_kpi_cards(self, selected_period, previous_period) -> None:
        """Render KPI metric cards at the top."""
        # Get metrics
        current_metrics = self.report.get_productivity_metrics(selected_period)
        previous_metrics = self.report.get_productivity_metrics(previous_period) if previous_period else {}
        deltas = self.report.get_deltas(current_metrics, previous_metrics)
        
        # First row of KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            delta_val = deltas.get("total_interactions", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "Total Interactions",
                f"{current_metrics.get('total_interactions', 0):,}",
                delta=delta_str
            )
        
        with col2:
            delta_val = deltas.get("avg_handle_time", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "Avg Handle Time",
                f"{current_metrics.get('avg_handle_time', 0):.1f} min",
                delta=delta_str,
                delta_color="inverse"
            )
        
        with col3:
            delta_val = deltas.get("customer_satisfaction_score", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "CSAT Score",
                f"{current_metrics.get('customer_satisfaction_score', 0):.2f}/5",
                delta=delta_str
            )
        
        with col4:
            delta_val = deltas.get("cost_per_interaction", {}).get("percentage", 0)
            delta_str = f"{delta_val:.1f}%" if delta_val != 0 else None
            st.metric(
                "Cost/Interaction",
                f"${current_metrics.get('cost_per_interaction', 0):.2f}",
                delta=delta_str,
                delta_color="inverse"
            )
        
        # Second row of KPIs - Channel breakdown
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📞 Calls", f"{current_metrics.get('total_calls', 0):,}")
        
        with col2:
            st.metric("📧 Emails", f"{current_metrics.get('total_emails', 0):,}")
        
        with col3:
            st.metric("💬 Chats", f"{current_metrics.get('total_chats', 0):,}")
        
        with col4:
            st.metric("📱 WhatsApp", f"{current_metrics.get('total_whatsapp', 0):,}")
        
        st.markdown("---")

    def _render_content_tabs(self, selected_period, previous_period) -> None:
        """Render the content tabs section."""
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overall Performance",
            "📞 Channel Performance", 
            "📈 Calls Performance",
            "👥 Agent Performance"
        ])
        
        with tab1:
            self.overall_content.render(selected_period, previous_period)
        
        with tab2:
            self.channel_content.render(selected_period, previous_period)
        
        with tab3:
            self.calls_content.render(selected_period, previous_period)
        
        with tab4:
            self.agent_content.render(selected_period, previous_period)
