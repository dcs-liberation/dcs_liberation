from __future__ import annotations

import random
from typing import Type

from game.theater import FrontLine
from game.utils import feet
from .capbuilder import CapBuilder
from .invalidobjectivelocation import InvalidObjectiveLocation
from .patrolling import PatrollingFlightPlan
from .waypointbuilder import WaypointBuilder


class Builder(CapBuilder):
    def build(self) -> BarCapFlightPlan:
        location = self.package.target

        if isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        start_pos, end_pos = self.cap_racetrack_for_objective(location, barcap=True)

        preferred_alt = self.flight.unit_type.preferred_patrol_altitude
        randomized_alt = preferred_alt + feet(random.randint(-2, 1) * 1000)
        patrol_alt = max(
            self.doctrine.min_patrol_altitude,
            min(self.doctrine.max_patrol_altitude, randomized_alt),
        )

        patrol_speed = self.flight.unit_type.preferred_patrol_speed(patrol_alt)

        builder = WaypointBuilder(self.flight, self.coalition)
        start, end = builder.race_track(start_pos, end_pos, patrol_alt)

        return BarCapFlightPlan(
            flight=self.flight,
            patrol_duration=self.doctrine.cap_duration,
            patrol_speed=patrol_speed,
            engagement_distance=self.doctrine.cap_engagement_range,
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position, start.position, patrol_alt
            ),
            nav_from=builder.nav_path(
                end.position, self.flight.arrival.position, patrol_alt
            ),
            patrol_start=start,
            patrol_end=end,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )


class BarCapFlightPlan(PatrollingFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder
