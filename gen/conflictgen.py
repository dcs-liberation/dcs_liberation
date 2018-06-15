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

def _opposite_heading(h):
    return h+180

GROUND_DISTANCE_FACTOR = 2
AIR_DISTANCE = 32000

INTERCEPT_ATTACKERS_HEADING = -45, 45
INTERCEPT_DEFENDERS_HEADING = -10, 10
INTERCEPT_ATTACKERS_DISTANCE = 60000
INTERCEPT_DEFENDERS_DISTANCE = 30000
INTERCEPT_MAX_DISTANCE = 80000
INTERCEPT_MIN_DISTANCE = 45000


class Conflict:
    attackers_side = None  # type: Country
    defenders_side = None  # type: Country
    position = None  # type: Point
    size = None  # type: int
    radials = None  # type: typing.List[int]

    ground_attackers_location = None  # type: Point
    ground_defenders_location = None  # type: Point
    air_attackers_location = None  # type: Point
    air_defenders_location = None  # type: Point

    @classmethod
    def capture_conflict(self, attacker: Country, attack_heading: int, defender: Country, defense_heading: int, position: Point, size: int, radials: typing.Collection[int]):
        instance = self()
        instance.attackers_side = attacker
        instance.defenders_side = defender
        instance.position = position
        instance.size = size
        instance.radials = radials

        instance.ground_attackers_location = instance.position.point_from_heading(attack_heading, instance.size * GROUND_DISTANCE_FACTOR)
        instance.ground_defenders_location = instance.position.point_from_heading(defense_heading, instance.size * GROUND_DISTANCE_FACTOR)

        instance.air_attackers_location = instance.position.point_from_heading(attack_heading, AIR_DISTANCE)
        instance.air_defenders_location = instance.position.point_from_heading(defense_heading, AIR_DISTANCE)

        return instance

    @classmethod
    def intercept_conflict(self, attacker: Country, defender: Country, from_cp, to_cp):
        from theater.conflicttheater import SIZE_REGULAR
        from theater.conflicttheater import ALL_RADIALS

        heading = from_cp.position.heading_between_point(to_cp.position)
        raw_distance = from_cp.position.distance_to_point(to_cp.position) / 2
        distance = max(min(raw_distance, INTERCEPT_MAX_DISTANCE), INTERCEPT_MIN_DISTANCE)
        position = from_cp.position.point_from_heading(heading, distance)

        instance = self()
        instance.attackers_side = attacker
        instance.defenders_side = defender

        instance.position = position
        instance.size = SIZE_REGULAR
        instance.radials = ALL_RADIALS

        instance.air_attackers_location = instance.position.point_from_heading(random.randint(*INTERCEPT_ATTACKERS_HEADING) + heading, INTERCEPT_ATTACKERS_DISTANCE)
        instance.air_defenders_location = instance.position

        return instance

    @classmethod
    def ground_intercept_conflict(self, attacker: Country, defender: Country, position: Point, heading: int, radials: typing.List[int]):
        from theater.conflicttheater import SIZE_SMALL

        instance = self()
        instance.attackers_side = attacker
        instance.defenders_side = defender

        instance.position = position
        instance.size = SIZE_SMALL
        instance.radials = radials

        instance.air_attackers_location = instance.position.point_from_heading(random.randint(*INTERCEPT_ATTACKERS_HEADING) + heading, AIR_DISTANCE)
        instance.ground_defenders_location = instance.position

        return instance
