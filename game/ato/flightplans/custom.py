from __future__ import annotations

from collections.abc import Iterator
from datetime import timedelta
from typing import TYPE_CHECKING, Type

from .flightplan import FlightPlan
from .ibuilder import IBuilder
from ..flightwaypointtype import FlightWaypointType

if TYPE_CHECKING:
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint


class Builder(IBuilder):
    def build(self) -> CustomFlightPlan:
        return CustomFlightPlan(self.flight, [])


class CustomFlightPlan(FlightPlan):
    def __init__(self, flight: Flight, waypoints: list[FlightWaypoint]) -> None:
        super().__init__(flight)
        self.custom_waypoints = waypoints

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield from self.custom_waypoints

    @property
    def tot_waypoint(self) -> FlightWaypoint | None:
        target_types = (
            FlightWaypointType.PATROL_TRACK,
            FlightWaypointType.TARGET_GROUP_LOC,
            FlightWaypointType.TARGET_POINT,
            FlightWaypointType.TARGET_SHIP,
        )
        for waypoint in self.waypoints:
            if waypoint in target_types:
                return waypoint
        return None

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.tot_waypoint:
            return self.package.time_over_target
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        return None

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target
