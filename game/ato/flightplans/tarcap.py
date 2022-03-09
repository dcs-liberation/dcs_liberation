from __future__ import annotations

import random
from collections.abc import Iterator
from datetime import timedelta
from typing import TYPE_CHECKING, Type

from game.utils import Distance, Speed, feet
from .capbuilder import CapBuilder
from .patrolling import PatrollingFlightPlan
from .waypointbuilder import WaypointBuilder

if TYPE_CHECKING:
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint


class Builder(CapBuilder):
    def build(self) -> TarCapFlightPlan:
        location = self.package.target

        preferred_alt = self.flight.unit_type.preferred_patrol_altitude
        randomized_alt = preferred_alt + feet(random.randint(-2, 1) * 1000)
        patrol_alt = max(
            self.doctrine.min_patrol_altitude,
            min(self.doctrine.max_patrol_altitude, randomized_alt),
        )
        patrol_speed = self.flight.unit_type.preferred_patrol_speed(patrol_alt)

        builder = WaypointBuilder(self.flight, self.coalition)
        orbit0p, orbit1p = self.cap_racetrack_for_objective(location, barcap=False)

        start, end = builder.race_track(orbit0p, orbit1p, patrol_alt)

        refuel = None

        if self.package.waypoints is not None:
            refuel = builder.refuel(self.package.waypoints.refuel)

        return TarCapFlightPlan(
            flight=self.flight,
            lead_time=timedelta(minutes=2),
            # Note that this duration only has an effect if there are no
            # flights in the package that have requested escort. If the package
            # requests an escort the CAP self.flight will remain on station for the
            # duration of the escorted mission, or until it is winchester/bingo.
            patrol_duration=self.doctrine.cap_duration,
            patrol_speed=patrol_speed,
            engagement_distance=self.doctrine.cap_engagement_range,
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position, orbit0p, patrol_alt
            ),
            nav_from=builder.nav_path(
                orbit1p, self.flight.arrival.position, patrol_alt
            ),
            patrol_start=start,
            patrol_end=end,
            refuel=refuel,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )


class TarCapFlightPlan(PatrollingFlightPlan):
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
        refuel: FlightWaypoint | None,
        lead_time: timedelta,
    ) -> None:
        super().__init__(
            flight,
            departure,
            arrival,
            divert,
            bullseye,
            nav_to,
            nav_from,
            patrol_start,
            patrol_end,
            patrol_duration,
            patrol_speed,
            engagement_distance,
        )
        self.refuel = refuel
        self.lead_time = lead_time

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to
        yield self.patrol_start
        yield self.patrol_end
        if self.refuel is not None:
            yield self.refuel
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return {self.patrol_start, self.patrol_end}

    @property
    def tot_offset(self) -> timedelta:
        return -self.lead_time

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.patrol_end:
            return self.patrol_end_time
        return super().depart_time_for_waypoint(waypoint)

    @property
    def patrol_start_time(self) -> timedelta:
        start = self.package.escort_start_time
        if start is not None:
            return start + self.tot_offset
        return self.tot

    @property
    def patrol_end_time(self) -> timedelta:
        end = self.package.escort_end_time
        if end is not None:
            return end
        return super().patrol_end_time
