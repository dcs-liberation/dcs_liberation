from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from dcs import Point

from game.ato.flightstate import Completed
from game.ato.flightstate.flightstate import FlightState
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.starttype import StartType
from game.utils import Distance, Speed, meters
from gen.flights.flightplan import LoiterFlightPlan, PatrollingFlightPlan

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings


def lerp(v0: float, v1: float, t: float) -> float:
    return (1 - t) * v0 + t * v1


class InFlight(FlightState):
    def __init__(self, flight: Flight, settings: Settings) -> None:
        super().__init__(flight, settings)
        self.waypoints = flight.flight_plan.iter_waypoints()
        # TODO: Error checking for stupid flight plans with fewer than two waypoints.
        self.current_waypoint = next(self.waypoints)
        self.next_waypoint = next(self.waypoints)
        self.passed_waypoints = {self.current_waypoint}
        self.total_time_to_next_waypoint = self._total_time()
        self.elapsed_time = timedelta()

    def _total_time(self) -> timedelta:
        if isinstance(self.flight.flight_plan, PatrollingFlightPlan):
            # Racetracks should remain at the first waypoint until the patrol ends so
            # that the waypoint generation doesn't need to reverse the orbit direction.
            if self.current_waypoint == self.flight.flight_plan.patrol_start:
                return self.flight.flight_plan.patrol_duration

        # Loiter time is already built into travel_time_between_waypoints.
        return self.flight.flight_plan.travel_time_between_waypoints(
            self.current_waypoint, self.next_waypoint
        )

    def progress(self) -> float:
        return (
            self.elapsed_time.total_seconds()
            / self.total_time_to_next_waypoint.total_seconds()
        )

    def estimate_position(self) -> Point:
        # TODO: Make Loiter and RaceTrack distinct FlightStates.
        if isinstance(self.flight.flight_plan, PatrollingFlightPlan):
            # Prevent spawning racetracks in the middle of a leg. For simplicity we
            # always start the aircraft at the beginning of the racetrack.
            if self.current_waypoint == self.flight.flight_plan.patrol_start:
                return self.current_waypoint.position
        elif isinstance(self.flight.flight_plan, LoiterFlightPlan):
            if (
                self.current_waypoint == self.flight.flight_plan.hold
                and self.elapsed_time < self.flight.flight_plan.hold_duration
            ):
                return self.current_waypoint.position

        x0 = self.current_waypoint.position.x
        y0 = self.current_waypoint.position.y
        x1 = self.next_waypoint.position.x
        y1 = self.next_waypoint.position.y
        progress = self.progress()
        return Point(lerp(x0, x1, progress), lerp(y0, y1, progress))

    def estimate_altitude(self) -> tuple[Distance, str]:
        # TODO: Should count progress as 0 until departing a hold.
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
        # TODO: Patrol/loiter speeds may be different.
        return self.flight.flight_plan.speed_between_waypoints(
            self.current_waypoint, self.next_waypoint
        )

    def update_waypoints(self) -> None:
        self.current_waypoint = self.next_waypoint
        self.passed_waypoints.add(self.current_waypoint)
        try:
            self.next_waypoint = next(self.waypoints)
        except StopIteration:
            self.flight.set_state(Completed(self.flight, self.settings))
        self.total_time_to_next_waypoint = self._total_time()
        self.elapsed_time = timedelta()

    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
        self.elapsed_time += duration
        if self.elapsed_time > self.total_time_to_next_waypoint:
            self.update_waypoints()

    def should_halt_sim(self) -> bool:
        contact_types = {
            FlightWaypointType.INGRESS_BAI,
            FlightWaypointType.INGRESS_CAS,
            FlightWaypointType.INGRESS_DEAD,
            FlightWaypointType.INGRESS_OCA_AIRCRAFT,
            FlightWaypointType.INGRESS_OCA_RUNWAY,
            FlightWaypointType.INGRESS_SEAD,
            FlightWaypointType.INGRESS_STRIKE,
        }
        # TODO: Check against enemy threats.
        if self.current_waypoint.waypoint_type in contact_types:
            logging.info(
                f"Interrupting simulation because {self.flight} has reached its "
                "ingress point"
            )
            return True

        threat_zone = self.flight.squadron.coalition.opponent.threat_zone
        if threat_zone.threatened_by_air_defense(self.estimate_position()):
            logging.info(
                f"Interrupting simulation because {self.flight} has encountered enemy "
                "air defenses"
            )
            return True

        return False

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    @property
    def spawn_type(self) -> StartType:
        return StartType.IN_FLIGHT
