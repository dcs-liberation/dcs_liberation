import typing
import dcs
import math

from shop import db
from theater.controlpoint import ControlPoint

from dcs.planes import *
from dcs.vehicles import *
from dcs.task import *

PLANES_IN_GROUP = 2
PLANES_IMPORTANCE_FACTOR = 2
ARMOR_IMPORTANCE_FACTOR = 4


class Base:
    aircraft = {}  # type: typing.Dict[PlaneType, int]
    armor = {}  # type: typing.Dict[Armor, int]
    aa = {} # type: typing.Dict[AirDefence, int]

    def __init__(self):
        pass

    @property
    def total_planes(self) -> int:
        return sum(self.aircraft.values())

    @property
    def total_armor(self) -> int:
        return sum(self.armor.values())

    def _find_best_unit(self, dict, for_type: Task, count: int) -> typing.Dict:
        sorted_planes = [key for key in dict.keys() if key in db.UNIT_BY_TASK[for_type]]
        sorted_planes.sort(key=lambda x: db.PRICES[x], reverse=True)

        result = {}
        for plane in sorted_planes:
            existing_count = dict[plane] # type: int
            if not existing_count:
                continue

            result_unit_count = min(count, existing_count)
            count -= result_unit_count
            result[plane] = result.get(plane, 0) + result_unit_count

        return result

    def _find_best_planes(self, for_type: Task, count: int) -> typing.Dict[PlaneType, int]:
        return self._find_best_unit(self.aircraft, for_type, count)

    def _find_best_armor(self, for_type: Task, count: int) -> typing.Dict[PlaneType, int]:
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

    def commit_scramble(self, scrambled_aircraft: typing.Dict[PlaneType, int]):
        for k, c in scrambled_aircraft:
            self.aircraft[k] -= c
            assert self.aircraft[k] >= 0
            if self.aircraft[k] == 0:
                del self.aircraft[k]

    def scramble_cas(self, for_target: ControlPoint) -> typing.Dict[PlaneType, int]:
        return self._find_best_planes(CAS, int(for_target.importance * PLANES_IMPORTANCE_FACTOR))

    def scramble_sweep(self, for_target: ControlPoint) -> typing.Dict[PlaneType, int]:
        return self._find_best_planes(FighterSweep, int(for_target.importance * PLANES_IMPORTANCE_FACTOR))

    def scramble_interceptors(self, factor: float) -> typing.Dict[PlaneType, int]:
        return self._find_best_planes(FighterSweep, int(self.total_planes * factor))

    def assemble_cap(self, for_target: ControlPoint) -> typing.Dict[Armor, int]:
        return self._find_best_armor(CAP, int(for_target.importance * ARMOR_IMPORTANCE_FACTOR))

    def assemble_defense(self, factor: float) -> typing.Dict[Armor, int]:
        return self._find_best_armor(CAP, int(self.total_armor * factor))
