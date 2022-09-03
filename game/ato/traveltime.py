from __future__ import annotations

import math
from datetime import timedelta
from typing import TYPE_CHECKING

from dcs.mapping import Point

from game.utils import (
    Distance,
    SPEED_OF_SOUND_AT_SEA_LEVEL,
    Speed,
    mach,
    meters,
)

if TYPE_CHECKING:
    from .flight import Flight
    from .package import Package


class GroundSpeed:
    @classmethod
    def for_flight(cls, flight: Flight, altitude: Distance) -> Speed:
        # TODO: Expose both a cruise speed and target speed.
        # The cruise speed can be used for ascent, hold, join, and RTB to save
        # on fuel, but mission speed will be fast enough to keep the flight
        # safer.

        # DCS's max speed is in kph at 0 MSL.
        max_speed = flight.unit_type.max_speed
        if max_speed > SPEED_OF_SOUND_AT_SEA_LEVEL:
            # Aircraft is supersonic. Limit to mach 0.85 to conserve fuel and
            # account for heavily loaded jets.
            return mach(0.85, altitude)

        # For subsonic aircraft, assume the aircraft can reasonably perform at
        # 80% of its maximum, and that it can maintain the same mach at altitude
        # as it can at sea level. This probably isn't great assumption, but
        # might. be sufficient given the wiggle room. We can come up with
        # another heuristic if needed.
        cruise_mach = max_speed.mach() * 0.85
        return mach(cruise_mach, altitude)


class TravelTime:
    @staticmethod
    def between_points(a: Point, b: Point, speed: Speed) -> timedelta:
        error_factor = 1.05
        distance = meters(a.distance_to_point(b))
        return timedelta(hours=distance.nautical_miles / speed.knots * error_factor)


# TODO: Most if not all of this should move into FlightPlan.
class TotEstimator:
    def __init__(self, package: Package) -> None:
        self.package = package

    def earliest_tot(self) -> timedelta:
        if not self.package.flights:
            return timedelta(0)

        earliest_tot = max(
            (self.earliest_tot_for_flight(f) for f in self.package.flights)
        )

        # Trim microseconds. DCS doesn't handle sub-second resolution for tasks,
        # and they're not interesting from a mission planning perspective so we
        # don't want them in the UI.
        #
        # Round up so we don't get negative start times.
        return timedelta(seconds=math.ceil(earliest_tot.total_seconds()))

    @staticmethod
    def earliest_tot_for_flight(flight: Flight) -> timedelta:
        """Estimate the fastest time from mission start to the target position.

        For BARCAP flights, this is time to the racetrack start. This ensures that
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
        return -time
