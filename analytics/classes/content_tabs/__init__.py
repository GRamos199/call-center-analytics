"""Content tabs module for dashboard sections."""
from .base_content import BaseContent
from .overall_content import OverallContent
from .channel_content import ChannelContent
from .calls_content import CallsContent
from .agent_content import AgentContent

__all__ = [
    "BaseContent",
    "OverallContent",
    "ChannelContent",
    "CallsContent",
    "AgentContent",
]
