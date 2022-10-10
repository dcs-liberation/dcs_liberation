from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from dcs import Point

from game.ato.flightstate import InFlight
from game.ato.starttype import StartType
from game.utils import Distance, LBS_TO_KG, Speed, meters

if TYPE_CHECKING:
    from game.sim.gameupdateevents import GameUpdateEvents


def lerp(v0: float, v1: float, t: float) -> float:
    return (1 - t) * v0 + t * v1


class Navigating(InFlight):
    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        super().on_game_tick(events, time, duration)

        # If the parent tick caused this waypoint to become inactive don't update the
        # position based on our now invalid state.
        if not self.current_waypoint_elapsed:
            events.update_flight_position(self.flight, self.estimate_position())

    def progress(self) -> float:
        return (
            self.elapsed_time.total_seconds()
            / self.total_time_to_next_waypoint.total_seconds()
        )

    def estimate_position(self) -> Point:
        return self.current_waypoint.position.lerp(
            self.next_waypoint.position, self.progress()
        )

    def estimate_altitude(self) -> tuple[Distance, str]:
        # This does not behave well when one of the waypoints is AGL and the other is
        # MSL. We can't really avoid that problem though. We don't know where the ground
        # is, so conversions between them are impossible, and we do need to use AGL
        # altitudes for takeoff and landing waypoints (even if we had the runway
        # elevation, we don't have elevation for FARPs).
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
