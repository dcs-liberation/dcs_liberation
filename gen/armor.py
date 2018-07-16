from itertools import zip_longest

from game import db
from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.unittype import *
from dcs.point import *
from dcs.task import *
from dcs.country import *

SPREAD_DISTANCE_FACTOR = 0.1, 0.3
SPREAD_DISTANCE_SIZE_FACTOR = 0.1


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

    def _generate_group(self, side: Country, unit: VehicleType, count: int, at: Point, to: Point = None):
        for c in range(count):
            group = self.m.vehicle_group(
                    side,
                    namegen.next_unit_name(side, unit),
                    unit,
                    position=self._group_point(at),
                    group_size=1,
                    move_formation=PointAction.OffRoad)

            if not to:
                to = self.conflict.position.point_from_heading(0, 500)

            wayp = group.add_waypoint(self._group_point(to))
            wayp.tasks = []

    def _generate_fight_at(self, attackers: db.ArmorDict, defenders: db.ArmorDict, position: Point):
        if attackers:
            for type, count in attackers.items():
                self._generate_group(
                    side=self.conflict.attackers_side,
                    unit=type,
                    count=count,
                    at=position.point_from_heading(self.conflict.heading - 90, 600),
                    to=position)

        if defenders:
            for type, count in defenders.items():
                self._generate_group(
                    side=self.conflict.defenders_side,
                    unit=type,
                    count=count,
                    at=position.point_from_heading(self.conflict.heading + 90, 600),
                    to=position)

    def generate(self, attackers: db.ArmorDict, defenders: db.ArmorDict):
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

    def generate_vec(self, attackers: db.ArmorDict, defenders: db.ArmorDict):
        defender_groups = list(db.unitdict_split(defenders, 6))
        distance_between_groups = min(self.conflict.distance / len(defender_groups), 12000)
        total_distance = distance_between_groups * len(defender_groups)

        attacker_groups = list(db.unitdict_split(attackers,
                                                 int(sum(attackers.values()) / len(defender_groups))))

        position = self.conflict.center.point_from_heading(self.conflict.opposite_heading, total_distance / 2)
        for attacker_group_dict, target_group_dict in zip_longest(attacker_groups, defender_groups):
            position = position.point_from_heading(self.conflict.heading, distance_between_groups)
            self._generate_fight_at(attacker_group_dict, target_group_dict, position)

    def generate_passengers(self, count: int):
        unit_type = random.choice(db.find_unittype(Nothing, self.conflict.attackers_side.name))

        self.m.vehicle_group(
            country=self.conflict.attackers_side,
            name=namegen.next_unit_name(self.conflict.attackers_side, unit_type),
            _type=unit_type,
            position=self.conflict.ground_attackers_location,
            group_size=count
        )
