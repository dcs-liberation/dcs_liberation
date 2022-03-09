from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from game.ato.flightplans.flightplan import FlightPlan

if TYPE_CHECKING:
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint


class StandardFlightPlan(FlightPlan, ABC):
    """Base type for all non-custom flight plans.

    We can't reason about custom flight plans so they get special treatment, but all
    others are guaranteed to have certain properties like departure and arrival points,
    potentially a divert field, and a bullseye
    """

    def __init__(
        self,
        flight: Flight,
        departure: FlightWaypoint,
        arrival: FlightWaypoint,
        divert: FlightWaypoint | None,
        bullseye: FlightWaypoint,
    ) -> None:
        super().__init__(flight)
        self.departure = departure
        self.arrival = arrival
        self.divert = divert
        self.bullseye = bullseye
