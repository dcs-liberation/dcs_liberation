from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from collections.abc import Iterator
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from game.ato.flightstate import InCombat, InFlight
from .. import GameUpdateEvents

if TYPE_CHECKING:
    from game.ato import Flight
    from ..simulationresults import SimulationResults


class FrozenCombat(ABC):
    def __init__(self, freeze_duration: timedelta) -> None:
        self.id = uuid.uuid4()
        self.freeze_duration = freeze_duration
        self.elapsed_time = timedelta()

    def on_game_tick(
        self,
        time: datetime,
        duration: timedelta,
        results: SimulationResults,
        events: GameUpdateEvents,
    ) -> bool:
        self.elapsed_time += duration
        if self.elapsed_time >= self.freeze_duration:
            self.resolve(results, events, time, self.elapsed_time)
            return True
        return False

    @abstractmethod
    def resolve(
        self,
        results: SimulationResults,
        events: GameUpdateEvents,
        time: datetime,
        elapsed_time: timedelta,
    ) -> None:
        ...

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
