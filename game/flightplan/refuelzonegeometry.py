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
        target: Point,
        home: Point,
        hold: Point,
        ip: Point,
        join: Point,
        coalition: Coalition,
        theater: ConflictTheater,
    ) -> None:
        self.target = target
        self.home = home
        self.hold = hold
        self.ip = ip
        self.join = join
        self.coalition = coalition
        self.theater = theater
