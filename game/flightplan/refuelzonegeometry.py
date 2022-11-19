from __future__ import annotations

from typing import TYPE_CHECKING

from dcs import Point

if TYPE_CHECKING:
    from game.coalition import Coalition


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
        # TODO: Avoid threatened areas, minimize backtracking.
        # https://github.com/dcs-liberation/dcs_liberation/issues/2542
        distance = 0.75 * self.package_home.distance_to_point(self.join)
        heading = self.package_home.heading_between_point(self.join)
        return self.package_home.point_from_heading(heading, distance)
