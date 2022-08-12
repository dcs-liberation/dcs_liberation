from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Type

from .flightplan import FlightPlan, Layout
from .ibuilder import IBuilder
from .ischeduler import IScheduler
from ..flightwaypointtype import FlightWaypointType

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class CustomLayout(Layout):
    custom_waypoints: list[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield from self.custom_waypoints


class Builder(IBuilder[CustomLayout]):
    def build(self) -> CustomLayout:
        return CustomLayout([])


class Scheduler(IScheduler[CustomLayout]):
    def schedule(self) -> CustomFlightPlan:
        return CustomFlightPlan(self.flight, self.layout)


class CustomFlightPlan(FlightPlan[CustomLayout]):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @staticmethod
    def scheduler_type() -> Type[Scheduler]:
        return Scheduler

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
