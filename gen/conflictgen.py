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


GROUND_DISTANCE_FACTOR = 0.8
GROUNDINTERCEPT_DISTANCE_FACTOR = 3
AIR_DISTANCE = 32000

INTERCEPT_ATTACKERS_HEADING = -45, 45
INTERCEPT_DEFENDERS_HEADING = -10, 10
INTERCEPT_ATTACKERS_DISTANCE = 60000
INTERCEPT_DEFENDERS_DISTANCE = 30000
INTERCEPT_MAX_DISTANCE = 80000
INTERCEPT_MIN_DISTANCE = 45000

NAVAL_INTERCEPT_DISTANCE_FACTOR = 1.3
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

    @classmethod
    def capture_conflict(self, attacker: Country, defender: Country, from_cp, to_cp):
        attack_heading = to_cp.find_radial(to_cp.position.heading_between_point(from_cp.position))
        defense_heading = to_cp.find_radial(from_cp.position.heading_between_point(to_cp.position), ignored_radial=attack_heading)
        position = to_cp.position

        instance = self()
        instance.attackers_side = attacker
        instance.defenders_side = defender
        instance.from_cp = from_cp
        instance.to_cp = to_cp
        instance.position = position
        instance.size = to_cp.size
        instance.radials = to_cp.radials

        instance.ground_attackers_location = instance.position.point_from_heading(attack_heading, instance.size * GROUND_DISTANCE_FACTOR)
        instance.ground_defenders_location = instance.position.point_from_heading(defense_heading, instance.size * GROUND_DISTANCE_FACTOR)

        instance.air_attackers_location = instance.position.point_from_heading(attack_heading, AIR_DISTANCE)
        instance.air_defenders_location = instance.position.point_from_heading(defense_heading, AIR_DISTANCE)

        return instance

    @classmethod
    def intercept_conflict(self, attacker: Country, defender: Country, from_cp, to_cp):
        from theater.conflicttheater import SIZE_REGULAR
        from theater.conflicttheater import ALL_RADIALS

        heading = _heading_sum(from_cp.position.heading_between_point(to_cp.position), random.choice([-1, 1]) * random.randint(60, 100))

        raw_distance = from_cp.position.distance_to_point(to_cp.position) * 0.4
        distance = max(min(raw_distance, INTERCEPT_MAX_DISTANCE), INTERCEPT_MIN_DISTANCE)
        position = from_cp.position.point_from_heading(heading, distance)

        instance = self()
        instance.from_cp = from_cp
        instance.to_cp = to_cp
        instance.attackers_side = attacker
        instance.defenders_side = defender

        instance.position = position
        instance.size = SIZE_REGULAR
        instance.radials = ALL_RADIALS

        instance.air_attackers_location = instance.position.point_from_heading(random.randint(*INTERCEPT_ATTACKERS_HEADING) + heading, INTERCEPT_ATTACKERS_DISTANCE)
        instance.air_defenders_location = instance.position

        return instance

    @classmethod
    def ground_intercept_conflict(self, attacker: Country, defender: Country, heading: int, from_cp, to_cp):
        instance = self()
        instance.from_cp = from_cp
        instance.to_cp = to_cp
        instance.attackers_side = attacker
        instance.defenders_side = defender

        instance.position = to_cp.position
        instance.size = to_cp.size
        instance.radials = to_cp.radials

        instance.air_attackers_location = instance.position.point_from_heading(random.randint(*INTERCEPT_ATTACKERS_HEADING) + heading, AIR_DISTANCE)
        instance.ground_defenders_location = instance.position.point_from_heading(random.choice(to_cp.radials), instance.size * GROUNDINTERCEPT_DISTANCE_FACTOR)

        return instance

    @classmethod
    def naval_intercept_conflict(cls, attacker: Country, defender: Country, theater: ConflictTheater, from_cp: ControlPoint, to_cp: ControlPoint):
        radial = random.choice(to_cp.sea_radials)

        initial_distance = int(from_cp.position.distance_to_point(to_cp.position) * NAVAL_INTERCEPT_DISTANCE_FACTOR)
        position = to_cp.position.point_from_heading(radial, initial_distance)
        for offset in range(0, initial_distance, NAVAL_INTERCEPT_STEP):
            if theater.is_on_land(position):
                break
            else:
                position = to_cp.position.point_from_heading(radial, offset)

        instance = cls()
        instance.from_cp = from_cp
        instance.to_cp = to_cp
        instance.attackers_side = attacker
        instance.defenders_side = defender

        instance.position = position
        instance.size = SIZE_REGULAR
        instance.radials = to_cp.radials

        attacker_heading = from_cp.position.heading_between_point(to_cp.position)
        instance.air_attackers_location = instance.position.point_from_heading(attacker_heading, AIR_DISTANCE)
        instance.air_defenders_location = instance.position.point_from_heading(_opposite_heading(attacker_heading), AIR_DISTANCE)

        return instance
