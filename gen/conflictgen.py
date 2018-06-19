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


GROUND_DISTANCE_FACTOR = 1
GROUNDINTERCEPT_DISTANCE_FACTOR = 6
AIR_DISTANCE = 32000

INTERCEPT_ATTACKERS_HEADING = -45, 45
INTERCEPT_DEFENDERS_HEADING = -10, 10
INTERCEPT_ATTACKERS_DISTANCE = 60000
INTERCEPT_DEFENDERS_DISTANCE = 30000
INTERCEPT_MAX_DISTANCE = 80000
INTERCEPT_MIN_DISTANCE = 45000

NAVAL_INTERCEPT_DISTANCE_FACTOR = 1.3
NAVAL_INTERCEPT_DISTANCE_MAX = 90000
NAVAL_INTERCEPT_STEP = 3000


def _opposite_heading(h):
    return h+180


def _heading_sum(h, a) -> int:
    h += a
    if h > 360:
        return h - 360
    elif h < 0:
        return 360 - h
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

    ground_attackers_location = None  # type: Point
    ground_defenders_location = None  # type: Point
    air_attackers_location = None  # type: Point
    air_defenders_location = None  # type: Point

    def __init__(self,
                 position: Point,
                 theater: ConflictTheater,
                 from_cp: ControlPoint,
                 to_cp: ControlPoint,
                 attackers_side: Country,
                 defenders_side: Country,
                 ground_attackers_location: Point,
                 ground_defenders_location: Point,
                 air_attackers_location: Point,
                 air_defenders_location: Point):
        self.attackers_side = attackers_side
        self.defenders_side = defenders_side
        self.from_cp = from_cp
        self.to_cp = to_cp
        self.theater = theater
        self.position = position
        self.size = to_cp.size
        self.radials = to_cp.radials
        self.ground_attackers_location = ground_attackers_location
        self.ground_defenders_location = ground_defenders_location
        self.air_attackers_location = air_attackers_location
        self.air_defenders_location = air_defenders_location

    @classmethod
    def _find_ground_location(cls, initial: Point, max_distance: int, heading: int, theater: ConflictTheater) -> Point:
        for _ in range(0, int(max_distance), 100):
            if theater.is_on_land(initial):
                return initial

            initial = initial.point_from_heading(heading, 100)
        return initial

    @classmethod
    def capture_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        position = to_cp.position
        attack_heading = to_cp.find_radial(to_cp.position.heading_between_point(from_cp.position))
        defense_heading = to_cp.find_radial(from_cp.position.heading_between_point(to_cp.position), ignored_radial=attack_heading)

        distance = to_cp.size * GROUND_DISTANCE_FACTOR
        attackers_location = position.point_from_heading(attack_heading, distance)
        attackers_location = Conflict._find_ground_location(attackers_location, distance * 2, _heading_sum(attack_heading, 180), theater)

        defenders_location = position.point_from_heading(defense_heading, distance)
        defenders_location = Conflict._find_ground_location(defenders_location, distance * 2, _heading_sum(defense_heading, 180), theater)

        return cls(
            position=position,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            ground_attackers_location=attackers_location,
            ground_defenders_location=defenders_location,
            air_attackers_location=position.point_from_heading(attack_heading, AIR_DISTANCE),
            air_defenders_location=position.point_from_heading(defense_heading, AIR_DISTANCE)
        )

    @classmethod
    def intercept_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        raw_distance = from_cp.position.distance_to_point(to_cp.position) * 0.4
        distance = max(min(raw_distance, INTERCEPT_MAX_DISTANCE), INTERCEPT_MIN_DISTANCE)

        heading = _heading_sum(from_cp.position.heading_between_point(to_cp.position), random.choice([-1, 1]) * random.randint(60, 100))
        position = from_cp.position.point_from_heading(heading, distance)

        return cls(
            position=position,
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
    def ground_intercept_conflict(cls, attacker: Country, defender: Country, heading: int, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        heading = random.choice(to_cp.radials)
        initial_location = to_cp.position.point_from_heading(heading, to_cp.size * GROUNDINTERCEPT_DISTANCE_FACTOR),
        max_distance = to_cp.size * GROUNDINTERCEPT_DISTANCE_FACTOR
        ground_location = Conflict._find_ground_location(initial_location, max_distance, _heading_sum(heading, 180), theater)

        return cls(
            position=to_cp.position,
            theater=theater,
            from_cp=from_cp,
            to_cp=to_cp,
            attackers_side=attacker,
            defenders_side=defender,
            ground_attackers_location=None,
            ground_defenders_location=ground_location,
            air_attackers_location=to_cp.position.point_from_heading(random.randint(*INTERCEPT_ATTACKERS_HEADING) + heading, AIR_DISTANCE),
            air_defenders_location=to_cp.position.point_from_heading(random.randint(*INTERCEPT_ATTACKERS_HEADING) + _opposite_heading(heading), AIR_DISTANCE)
        )

    @classmethod
    def intercept_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        raw_distance = from_cp.position.distance_to_point(to_cp.position) * 0.4
        distance = max(min(raw_distance, INTERCEPT_MAX_DISTANCE), INTERCEPT_MIN_DISTANCE)

        heading = _heading_sum(from_cp.position.heading_between_point(to_cp.position), random.choice([-1, 1]) * random.randint(60, 100))
        position = from_cp.position.point_from_heading(heading, distance)

        return cls(
            position=position,
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
    def naval_intercept_conflict(cls, attacker: Country, defender: Country, from_cp: ControlPoint, to_cp: ControlPoint, theater: ConflictTheater):
        radial = random.choice(to_cp.sea_radials)

        initial_distance = min(int(from_cp.position.distance_to_point(to_cp.position) * NAVAL_INTERCEPT_DISTANCE_FACTOR), NAVAL_INTERCEPT_DISTANCE_MAX)
        position = to_cp.position.point_from_heading(radial, initial_distance)
        for offset in range(0, initial_distance, NAVAL_INTERCEPT_STEP):
            if not theater.is_on_land(position):
                position = to_cp.position.point_from_heading(radial, initial_distance - offset)
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
