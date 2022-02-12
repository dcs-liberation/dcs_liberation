from __future__ import annotations

from datetime import timedelta
from typing import Optional, TYPE_CHECKING

from dcs import Point
from shapely.geometry import LineString

from game.ato import FlightType
from game.ato.flightstate import InFlight
from game.threatzones import ThreatPoly
from game.utils import Distance, Speed, dcs_to_shapely_point

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings


class RaceTrack(InFlight):
    def __init__(self, flight: Flight, settings: Settings, waypoint_index: int) -> None:
        assert flight.flight_plan.is_patrol(flight.flight_plan)
        self.patrol_duration = flight.flight_plan.patrol_duration
        super().__init__(flight, settings, waypoint_index)
        self.commit_region = LineString(
            [
                dcs_to_shapely_point(self.current_waypoint.position),
                dcs_to_shapely_point(self.next_waypoint.position),
            ]
        ).buffer(flight.flight_plan.engagement_distance.meters)

    def estimate_position(self) -> Point:
        # Prevent spawning racetracks in the middle of a leg. For simplicity we
        # always start the aircraft at the beginning of the racetrack.
        return self.current_waypoint.position

    def estimate_altitude(self) -> tuple[Distance, str]:
        return self.current_waypoint.alt, self.current_waypoint.alt_type

    def estimate_speed(self) -> Speed:
        return self.flight.unit_type.preferred_patrol_speed(self.estimate_altitude()[0])

    def estimate_fuel(self) -> float:
        # TODO: Estimate loiter consumption per minute?
        return self.estimate_fuel_at_current_waypoint()

    def travel_time_between_waypoints(self) -> timedelta:
        return self.patrol_duration

    def a2a_commit_region(self) -> Optional[ThreatPoly]:
        if self.flight.flight_type in {FlightType.BARCAP, FlightType.TARCAP}:
            return self.commit_region
        return None

    @property
    def description(self) -> str:
        return f"Patrolling for {self.patrol_duration - self.elapsed_time}"
