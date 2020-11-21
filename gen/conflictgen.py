import logging
import random
from typing import Tuple

from dcs.country import Country
from dcs.mapping import Point

from theater import ConflictTheater, ControlPoint, FrontLine

AIR_DISTANCE = 40000

CAPTURE_AIR_ATTACKERS_DISTANCE = 25000
CAPTURE_AIR_DEFENDERS_DISTANCE = 60000
STRIKE_AIR_ATTACKERS_DISTANCE = 45000
STRIKE_AIR_DEFENDERS_DISTANCE = 25000

CAP_CAS_DISTANCE = 10000, 120000

GROUND_INTERCEPT_SPREAD = 5000
GROUND_DISTANCE_FACTOR = 1.4
GROUND_DISTANCE = 2000

GROUND_ATTACK_DISTANCE = 25000, 13000

TRANSPORT_FRONTLINE_DIST = 1800

INTERCEPT_ATTACKERS_HEADING = -45, 45
INTERCEPT_DEFENDERS_HEADING = -10, 10
INTERCEPT_CONFLICT_DISTANCE = 50000
INTERCEPT_ATTACKERS_DISTANCE = 100000
INTERCEPT_MAX_DISTANCE = 160000
INTERCEPT_MIN_DISTANCE = 100000

NAVAL_INTERCEPT_DISTANCE_FACTOR = 1
NAVAL_INTERCEPT_DISTANCE_MAX = 40000
NAVAL_INTERCEPT_STEP = 5000

FRONTLINE_LENGTH = 80000
FRONTLINE_MIN_CP_DISTANCE = 5000
FRONTLINE_DISTANCE_STRENGTH_FACTOR = 0.7


def _opposite_heading(h):
    return h+180


def _heading_sum(h, a) -> int:
    h += a
    if h > 360:
        return h - 360
    elif h < 0:
        return 360 + h
    else:
        return h


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
                 heading=None,
                 distance=None,
                 ground_attackers_location: Point = None,
                 ground_defenders_location: Point = None,
                 air_attackers_location: Point = None,
                 air_defenders_location: Point = None):

        self.attackers_side = attackers_side
        self.defenders_side = defenders_side
        self.attackers_country = attackers_country
        self.defenders_country = defenders_country

        self.from_cp = from_cp
        self.to_cp = to_cp
        self.theater = theater
        self.position = position
        self.heading = heading
        self.distance = distance
        self.size = to_cp.size
        self.radials = to_cp.radials
        self.ground_attackers_location = ground_attackers_location
        self.ground_defenders_location = ground_defenders_location
        self.air_attackers_location = air_attackers_location
        self.air_defenders_location = air_defenders_location

    @property
    def center(self) -> Point:
        return self.position.point_from_heading(self.heading, self.distance / 2)

    @property
    def tail(self) -> Point:
        return self.position.point_from_heading(self.heading, self.distance)

    @property
    def is_vector(self) -> bool:
        return self.heading is not None

    @property
    def opposite_heading(self) -> int:
        return _heading_sum(self.heading, 180)

    @property
    def to_size(self):
        return self.to_cp.size * GROUND_DISTANCE_FACTOR

    def find_ground_position(self, at: Point, heading: int, max_distance: int = 40000) -> Point:
        return Conflict._find_ground_position(at, max_distance, heading, self.theater)

    @classmethod
    def has_frontline_between(cls, from_cp: ControlPoint, to_cp: ControlPoint) -> bool:
        return from_cp.has_frontline and to_cp.has_frontline

    @staticmethod
    def frontline_position(from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater) -> Tuple[Point, int]:
        frontline = FrontLine(from_cp, to_cp, theater)
        attack_heading = frontline.attack_heading
        position = frontline.position
        return position, _opposite_heading(attack_heading)


    @classmethod
    def frontline_vector(cls, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater) -> Tuple[Point, int, int]:
        """
        probe_end_point = initial.point_from_heading(heading, FRONTLINE_LENGTH)
        probe = geometry.LineString([(initial.x, initial.y), (probe_end_point.x, probe_end_point.y) ])
        intersection = probe.intersection(theater.land_poly)

        if isinstance(intersection, geometry.LineString):
            intersection = intersection
        elif isinstance(intersection, geometry.MultiLineString):
            intersection = intersection.geoms[0]
        else:
            print(intersection)
            return None

        return Point(*intersection.xy[0]), _heading_sum(heading, 90), intersection.length
        """
        frontline = cls.frontline_position(from_cp, to_cp, theater)
        center_position, heading = frontline
        left_position, right_position = None, None

        if not theater.is_on_land(center_position):
            pos = cls._find_ground_position(center_position, FRONTLINE_LENGTH, _heading_sum(heading, -90), theater)
            if pos:
                right_position = pos
                center_position = pos
            else:
                pos = cls._find_ground_position(center_position, FRONTLINE_LENGTH, _heading_sum(heading, +90), theater)
                if pos:
                    left_position = pos
                    center_position = pos

        if left_position is None:
            left_position = cls._extend_ground_position(center_position, int(FRONTLINE_LENGTH/2), _heading_sum(heading, -90), theater)

        if right_position is None:
            right_position = cls._extend_ground_position(center_position, int(FRONTLINE_LENGTH/2), _heading_sum(heading, 90), theater)

        return left_position, _heading_sum(heading, 90), int(right_position.distance_to_point(left_position))

    @classmethod
    def _extend_ground_position(cls, initial: Point, max_distance: int, heading: int, theater: ConflictTheater) -> Point:
        pos = initial
        for offset in range(0, int(max_distance), 500):
            new_pos = initial.point_from_heading(heading, offset)
            if theater.is_on_land(new_pos):
                pos = new_pos
            else:
                return pos
        return pos

        """
        probe_end_point = initial.point_from_heading(heading, max_distance)
        probe = geometry.LineString([(initial.x, initial.y), (probe_end_point.x, probe_end_point.y)])

        intersection = probe.intersection(theater.land_poly)
        if intersection is geometry.LineString:
            return Point(*intersection.xy[1])
        elif intersection is geometry.MultiLineString:
            return Point(*intersection.geoms[0].xy[1])

        return None
        """

    @classmethod
    def _find_ground_position(cls, initial: Point, max_distance: int, heading: int, theater: ConflictTheater) -> Point:
        pos = initial
        for _ in range(0, int(max_distance), 100):
            if theater.is_on_land(pos):
                return pos

            pos = pos.point_from_heading(heading, 500)
        """
        probe_end_point = initial.point_from_heading(heading, max_distance)
        probe = geometry.LineString([(initial.x, initial.y), (probe_end_point.x, probe_end_point.y) ])

        intersection = probe.intersection(theater.land_poly)
        if isinstance(intersection, geometry.LineString):
            return Point(*intersection.xy[1])
        elif isinstance(intersection, geometry.MultiLineString):
            return Point(*intersection.geoms[0].xy[1])
        """

        logging.error("Didn't find ground position ({})!".format(initial))
        return initial
