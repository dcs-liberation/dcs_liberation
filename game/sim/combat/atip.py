from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import timedelta
from typing import TYPE_CHECKING

from .frozencombat import FrozenCombat
from .. import GameUpdateEvents

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

    def resolve(self, results: SimulationResults, events: GameUpdateEvents) -> None:
        logging.debug(
            f"{self.flight} attack on {self.flight.package.target} auto-resolved with "
            "mission failure but no losses"
        )
