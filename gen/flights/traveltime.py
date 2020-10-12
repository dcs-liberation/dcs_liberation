from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, Optional

from dcs.mapping import Point

from game.utils import meter_to_nm
from gen.ato import Package
from gen.flights.flight import (
    Flight,
    FlightType,
    FlightWaypoint,
    FlightWaypointType,
)


CAP_DURATION = 30  # Minutes
CAP_TYPES = (FlightType.BARCAP, FlightType.CAP)


class GroundSpeed:
    @classmethod
    def for_package(cls, package: Package) -> int:
        speeds = []
        for flight in package.flights:
            speeds.append(cls.for_flight(flight))
        return min(speeds)  # knots

    @staticmethod
    def for_flight(_flight: Flight) -> int:
        # TODO: Gather data so this is useful.
        # TODO: Expose both a cruise speed and target speed.
        # The cruise speed can be used for ascent, hold, join, and RTB to save
        # on fuel, but mission speed will be fast enough to keep the flight
        # safer.
        return 400  # knots


class TravelTime:
    @staticmethod
    def between_points(a: Point, b: Point, speed: float) -> int:
        error_factor = 1.1
        distance = meter_to_nm(a.distance_to_point(b))
        hours = distance / speed
        seconds = hours * 3600
        return int(seconds * error_factor)


class TotEstimator:
    # An extra five minutes given as wiggle room. Expected to be spent at the
    # hold point performing any last minute configuration.
    HOLD_TIME = 5 * 60

    def __init__(self, package: Package) -> None:
        self.package = package
        self.timing = PackageWaypointTiming.for_package(package)

    def mission_start_time(self, flight: Flight) -> int:
        takeoff_time = self.takeoff_time_for_flight(flight)
        startup_time = self.estimate_startup(flight)
        ground_ops_time = self.estimate_ground_ops(flight)
        return takeoff_time - startup_time - ground_ops_time

    def takeoff_time_for_flight(self, flight: Flight) -> int:
        stop_types = {FlightWaypointType.JOIN, FlightWaypointType.PATROL_TRACK}
        travel_time = self.estimate_waypoints_to_target(flight, stop_types)
        if travel_time is None:
            logging.warning("Found no join point or patrol point. Cannot "
                            f"estimate takeoff time takeoff time for {flight}")
            # Takeoff immediately.
            return 0

        if self.package.primary_task in CAP_TYPES:
            start_time = self.timing.race_track_start
        else:
            start_time = self.timing.join
        return start_time - travel_time - self.HOLD_TIME

    def earliest_tot(self) -> int:
        return max((
            self.earliest_tot_for_flight(f) for f in self.package.flights
        )) + self.HOLD_TIME

    def earliest_tot_for_flight(self, flight: Flight) -> int:
        """Estimate fastest time from mission start to the target position.

        For CAP missions, this is time to race track start.

        For other mission types this is the time to the mission target.

        Args:
            flight: The flight to get the earliest TOT time for.

        Returns:
            The earliest possible TOT for the given flight in seconds. Returns 0
            if an ingress point cannot be found.
        """
        stop_types = {
            FlightWaypointType.PATROL_TRACK,
            FlightWaypointType.INGRESS_CAS,
            FlightWaypointType.INGRESS_SEAD,
            FlightWaypointType.INGRESS_STRIKE,
        }
        time_to_ingress = self.estimate_waypoints_to_target(flight, stop_types)
        if time_to_ingress is None:
            logging.warning(
                f"Found no ingress types. Cannot estimate TOT for {flight}")
            # Return 0 so this flight's travel time does not affect the rest of
            # the package.
            return 0

        if self.package.primary_task in CAP_TYPES:
            # The racetrack start *is* the target. The package target is the
            # protected objective.
            time_to_target = 0
        else:
            assert self.package.waypoints is not None
            time_to_target = TravelTime.between_points(
                self.package.waypoints.ingress, self.package.target.position,
                GroundSpeed.for_package(self.package))
        return sum([
            self.estimate_startup(flight),
            self.estimate_ground_ops(flight),
            time_to_ingress,
            time_to_target,
        ])

    @staticmethod
    def estimate_startup(flight: Flight) -> int:
        if flight.start_type == "Cold":
            return 10 * 60
        return 0

    @staticmethod
    def estimate_ground_ops(flight: Flight) -> int:
        if flight.start_type in ("Runway", "In Flight"):
            return 0
        if flight.from_cp.is_fleet:
            return 2 * 60
        else:
            return 5 * 60

    def estimate_waypoints_to_target(
            self, flight: Flight,
            stop_types: Iterable[FlightWaypointType]) -> Optional[int]:
        total = 0
        previous_position = flight.from_cp.position
        for waypoint in flight.points:
            position = Point(waypoint.x, waypoint.y)
            total += TravelTime.between_points(
                previous_position, position,
                self.speed_to_waypoint(flight, waypoint)
            )
            previous_position = position
            if waypoint.waypoint_type in stop_types:
                return total

        return None

    def speed_to_waypoint(self, flight: Flight,
                          waypoint: FlightWaypoint) -> int:
        pre_join = (FlightWaypointType.LOITER, FlightWaypointType.JOIN)
        if waypoint.waypoint_type == FlightWaypointType.ASCEND_POINT:
            # Flights that start airborne already have some altitude and a good
            # amount of speed.
            factor = 1.0 if flight.start_type == "In Flight" else 0.5
            return int(GroundSpeed.for_flight(flight) * factor)
        elif waypoint.waypoint_type in pre_join:
            return GroundSpeed.for_flight(flight)
        return GroundSpeed.for_package(self.package)


@dataclass(frozen=True)
class PackageWaypointTiming:
    #: The package being scheduled.
    package: Package

    #: The package join time.
    join: int

    #: The ingress waypoint TOT.
    ingress: int

    #: The egress waypoint TOT.
    egress: int

    #: The package split time.
    split: int

    @property
    def target(self) -> int:
        """The package time over target."""
        assert self.package.time_over_target is not None
        return self.package.time_over_target

    @property
    def race_track_start(self) -> int:
        if self.package.primary_task in CAP_TYPES:
            return self.package.time_over_target
        else:
            return self.ingress

    @property
    def race_track_end(self) -> int:
        if self.package.primary_task in CAP_TYPES:
            return self.target + CAP_DURATION * 60
        else:
            return self.egress

    def push_time(self, flight: Flight, hold_point: Point) -> int:
        assert self.package.waypoints is not None
        return self.join - TravelTime.between_points(
            hold_point,
            self.package.waypoints.join,
            GroundSpeed.for_flight(flight)
        )

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[int]:
        target_types = (
            FlightWaypointType.TARGET_GROUP_LOC,
            FlightWaypointType.TARGET_POINT,
            FlightWaypointType.TARGET_SHIP,
        )

        ingress_types = (
            FlightWaypointType.INGRESS_CAS,
            FlightWaypointType.INGRESS_SEAD,
            FlightWaypointType.INGRESS_STRIKE,
        )

        if waypoint.waypoint_type == FlightWaypointType.JOIN:
            return self.join
        elif waypoint.waypoint_type in ingress_types:
            return self.ingress
        elif waypoint.waypoint_type in target_types:
            return self.target
        elif waypoint.waypoint_type == FlightWaypointType.EGRESS:
            return self.egress
        elif waypoint.waypoint_type == FlightWaypointType.SPLIT:
            return self.split
        elif waypoint.waypoint_type == FlightWaypointType.PATROL_TRACK:
            return self.race_track_start
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint,
                                 flight: Flight) -> Optional[int]:
        if waypoint.waypoint_type == FlightWaypointType.LOITER:
            return self.push_time(flight, Point(waypoint.x, waypoint.y))
        elif waypoint.waypoint_type == FlightWaypointType.PATROL:
            return self.race_track_end
        return None

    @classmethod
    def for_package(cls, package: Package) -> PackageWaypointTiming:
        assert package.waypoints is not None

        group_ground_speed = GroundSpeed.for_package(package)

        ingress = package.time_over_target - TravelTime.between_points(
            package.waypoints.ingress,
            package.target.position,
            group_ground_speed
        )

        join = ingress - TravelTime.between_points(
            package.waypoints.join,
            package.waypoints.ingress,
            group_ground_speed
        )

        egress = package.time_over_target + TravelTime.between_points(
            package.target.position,
            package.waypoints.egress,
            group_ground_speed
        )

        split = egress + TravelTime.between_points(
            package.waypoints.egress,
            package.waypoints.split,
            group_ground_speed
        )

        return cls(package, join, ingress, egress, split)
