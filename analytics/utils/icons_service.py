"""
Icons service module.
Provides iconography for the dashboard UI using Unicode and emoji icons.
Icons sourced from popular icon libraries (Flaticon, Font Awesome equivalents).
"""


class IconsService:
    """Service to manage icons used in the dashboard."""

    # Metrics Icons
    COST_PER_AGENT = "💰"
    COST_PER_CLIENT = "💵"
    PRODUCTIVITY = "⚡"
    HOURS_WORKED = "⏱️"
    
    # Call Center Icons
    CALL_CENTER = "☎️"
    AGENT = "👤"
    AGENTS = "👥"
    CLIENT = "🧑‍💼"
    PHONE = "📱"
    
    # Analytics Icons
    CHART = "📊"
    TREND_UP = "📈"
    TREND_DOWN = "📉"
    PERCENTAGE = "%"
    AVERAGE = "≈"
    TOTAL = "∑"
    
    # Time Icons
    CALENDAR = "📅"
    WEEK = "📆"
    MONTH = "📅"
    TIME = "🕐"
    
    # Status Icons
    SUCCESS = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    INFO = "ℹ️"
    
    # Navigation Icons
    DASHBOARD = "🏠"
    SETTINGS = "⚙️"
    REFRESH = "🔄"
    FILTER = "🔍"
    EXPORT = "💾"

    @staticmethod
    def get_metric_icon(metric_name: str) -> str:
        """
        Get icon for a given metric name.
        
        Args:
            metric_name: Name of the metric (lowercase with underscores)
            
        Returns:
            Icon string
        """
        icon_map = {
            "cost_per_agent": IconsService.COST_PER_AGENT,
            "cost_per_client": IconsService.COST_PER_CLIENT,
            "productivity": IconsService.PRODUCTIVITY,
            "hours_worked": IconsService.HOURS_WORKED,
            "total_calls": IconsService.PHONE,
            "agents": IconsService.AGENTS,
        }
        return icon_map.get(metric_name, IconsService.CHART)

    @staticmethod
    def get_status_icon(status: str) -> str:
        """
        Get icon for a given status.
        
        Args:
            status: Status type (success, warning, error, info)
            
        Returns:
            Icon string
        """
        status_map = {
            "success": IconsService.SUCCESS,
            "warning": IconsService.WARNING,
            "error": IconsService.ERROR,
            "info": IconsService.INFO,
        }
        return status_map.get(status.lower(), IconsService.INFO)
