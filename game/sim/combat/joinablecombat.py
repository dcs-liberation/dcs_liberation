from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import TYPE_CHECKING

from .frozencombat import FrozenCombat

if TYPE_CHECKING:
    from game.ato import Flight


class JoinableCombat(FrozenCombat, ABC):
    def __init__(self, flights: list[Flight]) -> None:
        self.flights = flights

    @abstractmethod
    def joinable_by(self, flight: Flight) -> bool:
        ...

    def join(self, flight: Flight) -> None:
        self.flights.append(flight)

    def iter_flights(self) -> Iterator[Flight]:
        yield from self.flights
