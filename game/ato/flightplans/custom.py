from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Type

from .flightplan import FlightPlan, Layout
from .ibuilder import IBuilder
from .waypointbuilder import WaypointBuilder
from .. import Flight
from ..flightwaypointtype import FlightWaypointType

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class CustomLayout(Layout):
    custom_waypoints: list[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.custom_waypoints


class CustomFlightPlan(FlightPlan[CustomLayout]):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        target_types = (
            FlightWaypointType.PATROL_TRACK,
            FlightWaypointType.TARGET_GROUP_LOC,
            FlightWaypointType.TARGET_POINT,
            FlightWaypointType.TARGET_SHIP,
        )
        for waypoint in self.waypoints:
            if waypoint in target_types:
                return waypoint
        return self.layout.departure

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.tot_waypoint:
            return self.package.time_over_target
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        return None

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target


class Builder(IBuilder[CustomFlightPlan, CustomLayout]):
    def __init__(
        self, flight: Flight, waypoints: list[FlightWaypoint] | None = None
    ) -> None:
        super().__init__(flight)
        if waypoints is None:
            waypoints = []
        self.waypoints = waypoints

    def layout(self) -> CustomLayout:
        builder = WaypointBuilder(self.flight, self.coalition)
        return CustomLayout(builder.takeoff(self.flight.departure), self.waypoints)

    def build(self) -> CustomFlightPlan:
        return CustomFlightPlan(self.flight, self.layout())
