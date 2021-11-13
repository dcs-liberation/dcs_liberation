from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from dcs import Point

from game.ato.flightstate import Completed
from game.ato.flightstate.flightstate import FlightState
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.starttype import StartType
from game.utils import Distance, LBS_TO_KG, Speed, meters, pairwise
from gen.flights.flightplan import LoiterFlightPlan

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings
    from game.sim.aircraftengagementzones import AircraftEngagementZones


def lerp(v0: float, v1: float, t: float) -> float:
    return (1 - t) * v0 + t * v1


class InFlight(FlightState):
    def __init__(self, flight: Flight, settings: Settings, waypoint_index: int) -> None:
        super().__init__(flight, settings)
        waypoints = self.flight.flight_plan.waypoints
        self.waypoint_index = waypoint_index
        self.current_waypoint = waypoints[self.waypoint_index]
        # TODO: Error checking for flight plans without landing waypoints.
        self.next_waypoint = waypoints[self.waypoint_index + 1]
        self.total_time_to_next_waypoint = self.travel_time_between_waypoints()
        self.elapsed_time = timedelta()

    def has_passed_waypoint(self, waypoint: FlightWaypoint) -> bool:
        index = self.flight.flight_plan.waypoints.index(waypoint)
        return index <= self.waypoint_index

    def travel_time_between_waypoints(self) -> timedelta:
        travel_time = self.flight.flight_plan.travel_time_between_waypoints(
            self.current_waypoint, self.next_waypoint
        )
        if self.current_waypoint.waypoint_type is FlightWaypointType.LOITER:
            # Loiter time is already built into travel_time_between_waypoints. If we're
            # at a loiter point but still a regular InFlight (Loiter overrides this
            # method) that means we're traveling from the loiter point but no longer
            # loitering.
            assert isinstance(self.flight.flight_plan, LoiterFlightPlan)
            travel_time -= self.flight.flight_plan.hold_duration
        return travel_time

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

    def estimate_fuel_at_current_waypoint(self) -> float:
        initial_fuel = super().estimate_fuel()
        if self.flight.unit_type.fuel_consumption is None:
            return initial_fuel
        initial_fuel -= self.flight.unit_type.fuel_consumption.taxi * LBS_TO_KG
        waypoints = self.flight.flight_plan.waypoints[: self.waypoint_index + 1]
        for a, b in pairwise(waypoints[:-1]):
            consumption = self.flight.flight_plan.fuel_consumption_between_points(a, b)
            assert consumption is not None
            initial_fuel -= consumption * LBS_TO_KG
        return initial_fuel

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

    def next_waypoint_state(self) -> FlightState:
        from game.ato.flightstate.loiter import Loiter
        from game.ato.flightstate.racetrack import RaceTrack

        new_index = self.waypoint_index + 1
        if self.next_waypoint.waypoint_type is FlightWaypointType.LANDING_POINT:
            return Completed(self.flight, self.settings)
        if self.next_waypoint.waypoint_type is FlightWaypointType.PATROL_TRACK:
            return RaceTrack(self.flight, self.settings, new_index)
        if self.next_waypoint.waypoint_type is FlightWaypointType.LOITER:
            return Loiter(self.flight, self.settings, new_index)
        return InFlight(self.flight, self.settings, new_index)

    def advance_to_next_waypoint(self) -> None:
        self.flight.set_state(self.next_waypoint_state())

    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
        self.elapsed_time += duration
        if self.elapsed_time > self.total_time_to_next_waypoint:
            self.advance_to_next_waypoint()

    def should_halt_sim(self, enemy_aircraft_coverage: AircraftEngagementZones) -> bool:
        contact_types = {
            FlightWaypointType.INGRESS_BAI,
            FlightWaypointType.INGRESS_CAS,
            FlightWaypointType.INGRESS_DEAD,
            FlightWaypointType.INGRESS_OCA_AIRCRAFT,
            FlightWaypointType.INGRESS_OCA_RUNWAY,
            FlightWaypointType.INGRESS_SEAD,
            FlightWaypointType.INGRESS_STRIKE,
        }

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

        if enemy_aircraft_coverage.covers(self.estimate_position()):
            logging.info(
                f"Interrupting simulation because {self.flight} has encountered enemy "
                "air-to-air patrol"
            )
            return True

        return False

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    @property
    def spawn_type(self) -> StartType:
        return StartType.IN_FLIGHT

    @property
    def description(self) -> str:
        return f"Flying to {self.next_waypoint.name}"
