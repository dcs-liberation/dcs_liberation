"""Air Tasking Orders.

The classes of the Air Tasking Order (ATO) define all of the missions that have
been planned, and which aircraft have been assigned to them. Each planned
mission, or "package" is composed of individual flights. The package may contain
dissimilar aircraft performing different roles, but all for the same goal. For
example, the package to strike an enemy airfield may contain an escort flight,
a SEAD flight, and the strike aircraft themselves. CAP packages may contain only
the single CAP flight.
"""
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dcs.mapping import Point

from theater.missiontarget import MissionTarget
from .flights.flight import Flight, FlightType


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

    #: Desired TOT measured in seconds from mission start.
    time_over_target: int = field(default=0)

    waypoints: Optional[PackageWaypoints] = field(default=None)

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
        # flight with strike and SEAD is an OCA/Strike package. The type of
        # package is determined by the highest priority flight in the package.
        task_priorities = [
            FlightType.CAS,
            FlightType.STRIKE,
            FlightType.ANTISHIP,
            FlightType.BAI,
            FlightType.EVAC,
            FlightType.TROOP_TRANSPORT,
            FlightType.RECON,
            FlightType.ELINT,
            FlightType.DEAD,
            FlightType.SEAD,
            FlightType.LOGISTICS,
            FlightType.INTERCEPTION,
            FlightType.TARCAP,
            FlightType.CAP,
            FlightType.BARCAP,
            FlightType.EWAR,
            FlightType.ESCORT,
        ]
        for task in task_priorities:
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
        return task.name

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
