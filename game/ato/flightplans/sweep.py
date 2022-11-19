from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Iterator, TYPE_CHECKING, Type

from dcs import Point

from game.utils import Heading
from .ibuilder import IBuilder
from .loiter import LoiterFlightPlan, LoiterLayout
from .waypointbuilder import WaypointBuilder
from ..traveltime import GroundSpeed, TravelTime
from ...flightplan import HoldZoneGeometry

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class SweepLayout(LoiterLayout):
    nav_to: list[FlightWaypoint]
    sweep_start: FlightWaypoint
    sweep_end: FlightWaypoint
    nav_from: list[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield self.hold
        yield from self.nav_to
        yield self.sweep_start
        yield self.sweep_end
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class SweepFlightPlan(LoiterFlightPlan):
    @property
    def lead_time(self) -> timedelta:
        return timedelta(minutes=5)

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return {self.layout.sweep_end}

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        return self.layout.sweep_end

    @property
    def tot_offset(self) -> timedelta:
        return -self.lead_time

    @property
    def sweep_start_time(self) -> timedelta:
        travel_time = self.travel_time_between_waypoints(
            self.layout.sweep_start, self.layout.sweep_end
        )
        return self.sweep_end_time - travel_time

    @property
    def sweep_end_time(self) -> timedelta:
        return self.tot

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.layout.sweep_start:
            return self.sweep_start_time
        if waypoint == self.layout.sweep_end:
            return self.sweep_end_time
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.layout.hold:
            return self.push_time
        return None

    @property
    def push_time(self) -> timedelta:
        return self.sweep_end_time - TravelTime.between_points(
            self.layout.hold.position,
            self.layout.sweep_end.position,
            GroundSpeed.for_flight(self.flight, self.layout.hold.alt),
        )

    def mission_departure_time(self) -> timedelta:
        return self.sweep_end_time


class Builder(IBuilder[SweepFlightPlan, SweepLayout]):
    def layout(self) -> SweepLayout:
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

        return SweepLayout(
            departure=builder.takeoff(self.flight.departure),
            hold=hold,
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

    def build(self) -> SweepFlightPlan:
        return SweepFlightPlan(self.flight, self.layout())
