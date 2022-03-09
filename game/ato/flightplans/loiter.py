from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import timedelta
from typing import TYPE_CHECKING, TypeGuard

from game.typeguard import self_type_guard
from .flightplan import FlightPlan
from .standard import StandardFlightPlan

if TYPE_CHECKING:
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint


class LoiterFlightPlan(StandardFlightPlan, ABC):
    def __init__(
        self,
        flight: Flight,
        departure: FlightWaypoint,
        arrival: FlightWaypoint,
        divert: FlightWaypoint | None,
        bullseye: FlightWaypoint,
        nav_to: list[FlightWaypoint],
        nav_from: list[FlightWaypoint],
        hold: FlightWaypoint,
        hold_duration: timedelta,
    ) -> None:
        super().__init__(flight, departure, arrival, divert, bullseye)
        self.nav_to = nav_to
        self.nav_from = nav_from
        self.hold = hold
        self.hold_duration = hold_duration

    @property
    @abstractmethod
    def push_time(self) -> timedelta:
        ...

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.hold:
            return self.push_time
        return None

    def travel_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        travel_time = super().travel_time_between_waypoints(a, b)
        if a != self.hold:
            return travel_time
        return travel_time + self.hold_duration

    @self_type_guard
    def is_loiter(self, flight_plan: FlightPlan) -> TypeGuard[LoiterFlightPlan]:
        return True
