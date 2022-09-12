from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Tuple

from dcs.mapping import Point
from shapely.geometry import LineString, Point as ShapelyPoint
from shapely.ops import nearest_points

from game.theater.conflicttheater import ConflictTheater, FrontLine
from game.theater.controlpoint import ControlPoint
from game.utils import Heading, dcs_to_shapely_point

FRONTLINE_LENGTH = 80000


@dataclass(frozen=True)
class FrontLineBounds:
    left_position: Point
    right_position: Point

    @cached_property
    def length(self) -> int:
        return int(self.left_position.distance_to_point(self.right_position))

    @cached_property
    def center(self) -> Point:
        return (self.left_position + self.right_position) / 2

    @cached_property
    def heading_from_left_to_right(self) -> Heading:
        return Heading(
            int(self.left_position.heading_between_point(self.right_position))
        )


class FrontLineConflictDescription:
    def __init__(
        self,
        theater: ConflictTheater,
        front_line: FrontLine,
        position: Point,
        heading: Optional[Heading] = None,
        size: Optional[int] = None,
    ):
        self.front_line = front_line
        self.theater = theater
        self.position = position
        self.heading = heading
        self.size = size

    @property
    def blue_cp(self) -> ControlPoint:
        return self.front_line.blue_cp

    @property
    def red_cp(self) -> ControlPoint:
        return self.front_line.red_cp

    @classmethod
    def frontline_position(
        cls, frontline: FrontLine, theater: ConflictTheater
    ) -> Tuple[Point, Heading]:
        attack_heading = frontline.blue_forward_heading
        position = cls.find_ground_position(
            frontline.position,
            FRONTLINE_LENGTH,
            attack_heading.right,
            theater,
        )
        return position, attack_heading.opposite

    @classmethod
    def frontline_bounds(
        cls, front_line: FrontLine, theater: ConflictTheater
    ) -> FrontLineBounds:
        """
        Returns a vector for a valid frontline location avoiding exclusion zones.
        """
        center_position, heading = cls.frontline_position(front_line, theater)
        left_heading = heading.left
        right_heading = heading.right
        left_position = cls.extend_ground_position(
            center_position, int(FRONTLINE_LENGTH / 2), left_heading, theater
        )
        right_position = cls.extend_ground_position(
            center_position, int(FRONTLINE_LENGTH / 2), right_heading, theater
        )
        return FrontLineBounds(left_position, right_position)

    @classmethod
    def frontline_cas_conflict(
        cls, front_line: FrontLine, theater: ConflictTheater
    ) -> FrontLineConflictDescription:
        # TODO: Break apart the front-line and air conflict descriptions.
        # We're wastefully not caching the front-line bounds here because air conflicts
        # can't compute bounds, only a position.
        bounds = cls.frontline_bounds(front_line, theater)
        conflict = FrontLineConflictDescription(
            position=bounds.left_position,
            heading=bounds.heading_from_left_to_right,
            theater=theater,
            front_line=front_line,
            size=bounds.length,
        )
        return conflict

    @classmethod
    def extend_ground_position(
        cls,
        initial: Point,
        max_distance: int,
        heading: Heading,
        theater: ConflictTheater,
    ) -> Point:
        """Finds the first intersection with an exclusion zone in one heading from an initial point up to max_distance"""
        extended = initial.point_from_heading(heading.degrees, max_distance)
        if theater.landmap is None:
            # TODO: Why is this possible?
            return extended

        p0 = ShapelyPoint(initial.x, initial.y)
        p1 = ShapelyPoint(extended.x, extended.y)
        line = LineString([p0, p1])

        intersection = line.intersection(theater.landmap.inclusion_zone_only.boundary)
        if intersection.is_empty:
            # Max extent does not intersect with the boundary of the inclusion
            # zone, so the full front line is usable. This does assume that the
            # front line was centered on a valid location.
            return extended

        # Otherwise extend the front line only up to the intersection.
        return initial.point_from_heading(heading.degrees, p0.distance(intersection))

    @classmethod
    def find_ground_position(
        cls,
        initial: Point,
        max_distance: int,
        heading: Heading,
        theater: ConflictTheater,
    ) -> Point:
        """Finds a valid ground position for the front line center.

        Checks for positions along the front line first. If none succeed, the nearest
        land position to the initial point is used.
        """
        if theater.landmap is None:
            return initial

        line = LineString(
            [
                dcs_to_shapely_point(
                    initial.point_from_heading(heading.degrees, max_distance)
                ),
                dcs_to_shapely_point(
                    initial.point_from_heading(heading.opposite.degrees, max_distance)
                ),
            ]
        )
        masked_front_line = theater.landmap.inclusion_zone_only.intersection(line)
        if masked_front_line.is_empty:
            return theater.nearest_land_pos(initial)
        nearest_good, _ = nearest_points(
            masked_front_line, dcs_to_shapely_point(initial)
        )
        return initial.new_in_same_map(nearest_good.x, nearest_good.y)
