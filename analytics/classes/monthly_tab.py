"""
Monthly tab class module.
Handles rendering and presentation of monthly analytics dashboard.
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
        """Render the header section (placeholder for future container design)."""
        st.markdown("# 📅 Monthly Report")
        st.markdown("---")

    def _render_period_selector(self) -> tuple:
        """Render period selector and return selected and previous periods."""
        available_months = self.report.get_available_months()
        month_options = available_months["month"].dt.strftime("%B %Y").tolist()
        selected_idx = st.selectbox(
            "📆 Select Period",
            range(len(month_options)),
            format_func=lambda x: month_options[x],
            key="monthly_selector"
        )
        selected_month = available_months.iloc[selected_idx]["month"]
        
        # Get previous month for comparison
        prev_month = self.report.get_previous_month(selected_month)
        
        return selected_month, prev_month

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
            st.metric("Interactions/Agent", f"{current_metrics.get('interactions_per_agent', 0):.0f}")
        
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
