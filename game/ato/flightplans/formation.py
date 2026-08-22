from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import cached_property
from typing import Any, TYPE_CHECKING, TypeGuard, TypeVar

from game.typeguard import self_type_guard
from game.utils import Speed
from .flightplan import FlightPlan
from .loiter import LoiterFlightPlan, LoiterLayout

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class FormationLayout(LoiterLayout, ABC):
    nav_to: list[FlightWaypoint]
    pre_refuel: FlightWaypoint | None
    join: FlightWaypoint
    split: FlightWaypoint
    refuel: FlightWaypoint
    nav_from: list[FlightWaypoint]


LayoutT = TypeVar("LayoutT", bound=FormationLayout)


class FormationFlightPlan(LoiterFlightPlan[LayoutT], ABC):
    @property
    @abstractmethod
    def package_speed_waypoints(self) -> set[FlightWaypoint]: ...

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return self.package_speed_waypoints

    @cached_property
    def best_flight_formation_speed(self) -> Speed:
        """The best speed this flight is capable at all formation waypoints.

        To ease coordination with other flights, we aim to have a single mission
        speed used by the formation for all waypoints. As such, this function
        returns the highest ground speed that the flight is capable of flying at
        all of its formation waypoints.
        """
        speeds = []
        for previous_waypoint, waypoint in self.edges():
            if waypoint in self.package_speed_waypoints:
                speeds.append(
                    self.best_speed_between_waypoints(previous_waypoint, waypoint)
                )
        return min(speeds)

    def speed_between_waypoints(self, a: FlightWaypoint, b: FlightWaypoint) -> Speed:
        if b in self.package_speed_waypoints:
            # Should be impossible, as any package with at least one
            # FormationFlightPlan flight needs a formation speed.
            assert self.package.formation_speed is not None
            return self.package.formation_speed
        return super().speed_between_waypoints(a, b)

    @property
    def travel_time_to_rendezvous(self) -> timedelta:
        """The estimated time between the first waypoint and the join point."""
        return self._travel_time_to_waypoint(self.layout.join)

    @property
    @abstractmethod
    def join_time(self) -> datetime: ...

    @property
    @abstractmethod
    def split_time(self) -> datetime: ...

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        if waypoint == self.layout.pre_refuel:
            return self.pre_refuel_arrival_time
        if waypoint == self.layout.join:
            return self.join_time
        elif waypoint == self.layout.split:
            return self.split_time
        return None

    @property
    def pre_refuel_duration(self) -> timedelta:
        if self.layout.pre_refuel is None:
            return timedelta()
        return self.flight.coalition.game.settings.pre_mission_aar_hold_duration

    @property
    def pre_refuel_push_time(self) -> datetime | None:
        if self.layout.pre_refuel is None:
            return None
        return self.push_time - self.total_time_between_waypoints(
            self.layout.pre_refuel, self.layout.join
        )

    @property
    def pre_refuel_arrival_time(self) -> datetime | None:
        if self.layout.pre_refuel is None:
            return None
        push_time = self.pre_refuel_push_time
        if push_time is None:
            return None
        return push_time - self.pre_refuel_duration

    @property
    def push_time(self) -> datetime:
        return self.join_time - self.travel_time_between_waypoints(
            self.layout.hold, self.layout.join
        )

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        if waypoint == self.layout.pre_refuel:
            return self.pre_refuel_push_time
        return super().depart_time_for_waypoint(waypoint)

    def total_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        travel_time = super().total_time_between_waypoints(a, b)
        if a != self.layout.pre_refuel:
            return travel_time
        return travel_time + self.pre_refuel_duration

    @property
    def mission_begin_on_station_time(self) -> datetime | None:
        return None

    @property
    def mission_departure_time(self) -> datetime:
        return self.split_time

    def provide_pre_refuel_push_time(self) -> datetime:
        push_time = self.pre_refuel_push_time
        assert push_time is not None
        return push_time

    def add_waypoint_actions(self) -> None:
        super().add_waypoint_actions()
        if self.layout.pre_refuel is None:
            return
        from game.flightplan.waypointactions.hold import Hold

        pre_refuel = self.layout.pre_refuel
        speed = self.flight.unit_type.patrol_speed
        if speed is None:
            speed = Speed.from_mach(0.6, pre_refuel.alt)
        pre_refuel.add_action(
            Hold(self.provide_pre_refuel_push_time, pre_refuel.alt, speed)
        )

    @self_type_guard
    def is_formation(
        self, flight_plan: FlightPlan[Any]
    ) -> TypeGuard[FormationFlightPlan[Any]]:
        return True
