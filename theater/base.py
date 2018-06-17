import typing
import math
import itertools

from game import db
from theater.controlpoint import ControlPoint

from dcs.planes import *
from dcs.vehicles import *
from dcs.task import *

PLANES_IN_GROUP = 2

PLANES_SCRAMBLE_MIN = 4
PLANES_SCRAMBLE_FACTOR = 0.5


class Base:
    aircraft = {}  # type: typing.Dict[PlaneType, int]
    armor = {}  # type: typing.Dict[Armor, int]
    aa = {}  # type: typing.Dict[AirDefence, int]
    strength = 1  # type: float
    commision_points = {}

    def __init__(self):
        self.aircraft = {}
        self.armor = {}
        self.aa = {}
        self.commision_points = {}
        self.strength = 1

    @property
    def total_planes(self) -> int:
        return sum(self.aircraft.values())

    @property
    def total_armor(self) -> int:
        return sum(self.armor.values())

    @property
    def total_aa(self) -> int:
        return sum(self.aa.values())

    def total_units(self, task: Task) -> int:
        return sum([c for t, c in itertools.chain(self.aircraft.items(), self.armor.items(), self.aa.items()) if t in db.UNIT_BY_TASK[task]])

    def total_units_of_type(self, unit_type) -> int:
        return sum([c for t, c in itertools.chain(self.aircraft.items(), self.armor.items(), self.aa.items()) if t == unit_type])

    @property
    def all_units(self):
        return itertools.chain(self.aircraft.items(), self.armor.items(), self.aa.items())

    def _find_best_unit(self, dict, for_type: Task, count: int) -> typing.Dict:
        if count <= 0:
            return {}

        sorted_units = [key for key in dict.keys() if key in db.UNIT_BY_TASK[for_type]]
        sorted_units.sort(key=lambda x: db.PRICES[x], reverse=True)

        result = {}
        for unit_type in sorted_units:
            existing_count = dict[unit_type]  # type: int
            if not existing_count:
                continue

            if count <= 0:
                break

            result_unit_count = min(count, existing_count)
            count -= result_unit_count

            assert result_unit_count > 0
            result[unit_type] = result.get(unit_type, 0) + result_unit_count

        return result

    def _find_best_planes(self, for_type: Task, count: int) -> typing.Dict[PlaneType, int]:
        return self._find_best_unit(self.aircraft, for_type, count)

    def _find_best_armor(self, for_type: Task, count: int) -> typing.Dict[Armor, int]:
        return self._find_best_unit(self.armor, for_type, count)

    def _group_sizes(self, total_planes: int) -> typing.List[int]:
        total_scrambled = 0
        for _ in range(math.ceil(total_planes / PLANES_IN_GROUP)):
            total_scrambled += PLANES_IN_GROUP
            yield total_scrambled < total_planes and PLANES_IN_GROUP or total_planes - total_scrambled

    def _group_sizes_for(self, target: ControlPoint) -> typing.List[int]:
        total_planes = target.importance * PLANES_IMPORTANCE_FACTOR
        total_scrambled = 0
        for _ in range(math.ceil(total_planes / PLANES_IN_GROUP)):
            total_scrambled += PLANES_IN_GROUP
            yield PLANES_IN_GROUP and total_scrambled < total_planes or total_planes - total_scrambled

    def append_commision_points(self, for_type, points: float) -> int:
        self.commision_points[for_type] = self.commision_points.get(for_type, 0) + points
        points = self.commision_points[for_type]
        if points >= 1:
            self.commision_points[for_type] = points - math.floor(points)
            return int(math.floor(points))

        return 0

    def filter_units(self, applicable_units: typing.Collection):
        self.aircraft = {k: v for k, v in self.aircraft.items() if k in applicable_units}
        self.armor = {k: v for k, v in self.aircraft.items() if k in applicable_units}

    def commision_units(self, units: typing.Dict[typing.Any, int]):
        for value in units.values():
            assert value > 0
            assert value == math.floor(value)

        for unit_type, unit_count in units.items():
            for_task = db.unit_task(unit_type)

            target_dict = None
            if for_task == CAS or for_task == FighterSweep:
                target_dict = self.aircraft
            elif for_task == CAP:
                target_dict = self.armor
            elif for_task == AirDefence:
                target_dict = self.aa

            assert target_dict is not None
            target_dict[unit_type] = target_dict.get(unit_type, 0) + unit_count

    def commit_losses(self, units_lost: typing.Dict[typing.Any, int]):
        for unit_type, count in units_lost.items():
            if unit_type in self.aircraft:
                target_array = self.aircraft
            elif unit_type in self.armor:
                target_array = self.armor
            elif unit_type in self.aa:
                target_array = self.aa
            else:
                continue

            if unit_type not in target_array:
                continue
                
            target_array[unit_type] = max(target_array[unit_type] - count, 0)
            if target_array[unit_type] == 0:
                del target_array[unit_type]

    def affect_strength(self, amount):
        self.strength += amount
        if self.strength > 1:
            self.strength = 1

    def scramble_count(self) -> int:
        count = int(self.total_planes * PLANES_SCRAMBLE_FACTOR * self.strength)
        return min(max(count, PLANES_SCRAMBLE_MIN), self.total_planes)

    def assemble_count(self):
        return self.total_armor * self.strength

    def assemble_aa_count(self) -> int:
        return int(self.total_aa * (self.strength > 0.2 and self.strength or 0))

    def scramble_sweep(self) -> typing.Dict[PlaneType, int]:
        return self._find_best_planes(FighterSweep, self.scramble_count())

    def scramble_cas(self) -> typing.Dict[PlaneType, int]:
        return self._find_best_planes(CAS, self.scramble_count())

    def scramble_interceptors(self) -> typing.Dict[PlaneType, int]:
        return self._find_best_planes(FighterSweep, self.scramble_count())

    def assemble_cap(self) -> typing.Dict[Armor, int]:
        return self._find_best_armor(CAP, self.assemble_count())

    def assemble_defense(self) -> typing.Dict[Armor, int]:
        return self._find_best_armor(CAP, self.assemble_count())

    def assemble_aa(self) -> typing.Dict[AirDefence, int]:
        return self._find_best_unit(self.aa, AirDefence, self.assemble_aa_count())
