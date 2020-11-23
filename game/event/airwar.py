from __future__ import annotations
from typing import TYPE_CHECKING

from .event import Event

if TYPE_CHECKING:
    from game.theater import ConflictTheater


class AirWarEvent(Event):
    """An Event centered on the overall Air War"""

    def __str__(self):
        return "Frontline attack"
