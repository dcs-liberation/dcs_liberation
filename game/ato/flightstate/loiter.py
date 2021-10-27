from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from dcs import Point

from game.ato.flightstate import FlightState, InFlight
from game.utils import Distance, Speed
from gen.flights.flightplan import LoiterFlightPlan

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings


class Loiter(InFlight):
    def __init__(self, flight: Flight, settings: Settings, waypoint_index: int) -> None:
        assert isinstance(flight.flight_plan, LoiterFlightPlan)
        self.hold_duration = flight.flight_plan.hold_duration
        super().__init__(flight, settings, waypoint_index)

    def estimate_position(self) -> Point:
        return self.current_waypoint.position

    def estimate_altitude(self) -> tuple[Distance, str]:
        return self.current_waypoint.alt, self.current_waypoint.alt_type

    def estimate_speed(self) -> Speed:
        return self.flight.unit_type.preferred_patrol_speed(self.estimate_altitude()[0])

    def next_waypoint_state(self) -> FlightState:
        # Do not automatically advance to the next waypoint. Just proceed from the
        # current one with the normal flying state.
        return InFlight(self.flight, self.settings, self.waypoint_index)

    def travel_time_between_waypoints(self) -> timedelta:
        return self.hold_duration
