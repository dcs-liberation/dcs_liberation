from __future__ import annotations

import random
from abc import ABC
from typing import Any, TYPE_CHECKING, TypeVar

from dcs import Point
from shapely.geometry import Point as ShapelyPoint

from game.utils import Heading, meters, nautical_miles
from .flightplan import FlightPlan
from .patrolling import PatrollingLayout
from ..closestairfields import ObjectiveDistanceCache
from ..flightplans.ibuilder import IBuilder
from ..flightplans.planningerror import PlanningError

if TYPE_CHECKING:
    from game.theater import MissionTarget

FlightPlanT = TypeVar("FlightPlanT", bound=FlightPlan[Any])
LayoutT = TypeVar("LayoutT", bound=PatrollingLayout)


class CapBuilder(IBuilder[FlightPlanT, LayoutT], ABC):
    def cap_racetrack_for_objective(
        self, location: MissionTarget, barcap: bool
    ) -> tuple[Point, Point]:
        closest_cache = ObjectiveDistanceCache.get_closest_airfields(location)
        for airfield in closest_cache.operational_airfields:
            # If the mission is a BARCAP of an enemy airfield, find the *next*
            # closest enemy airfield.
            if airfield == self.package.target:
                continue
            if airfield.captured != self.is_player:
                closest_airfield = airfield
                break
        else:
            raise PlanningError("Could not find any enemy airfields")

        heading = Heading.from_degrees(
            location.position.heading_between_point(closest_airfield.position)
        )

        position = ShapelyPoint(
            self.package.target.position.x, self.package.target.position.y
        )

        if barcap:
            # BARCAPs should remain far enough back from the enemy that their
            # commit range does not enter the enemy's threat zone. Include a 5nm
            # buffer.
            distance_to_no_fly = (
                meters(position.distance(self.threat_zones.all))
                - self.doctrine.cap_engagement_range
                - nautical_miles(5)
            )
            max_track_length = self.doctrine.cap_max_track_length
        else:
            # Other race tracks (TARCAPs, currently) just try to keep some
            # distance from the nearest enemy airbase, but since they are by
            # definition in enemy territory they can't avoid the threat zone
            # without being useless.
            min_distance_from_enemy = nautical_miles(20)
            distance_to_airfield = meters(
                closest_airfield.position.distance_to_point(
                    self.package.target.position
                )
            )
            distance_to_no_fly = distance_to_airfield - min_distance_from_enemy

            # TARCAPs fly short racetracks because they need to react faster.
            max_track_length = self.doctrine.cap_min_track_length + 0.3 * (
                self.doctrine.cap_max_track_length - self.doctrine.cap_min_track_length
            )

        min_cap_distance = min(
            self.doctrine.cap_min_distance_from_cp, distance_to_no_fly
        )
        max_cap_distance = min(
            self.doctrine.cap_max_distance_from_cp, distance_to_no_fly
        )

        end = location.position.point_from_heading(
            heading.degrees,
            random.randint(int(min_cap_distance.meters), int(max_cap_distance.meters)),
        )

        track_length = random.randint(
            int(self.doctrine.cap_min_track_length.meters),
            int(max_track_length.meters),
        )
        start = end.point_from_heading(heading.opposite.degrees, track_length)
        return start, end
