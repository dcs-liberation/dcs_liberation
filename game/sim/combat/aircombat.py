from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.ops import unary_union

from game.ato.flightstate import InFlight
from game.utils import dcs_to_shapely_point
from .joinablecombat import JoinableCombat

if TYPE_CHECKING:
    from game.ato import Flight


class AirCombat(JoinableCombat):
    def __init__(self, flights: list[Flight]) -> None:
        super().__init__(flights)
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

    def because(self) -> str:
        blue_flights = []
        red_flights = []
        for flight in self.flights:
            if flight.squadron.player:
                blue_flights.append(str(flight))
            else:
                red_flights.append(str(flight))

        blue = ", ".join(blue_flights)
        red = ", ".join(red_flights)
        return f"of air combat {blue} vs {red}"

    def describe(self) -> str:
        return f"in air-to-air combat"
