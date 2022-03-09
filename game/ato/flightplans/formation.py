from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import timedelta
from functools import cached_property
from typing import TYPE_CHECKING, TypeGuard

from game.typeguard import self_type_guard
from game.utils import Speed
from .flightplan import FlightPlan
from .loiter import LoiterFlightPlan
from ..traveltime import GroundSpeed, TravelTime

if TYPE_CHECKING:
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint


class FormationFlightPlan(LoiterFlightPlan, ABC):
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
        join: FlightWaypoint,
        split: FlightWaypoint,
        refuel: FlightWaypoint,
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
        self.join = join
        self.split = split
        self.refuel = refuel

    @property
    @abstractmethod
    def package_speed_waypoints(self) -> set[FlightWaypoint]:
        ...

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return self.package_speed_waypoints

    def request_escort_at(self) -> FlightWaypoint | None:
        return self.join

    def dismiss_escort_at(self) -> FlightWaypoint | None:
        return self.split

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
        return self._travel_time_to_waypoint(self.join)

    @property
    @abstractmethod
    def join_time(self) -> timedelta:
        ...

    @property
    @abstractmethod
    def split_time(self) -> timedelta:
        ...

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.join:
            return self.join_time
        elif waypoint == self.split:
            return self.split_time
        return None

    @property
    def push_time(self) -> timedelta:
        return self.join_time - TravelTime.between_points(
            self.hold.position,
            self.join.position,
            GroundSpeed.for_flight(self.flight, self.hold.alt),
        )

    @property
    def mission_departure_time(self) -> timedelta:
        return self.split_time

    @self_type_guard
    def is_formation(self, flight_plan: FlightPlan) -> TypeGuard[FormationFlightPlan]:
        return True
