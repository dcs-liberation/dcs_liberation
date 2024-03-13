from __future__ import annotations

import logging
import random
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from shapely.ops import unary_union

from game.ato.flightstate import InCombat, InFlight
from game.utils import dcs_to_shapely_point
from .joinablecombat import JoinableCombat
from .. import GameUpdateEvents

if TYPE_CHECKING:
    from game.ato import Flight
    from ..simulationresults import SimulationResults


class AirCombat(JoinableCombat):
    def __init__(self, freeze_duration: timedelta, flights: list[Flight]) -> None:
        super().__init__(freeze_duration, flights)
        footprints = []
        for flight in self.flights:
            if (region := flight.state.a2a_commit_region()) is not None:
                footprints.append(region)
        self.footprint = unary_union(footprints)

    def joinable_by(self, flight: Flight) -> bool:
        if not flight.state.will_join_air_combat:
            return False

        if not isinstance(flight.state, InFlight):
            raise NotImplementedError(
                f"Only InFlight flights are expected to join air combat. {flight} is "
                "not InFlight"
            )

        if self.footprint.intersects(
            dcs_to_shapely_point(flight.state.estimate_position())
        ):
            return True
        return False

    def __str__(self) -> str:
        blue_flights = []
        red_flights = []
        for flight in self.flights:
            if flight.squadron.player:
                blue_flights.append(str(flight))
            else:
                red_flights.append(str(flight))

        blue = ", ".join(blue_flights)
        red = ", ".join(red_flights)
        return f"air combat {blue} vs {red}"

    def because(self) -> str:
        return f"of {self}"

    def describe(self) -> str:
        return f"in air-to-air combat"

    def resolve(
        self,
        results: SimulationResults,
        events: GameUpdateEvents,
        time: datetime,
        elapsed_time: timedelta,
    ) -> None:
        blue = []
        red = []
        for flight in self.flights:
            if flight.squadron.player:
                blue.append(flight)
            else:
                red.append(flight)
        if len(blue) > len(red):
            winner = blue
            loser = red
        elif len(blue) < len(red):
            winner = red
            loser = blue
        elif random.random() >= 0.5:
            winner = blue
            loser = red
        else:
            winner = red
            loser = blue

        if winner == blue:
            logging.debug(f"{self} auto-resolved as blue victory")
        else:
            logging.debug(f"{self} auto-resolved as red victory")

        for flight in loser:
            flight.kill(results, events)

        for flight in winner:
            assert isinstance(flight.state, InCombat)
            if random.random() >= 0.5:
                flight.kill(results, events)
            else:
                flight.state.exit_combat(events, time, elapsed_time)
