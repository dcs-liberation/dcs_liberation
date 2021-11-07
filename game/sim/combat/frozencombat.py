from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import TYPE_CHECKING

from game.ato.flightstate import InCombat, InFlight

if TYPE_CHECKING:
    from game.ato import Flight


class FrozenCombat(ABC):
    @abstractmethod
    def because(self) -> str:
        ...

    @abstractmethod
    def describe(self) -> str:
        ...

    @abstractmethod
    def iter_flights(self) -> Iterator[Flight]:
        ...

    def update_flight_states(self) -> None:
        for flight in self.iter_flights():
            if not isinstance(flight.state, InFlight):
                raise RuntimeError(
                    f"Found non in-flight aircraft engaged in combat: {flight}"
                )
            flight.set_state(InCombat(flight.state, self))
