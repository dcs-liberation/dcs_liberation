from __future__ import annotations

from abc import ABC
from collections.abc import Iterator
from datetime import timedelta
from typing import TYPE_CHECKING, TypeGuard

from game.ato.flightplans.standard import StandardFlightPlan
from game.typeguard import self_type_guard
from game.utils import Distance, Speed

if TYPE_CHECKING:
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint
    from .flightplan import FlightPlan


class PatrollingFlightPlan(StandardFlightPlan, ABC):
    def __init__(
        self,
        flight: Flight,
        departure: FlightWaypoint,
        arrival: FlightWaypoint,
        divert: FlightWaypoint | None,
        bullseye: FlightWaypoint,
        nav_to: list[FlightWaypoint],
        nav_from: list[FlightWaypoint],
        patrol_start: FlightWaypoint,
        patrol_end: FlightWaypoint,
        patrol_duration: timedelta,
        patrol_speed: Speed,
        engagement_distance: Distance,
    ) -> None:
        super().__init__(flight, departure, arrival, divert, bullseye)
        self.nav_to = nav_to
        self.nav_from = nav_from
        self.patrol_start = patrol_start
        self.patrol_end = patrol_end

        # Maximum time to remain on station.
        self.patrol_duration = patrol_duration

        # Racetrack speed TAS.
        self.patrol_speed = patrol_speed

        # The engagement range of any Search Then Engage task, or the radius of a
        # Search Then Engage in Zone task. Any enemies of the appropriate type for
        # this mission within this range of the flight's current position (or the
        # center of the zone) will be engaged by the flight.
        self.engagement_distance = engagement_distance

    @property
    def patrol_start_time(self) -> timedelta:
        return self.package.time_over_target

    @property
    def patrol_end_time(self) -> timedelta:
        # TODO: This is currently wrong for CAS.
        # CAS missions end when they're winchester or bingo. We need to
        # configure push tasks for the escorts rather than relying on timing.
        return self.patrol_start_time + self.patrol_duration

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.patrol_start:
            return self.patrol_start_time
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.patrol_end:
            return self.patrol_end_time
        return None

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to
        yield self.patrol_start
        yield self.patrol_end
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    @property
    def package_speed_waypoints(self) -> set[FlightWaypoint]:
        return {self.patrol_start, self.patrol_end}

    @property
    def tot_waypoint(self) -> FlightWaypoint | None:
        return self.patrol_start

    @property
    def mission_departure_time(self) -> timedelta:
        return self.patrol_end_time

    @self_type_guard
    def is_patrol(self, flight_plan: FlightPlan) -> TypeGuard[PatrollingFlightPlan]:
        return True
