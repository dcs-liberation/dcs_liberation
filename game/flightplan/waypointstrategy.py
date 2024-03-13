from __future__ import annotations

import math
from abc import abstractmethod, ABC
from collections.abc import Iterator, Callable
from dataclasses import dataclass
from typing import Any

from dcs.mapping import heading_between_points
from shapely.geometry import Point, MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry as Geometry, BaseGeometry
from shapely.ops import nearest_points

from game.utils import Distance, nautical_miles, Heading


def angle_between_points(a: Point, b: Point) -> float:
    return heading_between_points(a.x, a.y, b.x, b.y)


def point_at_heading(p: Point, heading: Heading, distance: Distance) -> Point:
    rad_heading = heading.radians
    return Point(
        p.x + math.cos(rad_heading) * distance.meters,
        p.y + math.sin(rad_heading) * distance.meters,
    )


class Prerequisite(ABC):
    @abstractmethod
    def is_satisfied(self) -> bool:
        ...

    @abstractmethod
    def describe_debug_info(
        self, to_geojson: Callable[[BaseGeometry], dict[str, Any]]
    ) -> dict[str, Any]:
        ...


class DistancePrerequisite(Prerequisite):
    def __init__(self, a: Point, b: Point, min_range: Distance) -> None:
        self.a = a
        self.b = b
        self.min_range = min_range

    def is_satisfied(self) -> bool:
        return self.a.distance(self.b) >= self.min_range.meters

    def describe_debug_info(
        self, to_geojson: Callable[[BaseGeometry], dict[str, Any]]
    ) -> dict[str, Any]:
        return {
            "requirement": f"at least {self.min_range} between",
            "satisfied": self.is_satisfied(),
            "subject": to_geojson(self.a),
            "target": to_geojson(self.b),
        }


class SafePrerequisite(Prerequisite):
    def __init__(self, point: Point, threat_zones: MultiPolygon) -> None:
        self.point = point
        self.threat_zones = threat_zones

    def is_satisfied(self) -> bool:
        return not self.point.intersects(self.threat_zones)

    def describe_debug_info(
        self, to_geojson: Callable[[BaseGeometry], dict[str, Any]]
    ) -> dict[str, Any]:
        return {
            "requirement": "is safe",
            "satisfied": self.is_satisfied(),
            "subject": to_geojson(self.point),
        }


class PrerequisiteBuilder:
    def __init__(
        self, subject: Point, threat_zones: MultiPolygon, strategy: WaypointStrategy
    ) -> None:
        self.subject = subject
        self.threat_zones = threat_zones
        self.strategy = strategy

    def is_safe(self) -> None:
        self.strategy.add_prerequisite(
            SafePrerequisite(self.subject, self.threat_zones)
        )

    def min_distance_from(self, target: Point, distance: Distance) -> None:
        self.strategy.add_prerequisite(
            DistancePrerequisite(self.subject, target, distance)
        )


@dataclass(frozen=True)
class ThreatTolerance:
    target: Point
    target_buffer: Distance
    tolerance: Distance


class RequirementBuilder:
    def __init__(self, threat_zones: MultiPolygon, strategy: WaypointStrategy) -> None:
        self.threat_zones = threat_zones
        self.strategy = strategy

    def safe(self) -> None:
        self.strategy.exclude_threat_zone()

    def at_least(self, distance: Distance) -> DistanceRequirementBuilder:
        return DistanceRequirementBuilder(self.strategy, min_distance=distance)

    def at_most(self, distance: Distance) -> DistanceRequirementBuilder:
        return DistanceRequirementBuilder(self.strategy, max_distance=distance)

    def maximum_turn_to(
        self, turn_point: Point, next_point: Point, turn_limit: Heading
    ) -> None:
        large_distance = nautical_miles(400)
        next_heading = Heading.from_degrees(
            angle_between_points(next_point, turn_point)
        )
        limit_ccw = point_at_heading(
            turn_point, next_heading - turn_limit, large_distance
        )
        limit_cw = point_at_heading(
            turn_point, next_heading + turn_limit, large_distance
        )

        allowed_wedge = Polygon([turn_point, limit_ccw, limit_cw])
        self.strategy.exclude(
            f"restrict turn from {turn_point} to {next_point} to {turn_limit}",
            turn_point.buffer(large_distance.meters).difference(allowed_wedge),
        )


class DistanceRequirementBuilder:
    def __init__(
        self,
        strategy: WaypointStrategy,
        min_distance: Distance | None = None,
        max_distance: Distance | None = None,
    ) -> None:
        if min_distance is None and max_distance is None:
            raise ValueError
        self.strategy = strategy
        self.min_distance = min_distance
        self.max_distance = max_distance

    def away_from(self, target: Point, description: str | None = None) -> None:
        if description is None:
            description = str(target)

        if self.min_distance is not None:
            self.strategy.exclude(
                f"at least {self.min_distance} away from {description}",
                target.buffer(self.min_distance.meters),
            )
        if self.max_distance is not None:
            self.strategy.exclude_beyond(
                f"at most {self.max_distance} away from {description}",
                target.buffer(self.max_distance.meters),
            )


@dataclass(frozen=True)
class WaypointDebugInfo:
    description: str
    geometry: BaseGeometry

    def to_geojson(
        self, to_geojson: Callable[[BaseGeometry], dict[str, Any]]
    ) -> dict[str, Any]:
        return {
            "type": "Feature",
            "properties": {
                "description": self.description,
            },
            "geometry": to_geojson(self.geometry),
        }


class WaypointStrategy:
    def __init__(self, threat_zones: MultiPolygon) -> None:
        self.threat_zones = threat_zones
        self.prerequisites: list[Prerequisite] = []
        self._max_area = Point(0, 0).buffer(2_000_000)
        self.allowed_area = self._max_area.buffer(0)
        self.debug_infos: list[WaypointDebugInfo] = []
        self._threat_tolerance: ThreatTolerance | None = None
        self.point_for_nearest_solution: Point | None = None

    def add_prerequisite(self, prerequisite: Prerequisite) -> None:
        self.prerequisites.append(prerequisite)

    def prerequisite(self, subject: Point) -> PrerequisiteBuilder:
        return PrerequisiteBuilder(subject, self.threat_zones, self)

    def exclude(self, description: str, geometry: Geometry) -> None:
        self.debug_infos.append(WaypointDebugInfo(description, geometry))
        self.allowed_area = self.allowed_area.difference(geometry)

    def exclude_beyond(self, description: str, geometry: Geometry) -> None:
        self.exclude(description, self._max_area.difference(geometry))

    def exclude_threat_zone(self) -> None:
        if (tolerance := self._threat_tolerance) is not None:
            description = (
                f"safe with a {tolerance.tolerance} tolerance to a "
                f"{tolerance.target_buffer} radius about {tolerance.target}"
            )
        else:
            description = "safe"
        self.exclude(description, self.threat_zones)

    def prerequisites_are_satisfied(self) -> bool:
        for prereq in self.prerequisites:
            if not prereq.is_satisfied():
                return False
        return True

    def require(self) -> RequirementBuilder:
        return RequirementBuilder(self.threat_zones, self)

    def threat_tolerance(
        self, target: Point, target_size: Distance, wiggle: Distance
    ) -> None:
        if self.threat_zones.is_empty:
            return

        min_distance_from_threat_to_target_buffer = target.buffer(
            target_size.meters
        ).distance(self.threat_zones.boundary)
        threat_mask = self.threat_zones.buffer(
            -min_distance_from_threat_to_target_buffer - wiggle.meters
        )
        self._threat_tolerance = ThreatTolerance(target, target_size, wiggle)
        self.threat_zones = self.threat_zones.difference(threat_mask)

    def nearest(self, point: Point) -> None:
        if self.point_for_nearest_solution is not None:
            raise RuntimeError("WaypointStrategy.nearest() called more than once")
        self.point_for_nearest_solution = point

    def find(self) -> Point | None:
        if self.point_for_nearest_solution is None:
            raise RuntimeError(
                "Must call WaypointStrategy.nearest() before WaypointStrategy.find()"
            )

        if not self.prerequisites_are_satisfied():
            return None

        try:
            return nearest_points(self.allowed_area, self.point_for_nearest_solution)[0]
        except ValueError:
            # No solutions.
            return None

    def iter_debug_info(self) -> Iterator[WaypointDebugInfo]:
        yield from self.debug_infos
        solution = self.find()
        if solution is None:
            return
        yield WaypointDebugInfo("solution", solution)
