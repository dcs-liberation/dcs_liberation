from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Type

from game.theater import FrontLine
from game.utils import Distance, Speed, kph, meters, dcs_to_shapely_point
from .ibuilder import IBuilder
from .invalidobjectivelocation import InvalidObjectiveLocation
from .patrolling import PatrollingFlightPlan, PatrollingLayout
from .uizonedisplay import UiZone, UiZoneDisplay
from .waypointbuilder import WaypointBuilder
from ..flightwaypointtype import FlightWaypointType
from ...flightplan.ipsolver import IpSolver
from ...persistence.paths import waypoint_debug_directory

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class CasLayout(PatrollingLayout):
    ingress: FlightWaypoint

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to
        yield self.ingress
        yield self.patrol_start
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
        return self.flight.coalition.doctrine.cas.duration

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
        return {self.layout.ingress, self.layout.patrol_start, self.layout.patrol_end}

    def ui_zone(self) -> UiZone:
        midpoint = (
            self.layout.patrol_start.position + self.layout.patrol_end.position
        ) / 2
        return UiZone(
            [midpoint],
            self.engagement_distance,
        )


class Builder(IBuilder[CasFlightPlan, CasLayout]):
    def layout(self, dump_debug_info: bool) -> CasLayout:
        location = self.package.target

        if not isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        from game.missiongenerator.frontlineconflictdescription import (
            FrontLineConflictDescription,
        )

        bounds = FrontLineConflictDescription.frontline_bounds(location, self.theater)
        patrol_start = bounds.left_position
        patrol_end = bounds.right_position

        start_distance = patrol_start.distance_to_point(self.flight.departure.position)
        end_distance = patrol_end.distance_to_point(self.flight.departure.position)
        if end_distance < start_distance:
            patrol_start, patrol_end = patrol_end, patrol_start

        builder = WaypointBuilder(self.flight, self.coalition)

        is_helo = self.flight.unit_type.dcs_unit_type.helicopter
        patrol_altitude = self.doctrine.resolve_combat_altitude(is_helo)
        use_agl_patrol_altitude = is_helo

        ip_solver = IpSolver(
            dcs_to_shapely_point(self.flight.departure.position),
            dcs_to_shapely_point(patrol_start),
            self.doctrine,
            self.threat_zones.all,
        )
        ip_solver.set_debug_properties(
            waypoint_debug_directory() / "IP", self.theater.terrain
        )
        ingress_point_shapely = ip_solver.solve()
        if dump_debug_info:
            ip_solver.dump_debug_info()

        ingress_point = patrol_start.new_in_same_map(
            ingress_point_shapely.x, ingress_point_shapely.y
        )

        patrol_start_waypoint = builder.nav(
            patrol_start, patrol_altitude, use_agl_patrol_altitude
        )
        patrol_start_waypoint.name = "FLOT START"
        patrol_start_waypoint.pretty_name = "FLOT start"
        patrol_start_waypoint.description = "FLOT boundary"
        patrol_start_waypoint.wants_escort = True

        patrol_end_waypoint = builder.nav(
            patrol_end, patrol_altitude, use_agl_patrol_altitude
        )
        patrol_end_waypoint.name = "FLOT END"
        patrol_end_waypoint.pretty_name = "FLOT end"
        patrol_end_waypoint.description = "FLOT boundary"
        patrol_end_waypoint.wants_escort = True

        ingress = builder.ingress(
            FlightWaypointType.INGRESS_CAS, ingress_point, location
        )
        ingress.description = f"Ingress to provide CAS at {location}"

        return CasLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position,
                ingress_point,
                patrol_altitude,
                use_agl_patrol_altitude,
            ),
            nav_from=builder.nav_path(
                patrol_end,
                self.flight.arrival.position,
                patrol_altitude,
                use_agl_patrol_altitude,
            ),
            ingress=ingress,
            patrol_start=patrol_start_waypoint,
            patrol_end=patrol_end_waypoint,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self, dump_debug_info: bool = False) -> CasFlightPlan:
        return CasFlightPlan(self.flight, self.layout(dump_debug_info))
