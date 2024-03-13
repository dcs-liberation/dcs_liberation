from __future__ import annotations

import math
from datetime import timezone
from typing import Iterator, List, Optional, TYPE_CHECKING, Tuple
from uuid import UUID

from dcs.mapping import Point
from dcs.terrain.terrain import Terrain
from shapely import geometry, ops

from .daytimemap import DaytimeMap
from .frontline import FrontLine
from .iadsnetwork.iadsnetwork import IadsNetwork
from .landmap import Landmap, poly_contains
from .seasonalconditions import SeasonalConditions
from ..utils import Heading

if TYPE_CHECKING:
    from .controlpoint import ControlPoint, MissionTarget
    from .theatergroundobject import TheaterGroundObject


class ConflictTheater:
    iads_network: IadsNetwork

    def __init__(
        self,
        terrain: Terrain,
        landmap: Landmap | None,
        time_zone: timezone,
        seasonal_conditions: SeasonalConditions,
        daytime_map: DaytimeMap,
    ) -> None:
        self.terrain = terrain
        self.landmap = landmap
        self.timezone = time_zone
        self.seasonal_conditions = seasonal_conditions
        self.daytime_map = daytime_map
        self.controlpoints: list[ControlPoint] = []

    def add_controlpoint(self, point: ControlPoint) -> None:
        self.controlpoints.append(point)

    @property
    def ground_objects(self) -> Iterator[TheaterGroundObject]:
        for cp in self.controlpoints:
            for go in cp.ground_objects:
                yield go

    def find_ground_objects_by_obj_name(
        self, obj_name: str
    ) -> list[TheaterGroundObject]:
        found = []
        for cp in self.controlpoints:
            for g in cp.ground_objects:
                if g.obj_name == obj_name:
                    found.append(g)
        return found

    def is_in_sea(self, point: Point) -> bool:
        if not self.landmap:
            return False

        if self.is_on_land(point):
            return False

        for exclusion_zone in self.landmap.exclusion_zones.geoms:
            if poly_contains(point.x, point.y, exclusion_zone):
                return False

        for sea in self.landmap.sea_zones.geoms:
            if poly_contains(point.x, point.y, sea):
                return True

        return False

    def is_on_land(self, point: Point) -> bool:
        if not self.landmap:
            return True

        is_point_included = False
        if poly_contains(point.x, point.y, self.landmap.inclusion_zones):
            is_point_included = True

        if not is_point_included:
            return False

        for exclusion_zone in self.landmap.exclusion_zones.geoms:
            if poly_contains(point.x, point.y, exclusion_zone):
                return False

        return True

    def nearest_land_pos(self, near: Point, extend_dist: int = 50) -> Point:
        """Returns the nearest point inside a land exclusion zone from point
        `extend_dist` determines how far inside the zone the point should be placed"""
        if self.is_on_land(near):
            return near
        point = geometry.Point(near.x, near.y)
        nearest_points = []
        if not self.landmap:
            raise RuntimeError("Landmap not initialized")
        for inclusion_zone in self.landmap.inclusion_zones.geoms:
            nearest_pair = ops.nearest_points(point, inclusion_zone)
            nearest_points.append(nearest_pair[1])
        min_distance = point.distance(nearest_points[0])  # type: geometry.Point
        nearest_point = nearest_points[0]  # type: geometry.Point
        for pt in nearest_points[1:]:
            distance = point.distance(pt)
            if distance < min_distance:
                min_distance = distance
                nearest_point = pt
        assert isinstance(nearest_point, geometry.Point)
        point = Point(point.x, point.y, self.terrain)
        nearest_point = Point(nearest_point.x, nearest_point.y, self.terrain)
        new_point = point.point_from_heading(
            point.heading_between_point(nearest_point),
            point.distance_to_point(nearest_point) + extend_dist,
        )
        return new_point

    def control_points_for(self, player: bool) -> Iterator[ControlPoint]:
        for point in self.controlpoints:
            if point.captured == player:
                yield point

    def player_points(self) -> List[ControlPoint]:
        return list(self.control_points_for(player=True))

    def conflicts(self) -> Iterator[FrontLine]:
        for cp in self.player_points():
            yield from cp.front_lines.values()

    def enemy_points(self) -> List[ControlPoint]:
        return list(self.control_points_for(player=False))

    def closest_control_point(
        self, point: Point, allow_naval: bool = False
    ) -> ControlPoint:
        closest = self.controlpoints[0]
        closest_distance = point.distance_to_point(closest.position)
        for control_point in self.controlpoints[1:]:
            if control_point.is_fleet and not allow_naval:
                continue
            distance = point.distance_to_point(control_point.position)
            if distance < closest_distance:
                closest = control_point
                closest_distance = distance
        return closest

    def closest_target(self, point: Point) -> MissionTarget:
        closest: MissionTarget = self.controlpoints[0]
        closest_distance = point.distance_to_point(closest.position)
        for control_point in self.controlpoints[1:]:
            distance = point.distance_to_point(control_point.position)
            if distance < closest_distance:
                closest = control_point
                closest_distance = distance
            for tgo in control_point.ground_objects:
                distance = point.distance_to_point(tgo.position)
                if distance < closest_distance:
                    closest = tgo
                    closest_distance = distance
        for conflict in self.conflicts():
            distance = conflict.position.distance_to_point(point)
            if distance < closest_distance:
                closest = conflict
                closest_distance = distance
        return closest

    def closest_opposing_control_points(self) -> Tuple[ControlPoint, ControlPoint]:
        """
        Returns a tuple of the two nearest opposing ControlPoints in theater.
        (player_cp, enemy_cp)
        """
        seen = set()
        min_distance = math.inf
        closest_blue = None
        closest_red = None
        for blue_cp in self.player_points():
            for red_cp in self.enemy_points():
                if (blue_cp, red_cp) in seen:
                    continue
                seen.add((blue_cp, red_cp))
                seen.add((red_cp, blue_cp))

                dist = red_cp.position.distance_to_point(blue_cp.position)
                if dist < min_distance:
                    closest_red = red_cp
                    closest_blue = blue_cp
                    min_distance = dist

        assert closest_blue is not None
        assert closest_red is not None
        return closest_blue, closest_red

    def find_control_point_by_id(self, cp_id: UUID) -> ControlPoint:
        for i in self.controlpoints:
            if i.id == cp_id:
                return i
        raise KeyError(f"Cannot find ControlPoint with ID {cp_id}")

    def find_control_point_by_airport_id(self, airport_id: int) -> ControlPoint:
        for cp in self.controlpoints:
            if cp.dcs_airport is not None and cp.dcs_airport.id == airport_id:
                return cp
        raise KeyError(f"Cannot find ControlPoint with airport ID {airport_id}")

    def control_point_named(self, name: str) -> ControlPoint:
        for cp in self.controlpoints:
            if cp.name == name:
                return cp
        raise KeyError(f"Cannot find ControlPoint named {name}")

    def heading_to_conflict_from(self, position: Point) -> Optional[Heading]:
        # Heading for a Group to the enemy.
        # Should be the point between the nearest and the most distant conflict
        conflicts: dict[MissionTarget, float] = {}

        for conflict in self.conflicts():
            conflicts[conflict] = conflict.position.distance_to_point(position)

        if len(conflicts) == 0:
            return None

        sorted_conflicts = [
            k for k, v in sorted(conflicts.items(), key=lambda item: item[1])
        ]
        last = len(sorted_conflicts) - 1

        conflict_center = sorted_conflicts[0].position.midpoint(
            sorted_conflicts[last].position
        )

        return Heading.from_degrees(position.heading_between_point(conflict_center))
