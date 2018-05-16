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
from dcs.country import *

SPREAD_DISTANCE_FACTOR = 0.01, 0.1
SPREAD_DISTANCE_SIZE_FACTOR = 0.5

class ArmorConflictGenerator:
    def __init__(self, mission: Mission, conflict: Conflict):
        self.m = mission
        self.conflict = conflict

    def _group_point(self, point) -> Point:
        distance = randint(
                int(self.conflict.size * SPREAD_DISTANCE_FACTOR[0]),
                int(self.conflict.size * SPREAD_DISTANCE_FACTOR[1]),
                )

        return point.random_point_within(distance, self.conflict.size * SPREAD_DISTANCE_SIZE_FACTOR)

    def _generate_group(self, side: Country, unit: UnitType, count: int, at: Point):
        for c in range(count):
            group = self.m.vehicle_group(
                    side,
                    namegen.next_armor_group_name(),
                    unit,
                    position=self._group_point(at),
                    group_size=1,
                    move_formation=PointAction.OnRoad)
            wayp = group.add_waypoint(self.conflict.point)
            wayp.tasks = []

    def generate(self, attackers: typing.Dict[UnitType, int], defenders: typing.Dict[UnitType, int]):
        for type, count in attackers.items():
            self._generate_group(
                    side=self.conflict.attackers_side,
                    unit=type,
                    count=count,
                    at=self.conflict.ground_attackers_location)

        for type, count in defenders.items():
            self._generate_group(
                    side=self.conflict.defenders_side,
                    unit=type,
                    count=count,
                    at=self.conflict.ground_defenders_location)
