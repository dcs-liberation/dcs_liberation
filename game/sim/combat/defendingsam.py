from __future__ import annotations

from collections.abc import Iterator
from typing import Any, TYPE_CHECKING

from .frozencombat import FrozenCombat

if TYPE_CHECKING:
    from game.ato import Flight
    from game.theater import TheaterGroundObject


class DefendingSam(FrozenCombat):
    def __init__(self, flight: Flight, air_defenses: list[TheaterGroundObject]) -> None:
        super().__init__()
        self.flight = flight
        self.air_defenses = air_defenses

    def because(self) -> str:
        sams = ", ".join(str(d) for d in self.air_defenses)
        return f"{self.flight} is engaged by enemy air defenses: {sams}"

    def describe(self) -> str:
        return f"engaged by enemy air defenses"

    def iter_flights(self) -> Iterator[Flight]:
        yield self.flight
