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
        """Render the header section (placeholder for future container design)."""
        st.markdown("# 📆 Weekly Report")
        st.markdown("---")

    def _render_period_selector(self) -> tuple:
        """Render period selector and return selected and previous periods."""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            available_weeks = self.report.get_available_weeks()
            week_options = available_weeks["week_start"].dt.strftime("Week of %b %d, %Y").tolist()
            selected_idx = st.selectbox(
                "📆 Select Period",
                range(len(week_options)),
                format_func=lambda x: week_options[x],
                key="weekly_selector"
            )
            selected_week = available_weeks.iloc[selected_idx]["week_start"]
        
        with col2:
            st.write("")
            st.write("")
            if st.button("🔄 Refresh Data", key="weekly_refresh", use_container_width=True):
                self.report.refresh_data()
                st.rerun()
        
        with col3:
            st.write("")
        
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
