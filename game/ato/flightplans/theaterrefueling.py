from __future__ import annotations

from datetime import datetime, timedelta
from typing import Type

from game.utils import Heading, feet, meters, nautical_miles
from .ibuilder import IBuilder
from .patrolling import PatrollingLayout
from .refuelingflightplan import RefuelingFlightPlan
from .waypointbuilder import WaypointBuilder


class TheaterRefuelingFlightPlan(RefuelingFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def patrol_start_time(self) -> datetime:
        first_pre_refuel = self.first_pre_mission_aar_time
        if first_pre_refuel is None:
            return super().patrol_start_time
        return min(super().patrol_start_time, first_pre_refuel)

    @property
    def patrol_duration(self) -> timedelta:
        # Add 30 minutes to desired_player_mission_duration as TOTs for flights
        # can sit up to this time. This extension means the tanker remains on
        # station for the flights' return.
        native_duration = (
            self.flight.coalition.game.settings.desired_player_mission_duration
            + timedelta(minutes=30)
        )
        native_end_time = self.tot + native_duration
        if self.patrol_start_time >= self.tot:
            return native_duration
        return native_end_time - self.patrol_start_time


class Builder(IBuilder[TheaterRefuelingFlightPlan, PatrollingLayout]):
    def layout(self) -> PatrollingLayout:
        racetrack_half_distance = nautical_miles(20).meters

        location = self.package.target

        closest_boundary = self.threat_zones.closest_boundary(location.position)
        heading_to_threat_boundary = Heading.from_degrees(
            location.position.heading_between_point(closest_boundary)
        )
        distance_to_threat = meters(
            location.position.distance_to_point(closest_boundary)
        )
        orbit_heading = heading_to_threat_boundary

        # Station 70nm outside the threat zone.
        threat_buffer = nautical_miles(70)
        if self.threat_zones.threatened(location.position):
            orbit_distance = distance_to_threat + threat_buffer
        else:
            orbit_distance = distance_to_threat - threat_buffer

        racetrack_center = location.position.point_from_heading(
            orbit_heading.degrees, orbit_distance.meters
        )

        racetrack_start = racetrack_center.point_from_heading(
            orbit_heading.right.degrees, racetrack_half_distance
        )

        racetrack_end = racetrack_center.point_from_heading(
            orbit_heading.left.degrees, racetrack_half_distance
        )

        builder = WaypointBuilder(self.flight, self.coalition)

        tanker_type = self.flight.unit_type
        if tanker_type.patrol_altitude is not None:
            altitude = tanker_type.patrol_altitude
        else:
            altitude = feet(21000)

        racetrack = builder.race_track(racetrack_start, racetrack_end, altitude)

        return PatrollingLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position, racetrack_start, altitude
            ),
            nav_from=builder.nav_path(
                racetrack_end, self.flight.arrival.position, altitude
            ),
            patrol_start=racetrack[0],
            patrol_end=racetrack[1],
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self, dump_debug_info: bool = False) -> TheaterRefuelingFlightPlan:
        return TheaterRefuelingFlightPlan(self.flight, self.layout())
