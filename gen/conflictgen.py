import typing
import pdb
import dcs

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
AIR_DISTANCE_FACTOR = 5

class Conflict:
    trigger_zone = None # type: TriggerZone
    activation_trigger = None # type: Trigger

    def __init__(self, attacker: Country, attack_heading: int, defender: Country, defense_heading: int, point: Point, size: int):
        self.attackers_side = attacker
        self.defenders_side = defender
        self.point = point
        self.size = size

        self.ground_attackers_location = self.point.point_from_heading(attack_heading, self.size * GROUND_DISTANCE_FACTOR)
        self.ground_defenders_location = self.point.point_from_heading(defense_heading, self.size * GROUND_DISTANCE_FACTOR)

        self.air_attackers_location = self.point.point_from_heading(attack_heading, self.size * AIR_DISTANCE_FACTOR)
        self.air_defenders_location = self.point.point_from_heading(defense_heading, self.size * AIR_DISTANCE_FACTOR)

