from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from datetime import timedelta
from typing import TYPE_CHECKING

from game.ato.flightstate import InCombat, InFlight
from .frozencombat import FrozenCombat

if TYPE_CHECKING:
    from game.ato import Flight


class JoinableCombat(FrozenCombat, ABC):
    def __init__(self, freeze_duration: timedelta, flights: list[Flight]) -> None:
        super().__init__(freeze_duration)
        self.flights = flights

    @abstractmethod
    def joinable_by(self, flight: Flight) -> bool:
        ...

    def join(self, flight: Flight) -> None:
        assert isinstance(flight.state, InFlight)
        assert not isinstance(flight.state, InCombat)
        self.flights.append(flight)
        flight.set_state(InCombat(flight.state, self))

    def iter_flights(self) -> Iterator[Flight]:
        yield from self.flights
