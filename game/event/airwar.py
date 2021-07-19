from __future__ import annotations

from .event import Event


class AirWarEvent(Event):
    """Event handler for the air battle"""

    def __str__(self) -> str:
        return "AirWar"
