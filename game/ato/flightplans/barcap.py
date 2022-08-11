from __future__ import annotations

import random
from datetime import timedelta
from typing import Type

from game.theater import FrontLine
from game.utils import Distance, Speed, feet
from .capbuilder import CapBuilder
from .invalidobjectivelocation import InvalidObjectiveLocation
from .patrolling import PatrollingFlightPlan, PatrollingLayout
from .waypointbuilder import WaypointBuilder


class BarCapFlightPlan(PatrollingFlightPlan[PatrollingLayout]):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def patrol_duration(self) -> timedelta:
        return self.flight.coalition.doctrine.cap_duration

    @property
    def patrol_speed(self) -> Speed:
        return self.flight.unit_type.preferred_patrol_speed(
            self.layout.patrol_start.alt
        )

    @property
    def engagement_distance(self) -> Distance:
        return self.flight.coalition.doctrine.cap_engagement_range


class Builder(CapBuilder[BarCapFlightPlan, PatrollingLayout]):
    def layout(self) -> PatrollingLayout:
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

        builder = WaypointBuilder(self.flight, self.coalition)
        start, end = builder.race_track(start_pos, end_pos, patrol_alt)

        return PatrollingLayout(
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

    def build(self) -> BarCapFlightPlan:
        return BarCapFlightPlan(self.flight, self.layout())
