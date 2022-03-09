from __future__ import annotations

from datetime import timedelta
from typing import Type

from game.ato.flightplans.ibuilder import IBuilder
from game.ato.flightplans.patrolling import PatrollingFlightPlan
from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.utils import Heading, feet, knots, meters, nautical_miles


class Builder(IBuilder):
    def build(self) -> AewcFlightPlan:
        racetrack_half_distance = nautical_miles(30).meters

        patrol_duration = timedelta(hours=4)

        location = self.package.target

        closest_boundary = self.threat_zones.closest_boundary(location.position)
        heading_to_threat_boundary = Heading.from_degrees(
            location.position.heading_between_point(closest_boundary)
        )
        distance_to_threat = meters(
            location.position.distance_to_point(closest_boundary)
        )
        orbit_heading = heading_to_threat_boundary

        # Station 80nm outside the threat zone.
        threat_buffer = nautical_miles(80)
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

        if self.flight.unit_type.patrol_altitude is not None:
            altitude = self.flight.unit_type.patrol_altitude
        else:
            altitude = feet(25000)

        if self.flight.unit_type.preferred_patrol_speed(altitude) is not None:
            speed = self.flight.unit_type.preferred_patrol_speed(altitude)
        else:
            speed = knots(390)

        racetrack = builder.race_track(racetrack_start, racetrack_end, altitude)

        return AewcFlightPlan(
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


class AewcFlightPlan(PatrollingFlightPlan):
    @staticmethod
    def builder_type() -> Type[IBuilder]:
        return Builder
