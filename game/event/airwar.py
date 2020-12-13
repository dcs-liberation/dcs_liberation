from __future__ import annotations
from typing import TYPE_CHECKING

from .event import Event

if TYPE_CHECKING:
    from game.theater import ConflictTheater


class AirWarEvent(Event):
    """Event handler for the air battle"""

    def __str__(self):
        return "AirWar"
