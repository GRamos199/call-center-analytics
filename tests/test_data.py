# =============================================================================
# Tests Directory
# Place your pytest tests here
# =============================================================================

import pytest
import sys
from pathlib import Path

# Add analytics to path
sys.path.insert(0, str(Path(__file__).parent.parent / "analytics"))


class TestDataLoader:
    """Tests for DataLoader class."""

    def test_monthly_data_loading(self):
        """Test that monthly data loads correctly."""
        from utils.data_loader import DataLoader
        
        dl = DataLoader(period="monthly")
        overall = dl.load_overall_data()
        
        assert overall is not None
        assert len(overall) > 0

    def test_weekly_data_loading(self):
        """Test that weekly data loads correctly."""
        from utils.data_loader import DataLoader
        
        dl = DataLoader(period="weekly")
        overall = dl.load_overall_data()
        
        assert overall is not None
        assert len(overall) > 0

    def test_period_switching(self):
        """Test switching between monthly and weekly periods."""
        from utils.data_loader import DataLoader
        
        dl = DataLoader(period="monthly")
        dl.set_period("weekly")
        
        assert dl.period == "weekly"


class TestMetricLoader:
    """Tests for MetricLoader class."""

    def test_productivity_metrics(self):
        """Test that productivity metrics are calculated."""
        from utils.data_loader import DataLoader
        from utils.metric_loader import MetricLoader
        
        dl = DataLoader(period="monthly")
        ml = MetricLoader(dl)
        
        metrics = ml.calculate_productivity_metrics()
        
        assert metrics is not None
        assert isinstance(metrics, dict)


class TestDataIntegrity:
    """Tests for data integrity."""

    def test_all_data_files_exist(self):
        """Test that all required data files exist."""
        from utils.data_loader import DataLoader
        
        for period in ["monthly", "weekly"]:
            dl = DataLoader(period=period)
            
            assert dl.load_overall_data() is not None
            assert dl.load_agent_data() is not None
            assert dl.load_channel_data() is not None
            assert dl.load_calls_data() is not None
