from __future__ import annotations

import math
from typing import TYPE_CHECKING

from dcs import Point

from game.utils import Distance, meters

if TYPE_CHECKING:
    from game.ato.flightwaypoint import FlightWaypoint
    from game.dcs.aircrafttype import FuelConsumption


class BingoEstimator:
    """Estimates bingo/joker fuel values for a flight plan.

    The results returned by this class are bogus for most airframes. Only the few
    airframes which have fuel consumption data available can provide even moderately
    reliable estimates. **Do not use this for flight planning.** This should only be
    used in briefing context where it's okay to be wrong.
    """

    def __init__(
        self,
        fuel_consumption: FuelConsumption | None,
        arrival: Point,
        divert: Point | None,
        waypoints: list[FlightWaypoint],
    ) -> None:
        self.fuel_consumption = fuel_consumption
        self.arrival = arrival
        self.divert = divert
        self.waypoints = waypoints

    def estimate_bingo(self) -> int:
        """Bingo fuel value for the FlightPlan"""
        if (fuel := self.fuel_consumption) is not None:
            return self._fuel_consumption_based_estimate(fuel)
        return self._legacy_bingo_estimate()

    def estimate_joker(self) -> int:
        """Joker fuel value for the FlightPlan"""
        return self.estimate_bingo() + 1000

    def _fuel_consumption_based_estimate(self, fuel: FuelConsumption) -> int:
        distance_to_arrival = self._max_distance_from(self.arrival)
        fuel_consumed = fuel.cruise * distance_to_arrival.nautical_miles
        bingo = fuel_consumed + fuel.min_safe
        return math.ceil(bingo / 100) * 100

    def _legacy_bingo_estimate(self) -> int:
        distance_to_arrival = self._max_distance_from(self.arrival)

        bingo = 1000.0  # Minimum Emergency Fuel
        bingo += 500  # Visual Traffic
        bingo += 15 * distance_to_arrival.nautical_miles

        if self.divert is not None:
            max_divert_distance = self._max_distance_from(self.divert)
            bingo += 10 * max_divert_distance.nautical_miles

        return round(bingo / 100) * 100

    def _max_distance_from(self, point: Point) -> Distance:
        return max(meters(point.distance_to_point(w.position)) for w in self.waypoints)
