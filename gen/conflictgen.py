import logging
from typing import Tuple, Optional

from dcs.country import Country
from dcs.mapping import Point
from shapely.geometry import LineString, Point as ShapelyPoint

from game.theater.conflicttheater import ConflictTheater, FrontLine
from game.theater.controlpoint import ControlPoint
from game.utils import heading_sum, opposite_heading


FRONTLINE_LENGTH = 80000

class Conflict:
    def __init__(self,
                 theater: ConflictTheater,
                 from_cp: ControlPoint,
                 to_cp: ControlPoint,
                 attackers_side: str,
                 defenders_side: str,
                 attackers_country: Country,
                 defenders_country: Country,
                 position: Point,
                 heading: Optional[int] = None,
                 size: Optional[int] = None
                 ):

        self.attackers_side = attackers_side
        self.defenders_side = defenders_side
        self.attackers_country = attackers_country
        self.defenders_country = defenders_country

        self.from_cp = from_cp
        self.to_cp = to_cp
        self.theater = theater
        self.position = position
        self.heading = heading
        self.size = size

    @classmethod
    def has_frontline_between(cls, from_cp: ControlPoint, to_cp: ControlPoint) -> bool:
        return from_cp.has_frontline and to_cp.has_frontline

    @classmethod
    def frontline_position(cls, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater) -> Tuple[Point, int]:
        frontline = FrontLine(from_cp, to_cp, theater)
        attack_heading = frontline.attack_heading
        position = cls.find_ground_position(frontline.position, FRONTLINE_LENGTH, heading_sum(attack_heading, 90), theater)
        return position, opposite_heading(attack_heading)

    @classmethod
    def frontline_vector(cls, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater) -> Tuple[Point, int, int]:
        """
        Returns a vector for a valid frontline location avoiding exclusion zones.
        """
        center_position, heading = cls.frontline_position(from_cp, to_cp, theater)
        left_heading = heading_sum(heading, -90)
        right_heading = heading_sum(heading, 90)
        left_position = cls.extend_ground_position(center_position, int(FRONTLINE_LENGTH / 2), left_heading, theater)
        right_position = cls.extend_ground_position(center_position, int(FRONTLINE_LENGTH / 2), right_heading, theater)
        distance = int(left_position.distance_to_point(right_position))
        return left_position, right_heading, distance

    @classmethod
    def frontline_cas_conflict(cls, attacker_name: str, defender_name: str, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        assert cls.has_frontline_between(from_cp, to_cp)
        position, heading, distance = cls.frontline_vector(from_cp, to_cp, theater)
        conflict = cls(
            position=position,
            heading=heading,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker_name,
            defenders_side=defender_name,
            attackers_country=attacker,
            defenders_country=defender,
            size=distance
        )
        return conflict

    @classmethod
    def extend_ground_position(cls, initial: Point, max_distance: int, heading: int, theater: ConflictTheater) -> Point:
        """Finds the first intersection with an exclusion zone in one heading from an initial point up to max_distance"""
        extended = initial.point_from_heading(heading, max_distance)
        if theater.landmap is None:
            # TODO: Why is this possible?
            return extended

        p0 = ShapelyPoint(initial.x, initial.y)
        p1 = ShapelyPoint(extended.x, extended.y)
        line = LineString([p0, p1])

        intersection = line.intersection(
            theater.landmap.inclusion_zone_only.boundary)
        if intersection.is_empty:
            # Max extent does not intersect with the boundary of the inclusion
            # zone, so the full front line is usable. This does assume that the
            # front line was centered on a valid location.
            return extended

        # Otherwise extend the front line only up to the intersection.
        return initial.point_from_heading(heading, p0.distance(intersection))

    @classmethod
    def find_ground_position(cls, initial: Point, max_distance: int, heading: int, theater: ConflictTheater, coerce=True) -> Optional[Point]:
        """
        Finds the nearest valid ground position along a provided heading and it's inverse up to max_distance.
        `coerce=True` will return the closest land position to `initial` regardless of heading or distance
        `coerce=False` will return None if a point isn't found
        """
        pos = initial
        if theater.is_on_land(pos):
            return pos
        for distance in range(0, int(max_distance), 100):
            pos = initial.point_from_heading(heading, distance)
            if theater.is_on_land(pos):
                return pos
            pos = initial.point_from_heading(opposite_heading(heading), distance)
        if coerce:
            pos = theater.nearest_land_pos(initial)
            return pos
        logging.error("Didn't find ground position ({})!".format(initial))
        return None
        
