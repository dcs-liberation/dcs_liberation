from __future__ import annotations

import copy
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
        closest_friendly_field = (
            None  # keep track of closest frieldly airfield in case we need it
        )
        for airfield in closest_cache.operational_airfields:
            # If the mission is a BARCAP of an enemy airfield, find the *next*
            # closest enemy airfield.
            if airfield == self.package.target:
                continue
            if airfield.captured != self.is_player:
                closest_airfield = airfield
                break
            elif closest_friendly_field is None:
                closest_friendly_field = airfield
        else:
            if barcap:
                # If planning a BARCAP, we should be able to find at least one enemy
                # airfield. If we can't, it's an error.
                raise PlanningError("Could not find any enemy airfields")
            else:
                # if we cannot find any friendly or enemy airfields other than the target,
                # there's nothing we can do
                if closest_friendly_field is None:
                    raise PlanningError(
                        "Could not find any enemy or friendly airfields"
                    )

                # If planning other race tracks (TARCAPs, currently), the target may be
                # the only enemy airfield. In this case, set the race track orientation using
                # a virtual point equi-distant from but opposite to the target from the closest
                # friendly airfield like below, where F is the closest friendly airfield, T is
                # the sole enemy airfield and V the virtual point
                #
                # F ---- T ----- V
                #
                # We need to create this virtual point, rather than using F to make sure
                # the race track is aligned towards the target.
                closest_friendly_field_position = copy.deepcopy(
                    closest_friendly_field.position
                )
                closest_airfield = closest_friendly_field
                closest_airfield.position.x = (
                    2 * self.package.target.position.x
                    - closest_friendly_field_position.x
                )
                closest_airfield.position.y = (
                    2 * self.package.target.position.y
                    - closest_friendly_field_position.y
                )

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
                - self.doctrine.cap.engagement_range
                - nautical_miles(5)
            )
            max_track_length = self.doctrine.cap.max_track_length
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
            max_track_length = self.doctrine.cap.min_track_length + 0.3 * (
                self.doctrine.cap.max_track_length - self.doctrine.cap.min_track_length
            )

        min_cap_distance = min(
            self.doctrine.cap.min_distance_from_cp, distance_to_no_fly
        )
        max_cap_distance = min(
            self.doctrine.cap.max_distance_from_cp, distance_to_no_fly
        )

        end = location.position.point_from_heading(
            heading.degrees,
            random.randint(int(min_cap_distance.meters), int(max_cap_distance.meters)),
        )

        track_length = random.randint(
            int(self.doctrine.cap.min_track_length.meters),
            int(max_track_length.meters),
        )
        start = end.point_from_heading(heading.opposite.degrees, track_length)
        return start, end
