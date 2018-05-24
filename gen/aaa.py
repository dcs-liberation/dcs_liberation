import typing
import pdb
import dcs

from random import randint

import globals

from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.vehicles import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.mapping import *
from dcs.point import *
from dcs.task import *

DISTANCE_FACTOR = 4, 5

class AAConflictGenerator:
    def __init__(self, mission: Mission, conflict: Conflict):
        self.m = mission
        self.conflict = conflict

    def generate(self, units: typing.Dict[UnitType, int]):
        for type, count in units.items():
            for _ in range(count):
                p = self.conflict.ground_defenders_location.random_point_within(
                        self.conflict.size * DISTANCE_FACTOR[1],
                        self.conflict.size * DISTANCE_FACTOR[0])

                self.m.vehicle_group(
                        country=self.conflict.defenders_side,
                        name=namegen.next_ground_group_name(),
                        _type=type,
                        position=p,
                        group_size=1)

