from __future__ import annotations

import logging
import math
from datetime import timedelta
from typing import Optional, TYPE_CHECKING

from dcs.mapping import Point
from dcs.unittype import FlyingType

from game.utils import meter_to_nm
from gen.flights.flight import Flight

if TYPE_CHECKING:
    from gen.ato import Package


class GroundSpeed:

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
    def between_points(a: Point, b: Point, speed: float) -> timedelta:
        error_factor = 1.1
        distance = meter_to_nm(a.distance_to_point(b))
        return timedelta(hours=distance / speed * error_factor)


class TotEstimator:
    # An extra five minutes given as wiggle room. Expected to be spent at the
    # hold point performing any last minute configuration.
    HOLD_TIME = timedelta(minutes=5)

    def __init__(self, package: Package) -> None:
        self.package = package

    def mission_start_time(self, flight: Flight) -> timedelta:
        takeoff_time = self.takeoff_time_for_flight(flight)
        startup_time = self.estimate_startup(flight)
        ground_ops_time = self.estimate_ground_ops(flight)
        start_time = takeoff_time - startup_time - ground_ops_time
        # In case FP math has given us some barely below zero time, round to
        # zero.
        if math.isclose(start_time.total_seconds(), 0):
            return timedelta()
        # Trim microseconds. DCS doesn't handle sub-second resolution for tasks,
        # and they're not interesting from a mission planning perspective so we
        # don't want them in the UI.
        #
        # Round down so *barely* above zero start times are just zero.
        return timedelta(seconds=math.floor(start_time.total_seconds()))

    def takeoff_time_for_flight(self, flight: Flight) -> timedelta:
        travel_time = self.travel_time_to_rendezvous_or_target(flight)
        if travel_time is None:
            logging.warning("Found no join point or patrol point. Cannot "
                            f"estimate takeoff time takeoff time for {flight}")
            # Takeoff immediately.
            return timedelta()

        from gen.flights.flightplan import FormationFlightPlan
        if isinstance(flight.flight_plan, FormationFlightPlan):
            tot = flight.flight_plan.tot_for_waypoint(
                flight.flight_plan.join)
            if tot is None:
                logging.warning(
                    "Could not determine the TOT of the join point. Takeoff "
                    f"time for {flight} will be immediate.")
                return timedelta()
        else:
            tot_waypoint = flight.flight_plan.tot_waypoint
            if tot_waypoint is None:
                tot = self.package.time_over_target
            else:
                tot = flight.flight_plan.tot_for_waypoint(tot_waypoint)
                if tot is None:
                    logging.error(f"TOT waypoint for {flight} has no TOT")
                    tot = self.package.time_over_target
        return tot - travel_time - self.HOLD_TIME

    def earliest_tot(self) -> timedelta:
        earliest_tot = max((
            self.earliest_tot_for_flight(f) for f in self.package.flights
        )) + self.HOLD_TIME

        # Trim microseconds. DCS doesn't handle sub-second resolution for tasks,
        # and they're not interesting from a mission planning perspective so we
        # don't want them in the UI.
        #
        # Round up so we don't get negative start times.
        return timedelta(seconds=math.ceil(earliest_tot.total_seconds()))

    def earliest_tot_for_flight(self, flight: Flight) -> timedelta:
        """Estimate fastest time from mission start to the target position.

        For BARCAP flights, this is time to race track start. This ensures that
        they are on station at the same time any other package members reach
        their ingress point.

        For other mission types this is the time to the mission target.

        Args:
            flight: The flight to get the earliest TOT time for.

        Returns:
            The earliest possible TOT for the given flight in seconds. Returns 0
            if an ingress point cannot be found.
        """
        time_to_target = self.travel_time_to_target(flight)
        if time_to_target is None:
            logging.warning(f"Cannot estimate TOT for {flight}")
            # Return 0 so this flight's travel time does not affect the rest
            # of the package.
            return timedelta()
        # Account for TOT offsets for the flight plan. An offset of -2 minutes
        # means the flight's TOT is 2 minutes ahead of the package's so it needs
        # an extra two minutes.
        offset = -flight.flight_plan.tot_offset
        startup = self.estimate_startup(flight)
        ground_ops = self.estimate_ground_ops(flight)
        return startup + ground_ops + time_to_target + offset

    @staticmethod
    def estimate_startup(flight: Flight) -> timedelta:
        if flight.start_type == "Cold":
            if flight.client_count:
                return timedelta(minutes=10)
            else:
                # The AI doesn't seem to have a real startup procedure.
                return timedelta(minutes=2)
        return timedelta()

    @staticmethod
    def estimate_ground_ops(flight: Flight) -> timedelta:
        if flight.start_type in ("Runway", "In Flight"):
            return timedelta()
        if flight.from_cp.is_fleet:
            return timedelta(minutes=2)
        else:
            return timedelta(minutes=5)

    @staticmethod
    def travel_time_to_target(flight: Flight) -> Optional[timedelta]:
        if flight.flight_plan is None:
            return None
        return flight.flight_plan.travel_time_to_target

    @staticmethod
    def travel_time_to_rendezvous_or_target(
            flight: Flight) -> Optional[timedelta]:
        if flight.flight_plan is None:
            return None
        from gen.flights.flightplan import FormationFlightPlan
        if isinstance(flight.flight_plan, FormationFlightPlan):
            return flight.flight_plan.travel_time_to_rendezvous
        return flight.flight_plan.travel_time_to_target
