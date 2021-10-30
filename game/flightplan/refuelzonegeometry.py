from __future__ import annotations

from typing import TYPE_CHECKING

import shapely.ops
from dcs import Point
from shapely.geometry import Point as ShapelyPoint, MultiPolygon

from game.utils import nautical_miles, meters

if TYPE_CHECKING:
    from game.coalition import Coalition
    from game.theater import ConflictTheater


class RefuelZoneGeometry:
    def __init__(
        self,
        package_home: Point,
        join: Point,
        coalition: Coalition,
    ) -> None:
        self.package_home = package_home
        self.join = join
        self.coalition = coalition

    def find_best_refuel_point(self) -> Point:
        # Do simple at first.
        # TODO: Consider threats.
        distance = 0.75 * self.package_home.distance_to_point(self.join)
        heading = self.package_home.heading_between_point(self.join)
        self.package_home.point_from_heading(heading, distance)
