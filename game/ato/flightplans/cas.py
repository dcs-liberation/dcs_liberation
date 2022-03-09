from __future__ import annotations

from collections.abc import Iterator
from datetime import timedelta
from typing import TYPE_CHECKING, Type

from game.theater import FrontLine
from game.utils import Distance, Speed, meters
from .ibuilder import IBuilder
from .invalidobjectivelocation import InvalidObjectiveLocation
from .patrolling import PatrollingFlightPlan
from .waypointbuilder import WaypointBuilder
from ..flightwaypointtype import FlightWaypointType

if TYPE_CHECKING:
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint


class Builder(IBuilder):
    def build(self) -> CasFlightPlan:
        location = self.package.target

        if not isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        from game.missiongenerator.frontlineconflictdescription import (
            FrontLineConflictDescription,
        )

        ingress, heading, distance = FrontLineConflictDescription.frontline_vector(
            location, self.theater
        )
        center = ingress.point_from_heading(heading.degrees, distance / 2)
        egress = ingress.point_from_heading(heading.degrees, distance)

        ingress_distance = ingress.distance_to_point(self.flight.departure.position)
        egress_distance = egress.distance_to_point(self.flight.departure.position)
        if egress_distance < ingress_distance:
            ingress, egress = egress, ingress

        builder = WaypointBuilder(self.flight, self.coalition)

        # 2021-08-02: patrol_speed will currently have no effect because
        # CAS doesn't use OrbitAction. But all PatrollingFlightPlan are expected
        # to have patrol_speed
        is_helo = self.flight.unit_type.dcs_unit_type.helicopter
        ingress_egress_altitude = (
            self.doctrine.ingress_altitude if not is_helo else meters(50)
        )
        patrol_speed = self.flight.unit_type.preferred_patrol_speed(
            ingress_egress_altitude
        )
        use_agl_ingress_egress = is_helo

        from game.missiongenerator.frontlineconflictdescription import FRONTLINE_LENGTH

        return CasFlightPlan(
            flight=self.flight,
            patrol_duration=self.doctrine.cas_duration,
            patrol_speed=patrol_speed,
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position,
                ingress,
                ingress_egress_altitude,
                use_agl_ingress_egress,
            ),
            nav_from=builder.nav_path(
                egress,
                self.flight.arrival.position,
                ingress_egress_altitude,
                use_agl_ingress_egress,
            ),
            patrol_start=builder.ingress(
                FlightWaypointType.INGRESS_CAS, ingress, location
            ),
            engagement_distance=meters(FRONTLINE_LENGTH) / 2,
            target=builder.cas(center),
            patrol_end=builder.egress(egress, location),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )


class CasFlightPlan(PatrollingFlightPlan):
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
        target: FlightWaypoint,
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
        self.target = target

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to
        yield self.patrol_start
        yield self.target
        yield self.patrol_end
        yield from self.nav_from
        yield self.departure
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return {self.patrol_start, self.target, self.patrol_end}

    def request_escort_at(self) -> FlightWaypoint | None:
        return self.patrol_start

    def dismiss_escort_at(self) -> FlightWaypoint | None:
        return self.patrol_end
