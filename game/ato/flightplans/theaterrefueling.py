from __future__ import annotations

from datetime import timedelta
from typing import Type

from game.utils import Heading, feet, knots, meters, nautical_miles
from .ibuilder import IBuilder
from .patrolling import PatrollingFlightPlan
from .waypointbuilder import WaypointBuilder


class Builder(IBuilder):
    def build(self) -> TheaterRefuelingFlightPlan:
        racetrack_half_distance = nautical_miles(20).meters

        patrol_duration = timedelta(hours=1)

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

        # TODO: Could use self.flight.unit_type.preferred_patrol_speed(altitude).
        if tanker_type.patrol_speed is not None:
            speed = tanker_type.patrol_speed
        else:
            # ~280 knots IAS at 21000.
            speed = knots(400)

        racetrack = builder.race_track(racetrack_start, racetrack_end, altitude)

        return TheaterRefuelingFlightPlan(
            flight=self.flight,
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
            patrol_duration=patrol_duration,
            patrol_speed=speed,
            # TODO: Factor out a common base of the combat and non-combat race-tracks.
            # No harm in setting this, but we ought to clean up a bit.
            engagement_distance=meters(0),
        )


class TheaterRefuelingFlightPlan(PatrollingFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder
