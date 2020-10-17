from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import Iterable, Optional

from dcs.mapping import Point
from dcs.unittype import FlyingType

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

INGRESS_TYPES = {
    FlightWaypointType.INGRESS_CAS,
    FlightWaypointType.INGRESS_SEAD,
    FlightWaypointType.INGRESS_STRIKE,
}

IP_TYPES = {
    FlightWaypointType.INGRESS_CAS,
    FlightWaypointType.INGRESS_SEAD,
    FlightWaypointType.INGRESS_STRIKE,
    FlightWaypointType.PATROL_TRACK,
}


class GroundSpeed:
    @staticmethod
    def mission_speed(package: Package) -> int:
        speeds = set()
        for flight in package.flights:
            waypoint = flight.waypoint_with_type(IP_TYPES)
            if waypoint is None:
                logging.error(f"Could not find ingress point for {flight}.")
                if flight.points:
                    logging.warning(
                        "Using first waypoint for mission altitude.")
                    waypoint = flight.points[0]
                else:
                    logging.warning(
                        "Flight has no waypoints. Assuming mission altitude "
                        "of 25000 feet.")
                    waypoint = FlightWaypoint(FlightWaypointType.NAV, 0, 0,
                                              25000)
            speeds.add(GroundSpeed.for_flight(flight, waypoint.alt))
        return min(speeds)

    @classmethod
    def for_flight(cls, flight: Flight, altitude: int) -> int:
        if not issubclass(flight.unit_type, FlyingType):
            raise TypeError("Flight has non-flying unit")

        # TODO: Expose both a cruise speed and target speed.
        # The cruise speed can be used for ascent, hold, join, and RTB to save
        # on fuel, but mission speed will be fast enough to keep the flight
        # safer.

        c_sound_sea_level = 661.5

        # DCS's max speed is in kph at 0 MSL. Convert to knots.
        max_speed = flight.unit_type.max_speed * 0.539957
        if max_speed > c_sound_sea_level:
            # Aircraft is supersonic. Limit to mach 0.8 to conserve fuel and
            # account for heavily loaded jets.
            return int(cls.from_mach(0.8, altitude))

        # For subsonic aircraft, assume the aircraft can reasonably perform at
        # 80% of its maximum, and that it can maintain the same mach at altitude
        # as it can at sea level. This probably isn't great assumption, but
        # might. be sufficient given the wiggle room. We can come up with
        # another heuristic if needed.
        mach = max_speed * 0.8 / c_sound_sea_level
        return int(cls.from_mach(mach, altitude))  # knots

    @staticmethod
    def from_mach(mach: float, altitude: int) -> float:
        """Returns the ground speed in knots for the given mach and altitude.

        Args:
            mach: The mach number to convert to ground speed.
            altitude: The altitude in feet.

        Returns:
            The ground speed corresponding to the given altitude and mach number
            in knots.
        """
        # https://www.grc.nasa.gov/WWW/K-12/airplane/atmos.html
        if altitude <= 36152:
            temperature_f = 59 - 0.00356 * altitude
        else:
            # There's another formula for altitudes over 82k feet, but we better
            # not be planning waypoints that high...
            temperature_f = -70

        temperature_k = (temperature_f + 459.67) * (5 / 9)

        # https://www.engineeringtoolbox.com/specific-heat-ratio-d_602.html
        # Dependent on temperature, but varies very little (+/-0.001)
        # between -40F and 180F.
        heat_capacity_ratio = 1.4

        # https://www.grc.nasa.gov/WWW/K-12/airplane/sound.html
        gas_constant = 286  # m^2/s^2/K
        c_sound = math.sqrt(heat_capacity_ratio * gas_constant * temperature_k)
        # c_sound is in m/s, convert to knots.
        return (c_sound * 1.944) * mach


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
        time_to_ingress = self.estimate_waypoints_to_target(flight, IP_TYPES)
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
                GroundSpeed.mission_speed(self.package))
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
        # TODO: This is AGL. We want MSL.
        previous_altitude = 0
        previous_position = flight.from_cp.position
        for waypoint in flight.points:
            position = Point(waypoint.x, waypoint.y)
            total += TravelTime.between_points(
                previous_position, position,
                self.speed_to_waypoint(flight, waypoint, previous_altitude)
            )
            previous_position = position
            previous_altitude = waypoint.alt
            if waypoint.waypoint_type in stop_types:
                return total

        return None

    def speed_to_waypoint(self, flight: Flight, waypoint: FlightWaypoint,
                          from_altitude: int) -> int:
        # TODO: Adjust if AGL.
        # We don't have an exact heightmap, but we should probably be performing
        # *some* adjustment for NTTR since the minimum altitude of the map is
        # near 2000 ft MSL.
        alt_for_speed = min(from_altitude, waypoint.alt)
        pre_join = (FlightWaypointType.LOITER, FlightWaypointType.JOIN)
        if waypoint.waypoint_type == FlightWaypointType.ASCEND_POINT:
            # Flights that start airborne already have some altitude and a good
            # amount of speed.
            factor = 1.0 if flight.start_type == "In Flight" else 0.5
            return int(GroundSpeed.for_flight(flight, alt_for_speed) * factor)
        elif waypoint.waypoint_type in pre_join:
            return GroundSpeed.for_flight(flight, alt_for_speed)
        return GroundSpeed.mission_speed(self.package)


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

    def push_time(self, flight: Flight, hold_point: FlightWaypoint) -> int:
        assert self.package.waypoints is not None
        return self.join - TravelTime.between_points(
            Point(hold_point.x, hold_point.y),
            self.package.waypoints.join,
            GroundSpeed.for_flight(flight, hold_point.alt)
        )

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[int]:
        target_types = (
            FlightWaypointType.TARGET_GROUP_LOC,
            FlightWaypointType.TARGET_POINT,
            FlightWaypointType.TARGET_SHIP,
        )

        if waypoint.waypoint_type == FlightWaypointType.JOIN:
            return self.join
        elif waypoint.waypoint_type in INGRESS_TYPES:
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
            return self.push_time(flight, waypoint)
        elif waypoint.waypoint_type == FlightWaypointType.PATROL:
            return self.race_track_end
        return None

    @classmethod
    def for_package(cls, package: Package) -> PackageWaypointTiming:
        assert package.waypoints is not None

        # TODO: Plan similar altitudes for the in-country leg of the mission.
        # Waypoint altitudes for a given flight *shouldn't* differ too much
        # between the join and split points, so we don't need speeds for each
        # leg individually since they should all be fairly similar. This doesn't
        # hold too well right now since nothing is stopping each waypoint from
        # jumping 20k feet each time, but that's a huge waste of energy we
        # should be avoiding anyway.
        if not package.flights:
            raise ValueError("Cannot plan TOT for package with no flights")

        group_ground_speed = GroundSpeed.mission_speed(package)

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
