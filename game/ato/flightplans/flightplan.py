"""Flight plan generation.

Flights are first planned generically by either the player or by the
MissionPlanner. Those only plan basic information like the objective, aircraft
type, and the size of the flight. The FlightPlanBuilder is responsible for
generating the waypoints for the mission.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Generic, TYPE_CHECKING, TypeGuard, TypeVar

from game.typeguard import self_type_guard
from game.utils import Distance, Speed, meters
from .planningerror import PlanningError
from ..flightwaypointtype import FlightWaypointType
from ..starttype import StartType
from ..traveltime import GroundSpeed

if TYPE_CHECKING:
    from game.theater import ControlPoint
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint
    from ..package import Package
    from .formation import FormationFlightPlan
    from .loiter import LoiterFlightPlan
    from .patrolling import PatrollingFlightPlan


@dataclass(frozen=True)
class Layout(ABC):
    departure: FlightWaypoint

    @property
    def waypoints(self) -> list[FlightWaypoint]:
        """A list of all waypoints in the flight plan, in order."""
        return list(self.iter_waypoints())

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        """Iterates over all waypoints in the flight plan, in order."""
        raise NotImplementedError


LayoutT = TypeVar("LayoutT", bound=Layout)


class FlightPlan(ABC, Generic[LayoutT]):
    def __init__(self, flight: Flight, layout: LayoutT) -> None:
        self.flight = flight
        self.layout = layout
        self.tot_offset = self.default_tot_offset()

    @property
    def package(self) -> Package:
        return self.flight.package

    @property
    def waypoints(self) -> list[FlightWaypoint]:
        """A list of all waypoints in the flight plan, in order."""
        return list(self.iter_waypoints())

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        """Iterates over all waypoints in the flight plan, in order."""
        yield from self.layout.iter_waypoints()

    def edges(
        self, until: FlightWaypoint | None = None
    ) -> Iterator[tuple[FlightWaypoint, FlightWaypoint]]:
        """A list of all paths between waypoints, in order."""
        waypoints = self.waypoints
        if until is None:
            last_index = len(waypoints)
        else:
            last_index = waypoints.index(until) + 1

        return zip(self.waypoints[:last_index], self.waypoints[1:last_index])

    def best_speed_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> Speed:
        """Desired ground speed between points a and b."""
        factor = 1.0
        if b.waypoint_type == FlightWaypointType.ASCEND_POINT:
            # Flights that start airborne already have some altitude and a good
            # amount of speed.
            factor = 0.5
        elif b.waypoint_type == FlightWaypointType.LOITER:
            # On the way to the hold point the AI won't climb unless they're in
            # formation, so slowing down the flight lead gives them more time to
            # form up and climb.
            # https://forums.eagle.ru/forum/english/digital-combat-simulator/dcs-world-2-5/dcs-wishlist-aa/7121300-ai-flights-will-not-climb-to-hold-point-because-wingman-not-joined
            #
            # Plus, it's a loiter point so there's no reason to hurry.
            factor = 0.75
        # TODO: Adjust if AGL.
        # We don't have an exact heightmap, but we should probably be performing
        # *some* adjustment for NTTR since the minimum altitude of the map is
        # near 2000 ft MSL.
        return GroundSpeed.for_flight(self.flight, min(a.alt, b.alt)) * factor

    def speed_between_waypoints(self, a: FlightWaypoint, b: FlightWaypoint) -> Speed:
        return self.best_speed_between_waypoints(a, b)

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return set()

    def fuel_consumption_between_points(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> float | None:
        ppm = self.fuel_rate_to_between_points(a, b)
        if ppm is None:
            return None
        distance = meters(a.position.distance_to_point(b.position))
        return distance.nautical_miles * ppm

    def fuel_rate_to_between_points(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> float | None:
        if self.flight.unit_type.fuel_consumption is None:
            return None
        if a.waypoint_type is FlightWaypointType.TAKEOFF:
            return self.flight.unit_type.fuel_consumption.climb
        if b in self.combat_speed_waypoints:
            return self.flight.unit_type.fuel_consumption.combat
        return self.flight.unit_type.fuel_consumption.cruise

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        """The waypoint that is associated with the package TOT, or None.

        Note that the only flight plans that should have no target waypoints are
        user-planned missions without any useful waypoints and flight plans that
        failed to generate. Nevertheless, we have to defend against it.
        """
        raise NotImplementedError

    @property
    def tot(self) -> datetime:
        return self.package.time_over_target + self.tot_offset

    def max_distance_from(self, cp: ControlPoint) -> Distance:
        """Returns the farthest waypoint of the flight plan from a ControlPoint.
        :arg cp The ControlPoint to measure distance from.
        """
        if not self.waypoints:
            return meters(0)
        return max(
            [meters(cp.position.distance_to_point(w.position)) for w in self.waypoints]
        )

    def default_tot_offset(self) -> timedelta:
        """This flight's offset from the package's TOT.

        Positive values represent later TOTs. An offset of -2 minutes is used
        for a flight that has a TOT 2 minutes before the rest of the package.
        """
        return timedelta()

    def _travel_time_to_waypoint(self, destination: FlightWaypoint) -> timedelta:
        total = timedelta()

        if destination not in self.waypoints:
            raise PlanningError(
                f"Did not find destination waypoint {destination} in "
                f"waypoints for {self.flight}"
            )

        for previous_waypoint, waypoint in self.edges(until=destination):
            total += self.total_time_between_waypoints(previous_waypoint, waypoint)

        # Trim microseconds. Our simulation tick rate is 1 second, so anything that
        # takes 100.1 or 100.9 seconds will take 100 seconds. DCS doesn't handle
        # sub-second resolution for tasks anyway, nor are they interesting from a
        # mission planning perspective, so there's little value to keeping them in the
        # model.
        return timedelta(seconds=math.floor(total.total_seconds()))

    def total_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        """Returns the total time spent between a and b.

        The total time between waypoints differs from the travel time in that it may
        include additional time for actions such as loitering.
        """
        return self.travel_time_between_waypoints(a, b)

    def travel_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        error_factor = 1.05
        speed = self.speed_between_waypoints(a, b)
        distance = meters(a.position.distance_to_point(b.position))
        return timedelta(hours=distance.nautical_miles / speed.knots * error_factor)

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        raise NotImplementedError

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        raise NotImplementedError

    def request_escort_at(self) -> FlightWaypoint | None:
        try:
            return next(self.escorted_waypoints())
        except StopIteration:
            return None

    def dismiss_escort_at(self) -> FlightWaypoint | None:
        try:
            return list(self.escorted_waypoints())[-1]
        except IndexError:
            return None

    def escorted_waypoints(self) -> Iterator[FlightWaypoint]:
        for waypoint in self.iter_waypoints():
            if waypoint.wants_escort:
                yield waypoint

    def takeoff_time(self) -> datetime:
        return self.tot - self._travel_time_to_waypoint(self.tot_waypoint)

    def minimum_duration_from_start_to_tot(self) -> timedelta:
        return (
            self._travel_time_to_waypoint(self.tot_waypoint)
            + self.estimate_startup()
            + self.estimate_ground_ops()
        )

    def startup_time(self) -> datetime:
        return (
            self.takeoff_time() - self.estimate_startup() - self.estimate_ground_ops()
        )

    def estimate_startup(self) -> timedelta:
        if self.flight.start_type is StartType.COLD:
            if self.flight.client_count:
                return timedelta(minutes=10)
            else:
                # The AI doesn't seem to have a real startup procedure.
                return timedelta(minutes=2)
        return timedelta()

    def estimate_ground_ops(self) -> timedelta:
        if self.flight.start_type in {StartType.RUNWAY, StartType.IN_FLIGHT}:
            return timedelta()
        if self.flight.departure.is_fleet:
            return timedelta(minutes=2)
        else:
            return timedelta(minutes=8)

    @property
    @abstractmethod
    def mission_begin_on_station_time(self) -> datetime | None:
        """The time that the mission is first on-station.

        Not all mission types will have a time when they can be considered on-station.
        Missions that patrol or loiter (CAPs, CAS, refueling, AEW&C, etc) will have this
        defined, but strike-like missions will not.
        """

    @property
    def mission_departure_time(self) -> datetime:
        """The time that the mission is complete and the flight RTBs."""
        raise NotImplementedError

    @self_type_guard
    def is_loiter(
        self, flight_plan: FlightPlan[Any]
    ) -> TypeGuard[LoiterFlightPlan[Any]]:
        return False

    @self_type_guard
    def is_patrol(
        self, flight_plan: FlightPlan[Any]
    ) -> TypeGuard[PatrollingFlightPlan[Any]]:
        return False

    @self_type_guard
    def is_formation(
        self, flight_plan: FlightPlan[Any]
    ) -> TypeGuard[FormationFlightPlan[Any]]:
        return False

    def add_waypoint_actions(self) -> None:
        pass
