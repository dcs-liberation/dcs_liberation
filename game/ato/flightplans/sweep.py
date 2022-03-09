from __future__ import annotations

from datetime import timedelta
from typing import Iterator, TYPE_CHECKING, Type

from dcs import Point

from game.utils import Heading
from .ibuilder import IBuilder
from .loiter import LoiterFlightPlan
from .waypointbuilder import WaypointBuilder
from ..traveltime import GroundSpeed, TravelTime
from ...flightplan import HoldZoneGeometry

if TYPE_CHECKING:
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint


class Builder(IBuilder):
    def build(self) -> SweepFlightPlan:
        assert self.package.waypoints is not None
        target = self.package.target.position
        heading = Heading.from_degrees(
            self.package.waypoints.join.heading_between_point(target)
        )
        start_pos = target.point_from_heading(
            heading.degrees, -self.doctrine.sweep_distance.meters
        )

        builder = WaypointBuilder(self.flight, self.coalition)
        start, end = builder.sweep(start_pos, target, self.doctrine.ingress_altitude)

        hold = builder.hold(self._hold_point())

        refuel = None

        if self.package.waypoints is not None:
            refuel = builder.refuel(self.package.waypoints.refuel)

        return SweepFlightPlan(
            flight=self.flight,
            lead_time=timedelta(minutes=5),
            departure=builder.takeoff(self.flight.departure),
            hold=hold,
            hold_duration=timedelta(minutes=5),
            nav_to=builder.nav_path(
                hold.position, start.position, self.doctrine.ingress_altitude
            ),
            nav_from=builder.nav_path(
                end.position,
                self.flight.arrival.position,
                self.doctrine.ingress_altitude,
            ),
            sweep_start=start,
            sweep_end=end,
            refuel=refuel,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def _hold_point(self) -> Point:
        assert self.package.waypoints is not None
        origin = self.flight.departure.position
        target = self.package.target.position
        join = self.package.waypoints.join
        ip = self.package.waypoints.ingress
        return HoldZoneGeometry(
            target, origin, ip, join, self.coalition, self.theater
        ).find_best_hold_point()


class SweepFlightPlan(LoiterFlightPlan):
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
        sweep_start: FlightWaypoint,
        sweep_end: FlightWaypoint,
        refuel: FlightWaypoint,
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
            hold,
            hold_duration,
        )
        self.sweep_start = sweep_start
        self.sweep_end = sweep_end
        self.refuel = refuel
        self.lead_time = lead_time

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield self.hold
        yield from self.nav_to
        yield self.sweep_start
        yield self.sweep_end
        if self.refuel is not None:
            yield self.refuel
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return {self.sweep_end}

    @property
    def tot_waypoint(self) -> FlightWaypoint | None:
        return self.sweep_end

    @property
    def tot_offset(self) -> timedelta:
        return -self.lead_time

    @property
    def sweep_start_time(self) -> timedelta:
        travel_time = self.travel_time_between_waypoints(
            self.sweep_start, self.sweep_end
        )
        return self.sweep_end_time - travel_time

    @property
    def sweep_end_time(self) -> timedelta:
        return self.tot

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.sweep_start:
            return self.sweep_start_time
        if waypoint == self.sweep_end:
            return self.sweep_end_time
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.hold:
            return self.push_time
        return None

    @property
    def push_time(self) -> timedelta:
        return self.sweep_end_time - TravelTime.between_points(
            self.hold.position,
            self.sweep_end.position,
            GroundSpeed.for_flight(self.flight, self.hold.alt),
        )

    def mission_departure_time(self) -> timedelta:
        return self.sweep_end_time
