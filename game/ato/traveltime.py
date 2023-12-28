from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from game.utils import Distance, SPEED_OF_SOUND_AT_SEA_LEVEL, Speed, mach

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

        if flight.squadron.aircraft.cruise_speed is not None:
            return mach(flight.squadron.aircraft.cruise_speed.mach(), altitude)

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


# TODO: Most if not all of this should move into FlightPlan.
class TotEstimator:
    def __init__(self, package: Package) -> None:
        self.package = package

    def earliest_tot(self, now: datetime) -> datetime:
        if not self.package.flights:
            return now

        return max(self.earliest_tot_for_flight(f, now) for f in self.package.flights)

    @staticmethod
    def earliest_tot_for_flight(flight: Flight, now: datetime) -> datetime:
        """Estimate the earliest time the flight can reach the target position.

        The interpretation of the TOT depends on the flight plan type. See the various
        FlightPlan implementations for details.

        Args:
            flight: The flight to get the earliest TOT for.
            now: The current mission time.

        Returns:
            The earliest possible TOT for the given flight.
        """
        return now + flight.flight_plan.minimum_duration_from_start_to_tot()
