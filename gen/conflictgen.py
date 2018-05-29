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
AIR_DISTANCE = 8000

INTERCEPT_ATTACKERS_HEADING = -45, 45
INTERCEPT_DEFENDERS_HEADING = -10, 10
INTERCEPT_ATTACKERS_DISTANCE = 60000
INTERCEPT_DEFENDERS_DISTANCE = 30000

class Conflict:
    @classmethod
    def capture_conflict(self, attacker: Country, attack_heading: int, defender: Country, defense_heading: int, position: Point, size: int):
        instance = self()
        instance.attackers_side = attacker
        instance.defenders_side = defender
        instance.position = position
        instance.size = size

        instance.ground_attackers_location = instance.position.point_from_heading(attack_heading, instance.size * GROUND_DISTANCE_FACTOR)
        instance.ground_defenders_location = instance.position.point_from_heading(defense_heading, instance.size * GROUND_DISTANCE_FACTOR)

        instance.air_attackers_location = instance.position.point_from_heading(attack_heading, AIR_DISTANCE)
        instance.air_defenders_location = instance.position.point_from_heading(defense_heading, AIR_DISTANCE)

        return instance

    @classmethod
    def intercept_conflict(self, attacker: Country, defender: Country, position: Point, heading: int):
        from theater.conflicttheater import SIZE_REGULAR

        instance = self()
        instance.attackers_side = attacker
        instance.defenders_side = defender

        instance.position = position
        instance.size = SIZE_REGULAR

        instance.air_attackers_location = instance.position.point_from_heading(random.randint(*INTERCEPT_ATTACKERS_HEADING) + heading, INTERCEPT_ATTACKERS_DISTANCE)
        instance.air_defenders_location = instance.position.point_from_heading(random.randint(*INTERCEPT_DEFENDERS_HEADING) + heading, INTERCEPT_DEFENDERS_DISTANCE)

        return instance
