import typing
import pdb
import dcs

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

GROUND_DISTANCE_FACTOR = 1
AIR_DISTANCE_FACTOR = 4

class Conflict:
    def __init__(self, heading: int, attacker: Country, defender: Country, point: Point, size: int):
        self.attackers_side = attacker
        self.defenders_side = defender
        self.point = point
        self.size = size

        self.ground_attackers_location = self.point.point_from_heading(heading, self.size * GROUND_DISTANCE_FACTOR)
        self.ground_defenders_location = self.point.point_from_heading(_opposite_heading(heading), self.size * GROUND_DISTANCE_FACTOR)

        self.air_attackers_location = self.point.point_from_heading(heading, self.size * AIR_DISTANCE_FACTOR)
        self.air_defenders_location = self.point.point_from_heading(_opposite_heading(heading), self.size * AIR_DISTANCE_FACTOR)
