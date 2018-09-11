import logging
import typing
import pdb
import dcs

from random import randint
from dcs import Mission

from dcs.mission import *
from dcs.vehicles import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.mapping import *
from dcs.point import *
from dcs.task import *
from dcs.country import *

from theater import *

AIR_DISTANCE = 40000

CAPTURE_AIR_ATTACKERS_DISTANCE = 25000
CAPTURE_AIR_DEFENDERS_DISTANCE = 60000
STRIKE_AIR_ATTACKERS_DISTANCE = 45000
STRIKE_AIR_DEFENDERS_DISTANCE = 25000

CAP_CAS_DISTANCE = 10000, 120000

GROUND_INTERCEPT_SPREAD = 5000
GROUND_DISTANCE_FACTOR = 1
GROUND_DISTANCE = 4000

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
    attackers_side = None  # type: Country
    defenders_side = None  # type: Country
    from_cp = None  # type: ControlPoint
    to_cp = None  # type: ControlPoint
    position = None  # type: Point
    size = None  # type: int
    radials = None  # type: typing.List[int]

    heading = None  # type: int
    distance = None  # type: int

    ground_attackers_location = None  # type: Point
    ground_defenders_location = None  # type: Point
    air_attackers_location = None  # type: Point
    air_defenders_location = None  # type: Point

    def __init__(self,
                 theater: ConflictTheater,
                 from_cp: ControlPoint,
                 to_cp: ControlPoint,
                 attackers_side: Country,
                 defenders_side: Country,
                 position: Point,
                 heading=None,
                 distance=None,
                 ground_attackers_location: Point = None,
                 ground_defenders_location: Point = None,
                 air_attackers_location: Point = None,
                 air_defenders_location: Point = None):
        self.attackers_side = attackers_side
        self.defenders_side = defenders_side
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

    def find_insertion_point(self, other_point: Point) -> Point:
        dx = self.position.x - self.tail.x
        dy = self.position.y - self.tail.y
        dr2 = float(dx ** 2 + dy ** 2)

        lerp = ((other_point.x - self.tail.x) * dx + (other_point.y - self.tail.y) * dy) / dr2
        if lerp < 0:
            lerp = 0
        elif lerp > 1:
            lerp = 1

        x = lerp * dx + self.tail.x
        y = lerp * dy + self.tail.y
        return Point(x, y)

    def find_ground_position(self, at: Point, heading: int, max_distance: int = 40000) -> typing.Optional[Point]:
        return Conflict._find_ground_position(at, max_distance, heading, self.theater)

    @classmethod
    def has_frontline_between(cls, from_cp: ControlPoint, to_cp: ControlPoint) -> bool:
        return from_cp.has_frontline and to_cp.has_frontline

    @classmethod
    def frontline_position(cls, from_cp: ControlPoint, to_cp: ControlPoint) -> typing.Tuple[Point, int]:
        distance = max(from_cp.position.distance_to_point(to_cp.position) * FRONTLINE_DISTANCE_STRENGTH_FACTOR * to_cp.base.strength, FRONTLINE_MIN_CP_DISTANCE)
        heading = to_cp.position.heading_between_point(from_cp.position)
        return to_cp.position.point_from_heading(heading, distance), heading

    @classmethod
    def frontline_vector(cls, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater) -> typing.Tuple[Point, int, int]:
        center_position, heading = cls.frontline_position(from_cp, to_cp)
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
        print("{} - {} {}".format(from_cp, to_cp, center_position))

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

    @classmethod
    def _find_ground_position(cls, initial: Point, max_distance: int, heading: int, theater: ConflictTheater) -> typing.Optional[Point]:
        pos = initial
        for _ in range(0, int(max_distance), 500):
            if theater.is_on_land(pos):
                return pos

            pos = pos.point_from_heading(heading, 500)

        logging.info("Didn't find ground position!")
        return None

    @classmethod
    def capture_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        position = to_cp.position
        attack_raw_heading = to_cp.position.heading_between_point(from_cp.position)
        attack_heading = to_cp.find_radial(attack_raw_heading)
        defense_heading = to_cp.find_radial(from_cp.position.heading_between_point(to_cp.position), ignored_radial=attack_heading)

        distance = GROUND_DISTANCE
        attackers_location = position.point_from_heading(attack_heading, distance)
        attackers_location = Conflict._find_ground_position(attackers_location, distance * 2, attack_heading, theater)

        defenders_location = position.point_from_heading(defense_heading, 0)
        defenders_location = Conflict._find_ground_position(defenders_location, distance * 2, defense_heading, theater)

        return cls(
            position=position,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            ground_attackers_location=attackers_location,
            ground_defenders_location=defenders_location,
            air_attackers_location=position.point_from_heading(attack_raw_heading, CAPTURE_AIR_ATTACKERS_DISTANCE),
            air_defenders_location=position.point_from_heading(_opposite_heading(attack_raw_heading), CAPTURE_AIR_DEFENDERS_DISTANCE)
        )

    @classmethod
    def strike_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        position = to_cp.position
        attack_raw_heading = to_cp.position.heading_between_point(from_cp.position)
        attack_heading = to_cp.find_radial(attack_raw_heading)
        defense_heading = to_cp.find_radial(from_cp.position.heading_between_point(to_cp.position), ignored_radial=attack_heading)

        distance = to_cp.size * GROUND_DISTANCE_FACTOR
        attackers_location = position.point_from_heading(attack_heading, distance)
        attackers_location = Conflict._find_ground_position(attackers_location, distance * 2, _heading_sum(attack_heading, 180), theater)

        defenders_location = position.point_from_heading(defense_heading, distance)
        defenders_location = Conflict._find_ground_position(defenders_location, distance * 2, _heading_sum(defense_heading, 180), theater)

        return cls(
            position=position,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            ground_attackers_location=attackers_location,
            ground_defenders_location=defenders_location,
            air_attackers_location=position.point_from_heading(attack_raw_heading, STRIKE_AIR_ATTACKERS_DISTANCE),
            air_defenders_location=position.point_from_heading(_opposite_heading(attack_raw_heading), STRIKE_AIR_DEFENDERS_DISTANCE)
        )

    @classmethod
    def intercept_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        raw_distance = from_cp.position.distance_to_point(to_cp.position) * 1.5
        distance = max(min(raw_distance, INTERCEPT_MAX_DISTANCE), INTERCEPT_MIN_DISTANCE)

        heading = _heading_sum(from_cp.position.heading_between_point(to_cp.position), random.choice([-1, 1]) * random.randint(60, 100))
        position = from_cp.position.point_from_heading(heading, distance)

        return cls(
            position=position.point_from_heading(position.heading_between_point(to_cp.position), INTERCEPT_CONFLICT_DISTANCE),
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            ground_attackers_location=None,
            ground_defenders_location=None,
            air_attackers_location=position.point_from_heading(random.randint(*INTERCEPT_ATTACKERS_HEADING) + heading, INTERCEPT_ATTACKERS_DISTANCE),
            air_defenders_location=position
        )

    @classmethod
    def ground_attack_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        heading = random.choice(to_cp.radials)
        initial_location = to_cp.position.random_point_within(*GROUND_ATTACK_DISTANCE)
        position = Conflict._find_ground_position(initial_location, GROUND_INTERCEPT_SPREAD, _heading_sum(heading, 180), theater)
        if not position:
            heading = to_cp.find_radial(to_cp.position.heading_between_point(from_cp.position))
            position = to_cp.position.point_from_heading(heading, to_cp.size * GROUND_DISTANCE_FACTOR)

        return cls(
            position=position,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            ground_attackers_location=position,
            ground_defenders_location=None,
            air_attackers_location=None,
            air_defenders_location=position.point_from_heading(heading, AIR_DISTANCE),
        )

    @classmethod
    def frontline_cas_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        assert cls.has_frontline_between(from_cp, to_cp)
        position, heading, distance = cls.frontline_vector(from_cp, to_cp, theater)

        return cls(
            position=position,
            heading=heading,
            distance=distance,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            ground_attackers_location=None,
            ground_defenders_location=None,
            air_attackers_location=position.point_from_heading(random.randint(*INTERCEPT_ATTACKERS_HEADING) + heading, AIR_DISTANCE),
            air_defenders_location=position.point_from_heading(random.randint(*INTERCEPT_ATTACKERS_HEADING) + _opposite_heading(heading), AIR_DISTANCE),
        )

    @classmethod
    def frontline_cap_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        assert cls.has_frontline_between(from_cp, to_cp)

        position, heading, distance = cls.frontline_vector(from_cp, to_cp, theater)
        attack_position = position.point_from_heading(heading, randint(0, int(distance)))
        attackers_position = attack_position.point_from_heading(heading - 90, AIR_DISTANCE)
        defenders_position = attack_position.point_from_heading(heading + 90, random.randint(*CAP_CAS_DISTANCE))

        return cls(
            position=position,
            heading=heading,
            distance=distance,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            air_attackers_location=attackers_position,
            air_defenders_location=defenders_position,
        )

    @classmethod
    def ground_base_attack(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        position = to_cp.position
        attack_heading = to_cp.find_radial(to_cp.position.heading_between_point(from_cp.position))
        defense_heading = to_cp.find_radial(from_cp.position.heading_between_point(to_cp.position), ignored_radial=attack_heading)

        distance = to_cp.size * GROUND_DISTANCE_FACTOR
        defenders_location = position.point_from_heading(defense_heading, distance)
        defenders_location = Conflict._find_ground_position(defenders_location, distance * 2, _heading_sum(defense_heading, 180), theater)

        return cls(
            position=position,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            ground_attackers_location=None,
            ground_defenders_location=defenders_location,
            air_attackers_location=position.point_from_heading(attack_heading, AIR_DISTANCE),
            air_defenders_location=position
        )

    @classmethod
    def naval_intercept_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        radial = random.choice(to_cp.sea_radials)

        initial_distance = min(int(from_cp.position.distance_to_point(to_cp.position) * NAVAL_INTERCEPT_DISTANCE_FACTOR), NAVAL_INTERCEPT_DISTANCE_MAX)
        initial_position = to_cp.position.point_from_heading(radial, initial_distance)
        for offset in range(0, initial_distance, NAVAL_INTERCEPT_STEP):
            position = initial_position.point_from_heading(_opposite_heading(radial), offset)

            if not theater.is_on_land(position):
                break

        attacker_heading = from_cp.position.heading_between_point(to_cp.position)
        return cls(
            position=position,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            ground_attackers_location=None,
            ground_defenders_location=position,
            air_attackers_location=position.point_from_heading(attacker_heading, AIR_DISTANCE),
            air_defenders_location=position.point_from_heading(_opposite_heading(attacker_heading), AIR_DISTANCE)
        )

    @classmethod
    def transport_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        frontline_position, heading = cls.frontline_position(from_cp, to_cp)
        initial_dest = frontline_position.point_from_heading(heading, TRANSPORT_FRONTLINE_DIST)
        dest = cls._find_ground_position(initial_dest, from_cp.position.distance_to_point(to_cp.position) / 3, heading, theater)
        if not dest:
            radial = to_cp.find_radial(to_cp.position.heading_between_point(from_cp.position))
            dest = to_cp.position.point_from_heading(radial, to_cp.size * GROUND_DISTANCE_FACTOR)

        return cls(
            position=dest,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            ground_attackers_location=from_cp.position,
            ground_defenders_location=frontline_position,
            air_attackers_location=from_cp.position.point_from_heading(0, 100),
            air_defenders_location=frontline_position
        )