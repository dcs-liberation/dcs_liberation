from __future__ import annotations

from typing import TYPE_CHECKING

from dcs import Point

from game.ato.flightstate import InFlight
from game.ato.starttype import StartType
from game.utils import Distance, LBS_TO_KG, Speed, meters

if TYPE_CHECKING:
    pass


def lerp(v0: float, v1: float, t: float) -> float:
    return (1 - t) * v0 + t * v1


class Navigating(InFlight):
    def progress(self) -> float:
        return (
            self.elapsed_time.total_seconds()
            / self.total_time_to_next_waypoint.total_seconds()
        )

    def estimate_position(self) -> Point:
        x0 = self.current_waypoint.position.x
        y0 = self.current_waypoint.position.y
        x1 = self.next_waypoint.position.x
        y1 = self.next_waypoint.position.y
        progress = self.progress()
        return Point(lerp(x0, x1, progress), lerp(y0, y1, progress))

    def estimate_altitude(self) -> tuple[Distance, str]:
        return (
            meters(
                lerp(
                    self.current_waypoint.alt.meters,
                    self.next_waypoint.alt.meters,
                    self.progress(),
                )
            ),
            self.current_waypoint.alt_type,
        )

    def estimate_speed(self) -> Speed:
        return self.flight.flight_plan.speed_between_waypoints(
            self.current_waypoint, self.next_waypoint
        )

    def estimate_fuel(self) -> float:
        initial_fuel = self.estimate_fuel_at_current_waypoint()
        ppm = self.flight.flight_plan.fuel_rate_to_between_points(
            self.current_waypoint, self.next_waypoint
        )
        if ppm is None:
            return initial_fuel
        position = self.estimate_position()
        distance = meters(self.current_waypoint.position.distance_to_point(position))
        consumption = distance.nautical_miles * ppm * LBS_TO_KG
        return initial_fuel - consumption

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    @property
    def spawn_type(self) -> StartType:
        return StartType.IN_FLIGHT

    @property
    def description(self) -> str:
        return f"Flying to {self.next_waypoint.name}"
