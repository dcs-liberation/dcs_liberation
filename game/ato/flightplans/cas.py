from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Type

from game.theater import FrontLine
from game.utils import Distance, Speed, kph, meters
from .ibuilder import IBuilder
from .invalidobjectivelocation import InvalidObjectiveLocation
from .patrolling import PatrollingFlightPlan, PatrollingLayout
from .uizonedisplay import UiZone, UiZoneDisplay
from .waypointbuilder import WaypointBuilder
from ..flightwaypointtype import FlightWaypointType

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class CasLayout(PatrollingLayout):
    target: FlightWaypoint

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to
        yield self.patrol_start
        yield self.target
        yield self.patrol_end
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class CasFlightPlan(PatrollingFlightPlan[CasLayout], UiZoneDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def patrol_duration(self) -> timedelta:
        return self.flight.coalition.doctrine.cas_duration

    @property
    def patrol_speed(self) -> Speed:
        # 2021-08-02: patrol_speed will currently have no effect because
        # CAS doesn't use OrbitAction. But all PatrollingFlightPlan are expected
        # to have patrol_speed
        return kph(0)

    @property
    def engagement_distance(self) -> Distance:
        from game.missiongenerator.frontlineconflictdescription import FRONTLINE_LENGTH

        return meters(FRONTLINE_LENGTH) / 2

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return {self.layout.patrol_start, self.layout.target, self.layout.patrol_end}

    def request_escort_at(self) -> FlightWaypoint | None:
        return self.layout.patrol_start

    def dismiss_escort_at(self) -> FlightWaypoint | None:
        return self.layout.patrol_end

    def ui_zone(self) -> UiZone:
        return UiZone(
            [self.layout.target.position],
            self.engagement_distance,
        )


class Builder(IBuilder[CasFlightPlan, CasLayout]):
    def layout(self) -> CasLayout:
        location = self.package.target

        if not isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        from game.missiongenerator.frontlineconflictdescription import (
            FrontLineConflictDescription,
        )

        bounds = FrontLineConflictDescription.frontline_bounds(location, self.theater)
        ingress = bounds.left_position
        center = bounds.center
        egress = bounds.right_position

        ingress_distance = ingress.distance_to_point(self.flight.departure.position)
        egress_distance = egress.distance_to_point(self.flight.departure.position)
        if egress_distance < ingress_distance:
            ingress, egress = egress, ingress

        builder = WaypointBuilder(self.flight, self.coalition)

        is_helo = self.flight.unit_type.dcs_unit_type.helicopter
        ingress_egress_altitude = (
            self.doctrine.ingress_altitude if not is_helo else meters(50)
        )
        use_agl_ingress_egress = is_helo

        return CasLayout(
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
            target=builder.cas(center),
            patrol_end=builder.egress(egress, location),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self) -> CasFlightPlan:
        return CasFlightPlan(self.flight, self.layout())
