import itertools
import logging
import math
import typing
from typing import Dict, Type

from dcs.task import CAP, CAS, Embarking, PinpointStrike, Task
from dcs.unittype import FlyingType, UnitType, VehicleType
from dcs.vehicles import AirDefence, Armor

from game import db
from gen.ground_forces.ai_ground_planner_db import TYPE_SHORAD

STRENGTH_AA_ASSEMBLE_MIN = 0.2
PLANES_SCRAMBLE_MIN_BASE = 2
PLANES_SCRAMBLE_MAX_BASE = 8
PLANES_SCRAMBLE_FACTOR = 0.3

BASE_MAX_STRENGTH = 1
BASE_MIN_STRENGTH = 0


class Base:

    def __init__(self):
        self.aircraft: Dict[Type[FlyingType], int] = {}
        self.armor: Dict[Type[VehicleType], int] = {}
        self.aa: Dict[AirDefence, int] = {}
        self.commision_points: Dict[Type, float] = {}
        self.strength = 1

    @property
    def total_aircraft(self) -> int:
        return sum(self.aircraft.values())

    @property
    def total_armor(self) -> int:
        return sum(self.armor.values())

    @property
    def total_frontline_aa(self) -> int:
        return sum([v for k, v in self.armor.items() if k in TYPE_SHORAD])

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

    def _find_best_unit(self, available_units: Dict[UnitType, int],
                        for_type: Task, count: int) -> Dict[UnitType, int]:
        if count <= 0:
            logging.warning("{}: no units for {}".format(self, for_type))
            return {}

        sorted_units = [key for key in available_units if
                        key in db.UNIT_BY_TASK[for_type]]
        sorted_units.sort(key=lambda x: db.PRICES[x], reverse=True)

        result: Dict[UnitType, int] = {}
        for unit_type in sorted_units:
            existing_count = available_units[unit_type]  # type: int
            if not existing_count:
                continue

            if count <= 0:
                break

            result_unit_count = min(count, existing_count)
            count -= result_unit_count

            assert result_unit_count > 0
            result[unit_type] = result.get(unit_type, 0) + result_unit_count

        logging.info("{} for {} ({}): {}".format(self, for_type, count, result))
        return result

    def _find_best_planes(self, for_type: Task, count: int) -> typing.Dict[FlyingType, int]:
        return self._find_best_unit(self.aircraft, for_type, count)

    def _find_best_armor(self, for_type: Task, count: int) -> typing.Dict[Armor, int]:
        return self._find_best_unit(self.armor, for_type, count)

    def append_commision_points(self, for_type, points: float) -> int:
        self.commision_points[for_type] = self.commision_points.get(for_type, 0) + points
        points = self.commision_points[for_type]
        if points >= 1:
            self.commision_points[for_type] = points - math.floor(points)
            return int(math.floor(points))

        return 0

    def filter_units(self, applicable_units: typing.Collection):
        self.aircraft = {k: v for k, v in self.aircraft.items() if k in applicable_units}
        self.armor = {k: v for k, v in self.armor.items() if k in applicable_units}

    def commision_units(self, units: typing.Dict[typing.Any, int]):
        for value in units.values():
            assert value > 0
            assert value == math.floor(value)

        for unit_type, unit_count in units.items():
            for_task = db.unit_task(unit_type)

            target_dict = None
            if for_task == CAS or for_task == CAP or for_task == Embarking:
                target_dict = self.aircraft
            elif for_task == PinpointStrike:
                target_dict = self.armor
            elif for_task == AirDefence:
                target_dict = self.aa

            if target_dict is not None:
                target_dict[unit_type] = target_dict.get(unit_type, 0) + unit_count
            else:
                logging.error("Unable to determine target dict for " + str(unit_type))

    def commit_losses(self, units_lost: typing.Dict[typing.Any, int]):

        for unit_type, count in units_lost.items():

            if unit_type in self.aircraft:
                target_array = self.aircraft
            elif unit_type in self.armor:
                target_array = self.armor
            else:
                print("Base didn't find event type {}".format(unit_type))
                continue

            if unit_type not in target_array:
                print("Base didn't find event type {}".format(unit_type))
                continue
                
            target_array[unit_type] = max(target_array[unit_type] - count, 0)
            if target_array[unit_type] == 0:
                del target_array[unit_type]

    def affect_strength(self, amount):
        self.strength += amount
        if self.strength > BASE_MAX_STRENGTH:
            self.strength = BASE_MAX_STRENGTH
        elif self.strength <= 0:
            self.strength = BASE_MIN_STRENGTH

    def set_strength_to_minimum(self) -> None:
        self.strength = BASE_MIN_STRENGTH

    def scramble_count(self, multiplier: float, task: Task = None) -> int:
        if task:
            count = sum([v for k, v in self.aircraft.items() if db.unit_task(k) == task])
        else:
            count = self.total_aircraft

        count = int(math.ceil(count * PLANES_SCRAMBLE_FACTOR * self.strength))
        return min(min(max(count, PLANES_SCRAMBLE_MIN_BASE), int(PLANES_SCRAMBLE_MAX_BASE * multiplier)), count)

    def assemble_count(self):
        return int(self.total_armor * 0.5)

    def assemble_aa_count(self) -> int:
        # previous logic removed because we always want the full air defense capabilities.
        return self.total_aa

    def scramble_sweep(self, multiplier: float) -> typing.Dict[FlyingType, int]:
        return self._find_best_planes(CAP, self.scramble_count(multiplier, CAP))

    def scramble_last_defense(self):
        # return as many CAP-capable aircraft as we can since this is the last defense of the base
        # (but not more than 20 - that's just nuts)
        return self._find_best_planes(CAP, min(self.total_aircraft, 20))

    def scramble_cas(self, multiplier: float) -> typing.Dict[FlyingType, int]:
        return self._find_best_planes(CAS, self.scramble_count(multiplier, CAS))

    def scramble_interceptors(self, multiplier: float) -> typing.Dict[FlyingType, int]:
        return self._find_best_planes(CAP, self.scramble_count(multiplier, CAP))

    def assemble_attack(self) -> typing.Dict[Armor, int]:
        return self._find_best_armor(PinpointStrike, self.assemble_count())

    def assemble_defense(self) -> typing.Dict[Armor, int]:
        count = int(self.total_armor * min(self.strength + 0.5, 1))
        return self._find_best_armor(PinpointStrike, count)

    def assemble_aa(self, count=None) -> typing.Dict[AirDefence, int]:
        return self._find_best_unit(self.aa, AirDefence, count and min(count, self.total_aa) or self.assemble_aa_count())
