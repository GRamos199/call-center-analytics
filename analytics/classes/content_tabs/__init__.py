"""Content tabs module for dashboard sections."""

from .agent_content import AgentContent
from .base_content import BaseContent
from .calls_content import CallsContent
from .channel_content import ChannelContent
from .overall_content import OverallContent

__all__ = [
    "BaseContent",
    "OverallContent",
    "ChannelContent",
    "CallsContent",
    "AgentContent",
]
