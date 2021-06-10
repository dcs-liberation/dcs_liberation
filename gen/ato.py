"""Air Tasking Orders.

The classes of the Air Tasking Order (ATO) define all of the missions that have
been planned, and which aircraft have been assigned to them. Each planned
mission, or "package" is composed of individual flights. The package may contain
dissimilar aircraft performing different roles, but all for the same goal. For
example, the package to strike an enemy airfield may contain an escort flight,
a SEAD flight, and the strike aircraft themselves. CAP packages may contain only
the single CAP flight.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Dict, List, Optional

from dcs.mapping import Point

from game.theater.missiontarget import MissionTarget
from game.utils import Speed
from .flights.flight import Flight, FlightType
from .flights.flightplan import FormationFlightPlan
from .flights.traveltime import TotEstimator


@dataclass(frozen=True)
class Task:
    """The main task of a flight or package."""

    #: The type of task.
    task_type: FlightType

    #: The location of the objective.
    location: str


@dataclass(frozen=True)
class PackageWaypoints:
    join: Point
    ingress: Point
    egress: Point
    split: Point


@dataclass
class Package:
    """A mission package."""

    #: The mission target. Currently can be either a ControlPoint or a
    #: TheaterGroundObject (non-ControlPoint map objectives).
    target: MissionTarget

    #: The set of flights in the package.
    flights: List[Flight] = field(default_factory=list)

    delay: int = field(default=0)

    #: True if the package ToT should be reset to ASAP whenever the player makes
    #: a change. This is really a UI property rather than a game property, but
    #: we want it to persist in the save.
    auto_asap: bool = field(default=False)

    #: Desired TOT as an offset from mission start.
    time_over_target: timedelta = field(default=timedelta())

    waypoints: Optional[PackageWaypoints] = field(default=None)

    @property
    def has_players(self) -> bool:
        return any(flight.client_count for flight in self.flights)

    @property
    def formation_speed(self) -> Optional[Speed]:
        """The speed of the package when in formation.

        If none of the flights in the package will join a formation, this
        returns None. This is nto uncommon, since only strike-like (strike,
        DEAD, anti-ship, BAI, etc.) flights and their escorts fly in formation.
        Others (CAP and CAS, currently) will coordinate in target timing but
        fly their own path to the target.
        """
        speeds = []
        for flight in self.flights:
            if isinstance(flight.flight_plan, FormationFlightPlan):
                speeds.append(flight.flight_plan.best_flight_formation_speed)
        if not speeds:
            return None
        return min(speeds)

    # TODO: Should depend on the type of escort.
    # SEAD might be able to leave before CAP.
    @property
    def escort_start_time(self) -> Optional[timedelta]:
        times = []
        for flight in self.flights:
            waypoint = flight.flight_plan.request_escort_at()
            if waypoint is None:
                continue
            tot = flight.flight_plan.tot_for_waypoint(waypoint)
            if tot is None:
                logging.error(
                    f"{flight} requested escort at {waypoint} but that "
                    "waypoint has no TOT. It may not be escorted."
                )
                continue
            times.append(tot)
        if times:
            return min(times)
        return None

    @property
    def escort_end_time(self) -> Optional[timedelta]:
        times = []
        for flight in self.flights:
            waypoint = flight.flight_plan.dismiss_escort_at()
            if waypoint is None:
                continue
            tot = flight.flight_plan.tot_for_waypoint(waypoint)
            if tot is None:
                tot = flight.flight_plan.depart_time_for_waypoint(waypoint)
            if tot is None:
                logging.error(
                    f"{flight} dismissed escort at {waypoint} but that "
                    "waypoint has no TOT or departure time. It may not be "
                    "escorted."
                )
                continue
            times.append(tot)
        if times:
            return max(times)
        return None

    @property
    def mission_departure_time(self) -> Optional[timedelta]:
        times = []
        for flight in self.flights:
            times.append(flight.flight_plan.mission_departure_time)
        if times:
            return max(times)
        return None

    def set_tot_asap(self) -> None:
        self.time_over_target = TotEstimator(self).earliest_tot()

    def add_flight(self, flight: Flight) -> None:
        """Adds a flight to the package."""
        self.flights.append(flight)

    def remove_flight(self, flight: Flight) -> None:
        """Removes a flight from the package."""
        self.flights.remove(flight)
        if not self.flights:
            self.waypoints = None

    @property
    def primary_task(self) -> Optional[FlightType]:
        if not self.flights:
            return None

        flight_counts: Dict[FlightType, int] = defaultdict(lambda: 0)
        for flight in self.flights:
            flight_counts[flight.flight_type] += 1

        # The package will contain a mix of mission types, but in general we can
        # determine the goal of the mission because some mission types are more
        # likely to be the main task than others. For example, a package with
        # only CAP flights is a CAP package, a flight with CAP and strike is a
        # strike package, a flight with CAP and DEAD is a DEAD package, and a
        # flight with strike and SEAD is an OCA/Strike package. This list defines the
        # priority order for package task names. The package's primary task will be the
        # first task in this list that matches a flight in the package.
        tasks_by_priority = [
            FlightType.CAS,
            FlightType.STRIKE,
            FlightType.ANTISHIP,
            FlightType.OCA_AIRCRAFT,
            FlightType.OCA_RUNWAY,
            FlightType.BAI,
            FlightType.DEAD,
            FlightType.TRANSPORT,
            FlightType.SEAD,
            FlightType.TARCAP,
            FlightType.BARCAP,
            FlightType.AEWC,
            FlightType.REFUELING,
            FlightType.SWEEP,
            FlightType.ESCORT,
        ]
        for task in tasks_by_priority:
            if flight_counts[task]:
                return task

        # If we get here, our task_priorities list above is incomplete. Log the
        # issue and return the type of *any* flight in the package.
        some_mission = next(iter(self.flights)).flight_type
        logging.warning(f"Unhandled mission type: {some_mission}")
        return some_mission

    @property
    def package_description(self) -> str:
        """Generates a package description based on flight composition."""
        task = self.primary_task
        if task is None:
            return "No mission"
        oca_strike_types = {FlightType.OCA_AIRCRAFT, FlightType.OCA_RUNWAY}
        if task in oca_strike_types:
            return "OCA Strike"
        return str(task)

    def __hash__(self) -> int:
        # TODO: Far from perfect. Number packages?
        return hash(self.target.name)


@dataclass
class AirTaskingOrder:
    """The entire ATO for one coalition."""

    #: The set of all planned packages in the ATO.
    packages: List[Package] = field(default_factory=list)

    def add_package(self, package: Package) -> None:
        """Adds a package to the ATO."""
        self.packages.append(package)

    def remove_package(self, package: Package) -> None:
        """Removes a package from the ATO."""
        self.packages.remove(package)

    def clear(self) -> None:
        """Removes all packages from the ATO."""
        self.packages.clear()
