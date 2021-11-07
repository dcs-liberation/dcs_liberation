from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from .frozencombat import FrozenCombat

if TYPE_CHECKING:
    from game.ato import Flight


class AtIp(FrozenCombat):
    def __init__(self, flight: Flight) -> None:
        super().__init__()
        self.flight = flight

    def because(self) -> str:
        return f"{self.flight} is at its IP"

    def describe(self) -> str:
        return f"at IP"

    def iter_flights(self) -> Iterator[Flight]:
        yield self.flight
