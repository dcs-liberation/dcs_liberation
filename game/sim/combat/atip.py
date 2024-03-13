from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from .frozencombat import FrozenCombat
from .. import GameUpdateEvents
from ...ato.flightstate import InCombat

if TYPE_CHECKING:
    from game.ato import Flight
    from ..simulationresults import SimulationResults


class AtIp(FrozenCombat):
    def __init__(self, freeze_duration: timedelta, flight: Flight) -> None:
        super().__init__(freeze_duration)
        self.flight = flight

    def because(self) -> str:
        return f"{self.flight} is at its IP"

    def describe(self) -> str:
        return f"at IP"

    def iter_flights(self) -> Iterator[Flight]:
        yield self.flight

    def resolve(
        self,
        results: SimulationResults,
        events: GameUpdateEvents,
        time: datetime,
        elapsed_time: timedelta,
    ) -> None:
        logging.debug(
            f"{self.flight} attack on {self.flight.package.target} auto-resolved with "
            "mission failure but no losses"
        )
        assert isinstance(self.flight.state, InCombat)
        self.flight.state.exit_combat(
            events, time, elapsed_time, avoid_further_combat=True
        )
