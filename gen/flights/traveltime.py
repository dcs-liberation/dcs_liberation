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
    def from_mach(mach: float, altitude_m: int) -> float:
        """Returns the ground speed in knots for the given mach and altitude.

        Args:
            mach: The mach number to convert to ground speed.
            altitude_m: The altitude in meters.

        Returns:
            The ground speed corresponding to the given altitude and mach number
            in knots.
        """
        # https://www.grc.nasa.gov/WWW/K-12/airplane/atmos.html
        altitude_ft = altitude_m * 3.28084
        if altitude_ft <= 36152:
            temperature_f = 59 - 0.00356 * altitude_ft
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


# TODO: Most if not all of this should move into FlightPlan.
class TotEstimator:

    def __init__(self, package: Package) -> None:
        self.package = package

    @staticmethod
    def mission_start_time(flight: Flight) -> timedelta:
        startup_time = flight.flight_plan.startup_time()
        if startup_time is None:
            # Could not determine takeoff time, probably due to a custom flight
            # plan. Start immediately.
            return timedelta()
        return startup_time

    def earliest_tot(self) -> timedelta:
        earliest_tot = max((
            self.earliest_tot_for_flight(f) for f in self.package.flights
        ))

        # Trim microseconds. DCS doesn't handle sub-second resolution for tasks,
        # and they're not interesting from a mission planning perspective so we
        # don't want them in the UI.
        #
        # Round up so we don't get negative start times.
        return timedelta(seconds=math.ceil(earliest_tot.total_seconds()))

    @staticmethod
    def earliest_tot_for_flight(flight: Flight) -> timedelta:
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
        # Clear the TOT, calculate the startup time. Negating the result gives
        # the earliest possible start time.
        orig_tot = flight.package.time_over_target
        try:
            flight.package.time_over_target = timedelta()
            time = flight.flight_plan.startup_time()
        finally:
            flight.package.time_over_target = orig_tot

        if time is None:
            logging.warning(f"Cannot estimate TOT for {flight}")
            # Return 0 so this flight's travel time does not affect the rest
            # of the package.
            return timedelta()
        return -time
