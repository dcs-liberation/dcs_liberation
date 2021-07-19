from __future__ import annotations

import logging
from typing import Tuple, Optional

from dcs.country import Country
from dcs.mapping import Point
from shapely.geometry import LineString, Point as ShapelyPoint

from game.theater.conflicttheater import ConflictTheater, FrontLine
from game.theater.controlpoint import ControlPoint
from game.utils import Heading


FRONTLINE_LENGTH = 80000


class Conflict:
    def __init__(
        self,
        theater: ConflictTheater,
        front_line: FrontLine,
        attackers_side: str,
        defenders_side: str,
        attackers_country: Country,
        defenders_country: Country,
        position: Point,
        heading: Optional[Heading] = None,
        size: Optional[int] = None,
    ):

        self.attackers_side = attackers_side
        self.defenders_side = defenders_side
        self.attackers_country = attackers_country
        self.defenders_country = defenders_country

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
    def has_frontline_between(cls, from_cp: ControlPoint, to_cp: ControlPoint) -> bool:
        return from_cp.has_frontline and to_cp.has_frontline

    @classmethod
    def frontline_position(
        cls, frontline: FrontLine, theater: ConflictTheater
    ) -> Tuple[Point, Heading]:
        attack_heading = frontline.attack_heading
        position = cls.find_ground_position(
            frontline.position,
            FRONTLINE_LENGTH,
            attack_heading.right,
            theater,
        )
        if position is None:
            raise RuntimeError("Could not find front line position")
        return position, attack_heading.opposite

    @classmethod
    def frontline_vector(
        cls, front_line: FrontLine, theater: ConflictTheater
    ) -> Tuple[Point, Heading, int]:
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
        distance = int(left_position.distance_to_point(right_position))
        return left_position, right_heading, distance

    @classmethod
    def frontline_cas_conflict(
        cls,
        attacker_name: str,
        defender_name: str,
        attacker: Country,
        defender: Country,
        front_line: FrontLine,
        theater: ConflictTheater,
    ) -> Conflict:
        assert cls.has_frontline_between(front_line.blue_cp, front_line.red_cp)
        position, heading, distance = cls.frontline_vector(front_line, theater)
        conflict = cls(
            position=position,
            heading=heading,
            theater=theater,
            front_line=front_line,
            attackers_side=attacker_name,
            defenders_side=defender_name,
            attackers_country=attacker,
            defenders_country=defender,
            size=distance,
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
        coerce: bool = True,
    ) -> Optional[Point]:
        """
        Finds the nearest valid ground position along a provided heading and it's inverse up to max_distance.
        `coerce=True` will return the closest land position to `initial` regardless of heading or distance
        `coerce=False` will return None if a point isn't found
        """
        pos = initial
        if theater.is_on_land(pos):
            return pos
        for distance in range(0, int(max_distance), 100):
            pos = initial.point_from_heading(heading.degrees, distance)
            if theater.is_on_land(pos):
                return pos
            pos = initial.point_from_heading(heading.opposite.degrees, distance)
            if theater.is_on_land(pos):
                return pos
        if coerce:
            pos = theater.nearest_land_pos(initial)
            return pos
        logging.error("Didn't find ground position ({})!".format(initial))
        return None
