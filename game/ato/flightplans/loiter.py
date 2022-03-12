from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, TYPE_CHECKING, TypeGuard

from game.typeguard import self_type_guard
from .flightplan import FlightPlan
from .standard import StandardFlightPlan, StandardLayout

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class LoiterLayout(StandardLayout, ABC):
    hold: FlightWaypoint


class LoiterFlightPlan(StandardFlightPlan[Any], ABC):
    @property
    def hold_duration(self) -> timedelta:
        return timedelta(minutes=5)

    @property
    @abstractmethod
    def push_time(self) -> timedelta:
        ...

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.layout.hold:
            return self.push_time
        return None

    def travel_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        travel_time = super().travel_time_between_waypoints(a, b)
        if a != self.layout.hold:
            return travel_time
        return travel_time + self.hold_duration

    @self_type_guard
    def is_loiter(self, flight_plan: FlightPlan[Any]) -> TypeGuard[LoiterFlightPlan]:
        return True
