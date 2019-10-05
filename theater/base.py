import logging
import typing
import math
import itertools

from dcs.planes import *
from dcs.vehicles import *
from dcs.task import *

from game import db
from gen import aaa

STRENGTH_AA_ASSEMBLE_MIN = 0.2
PLANES_SCRAMBLE_MIN_BASE = 2
PLANES_SCRAMBLE_MAX_BASE = 8
PLANES_SCRAMBLE_FACTOR = 0.3

BASE_MAX_STRENGTH = 1
BASE_MIN_STRENGTH = 0


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
            logging.warning("{}: no units for {}".format(self, for_type))
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

        logging.info("{} for {} ({}): {}".format(self, for_type, count, result))
        return result

    def _find_best_planes(self, for_type: Task, count: int) -> typing.Dict[PlaneType, int]:
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

            assert target_dict is not None
            target_dict[unit_type] = target_dict.get(unit_type, 0) + unit_count

    def commit_losses(self, units_lost: typing.Dict[typing.Any, int]):
        # advanced SAM sites have multiple units - this code was not at all set up to handle that
        #   to avoid having to restructure a bunch of upstream code, we track total destroyed units and
        #   use that to determine if a site was destroyed
        # this can be thought of as the enemy re-distributing parts of SAM sites to keep as many
        #  operational as possible (pulling specific units from ...storage... to bring them back online
        #  if non-letal damage was done)
        # in the future, I may add more depth to this (e.g. a base having a certain number of spares and tracking
        #  the number of pieces of each site), but for now this is what we get
        sams_destroyed = {}
        # we count complex SAM sites at the end - don't double count
        aa_skip = [
            AirDefence.SAM_SA_6_Kub_LN_2P25,
            AirDefence.SAM_SA_3_S_125_LN_5P73,
            AirDefence.SAM_SA_11_Buk_LN_9A310M1
        ]
        for unit_type, count in units_lost.items():
            if unit_type in db.SAM_CONVERT or unit_type in db.SAM_CONVERT['except']:
                # unit is part of an advanced SAM site, which means it will fail the below check
                try:
                    sams_destroyed[unit_type] += 1
                except KeyError:
                    sams_destroyed[unit_type] = 1
            if unit_type in self.aircraft:
                target_array = self.aircraft
            elif unit_type in self.armor:
                target_array = self.armor
            elif unit_type in self.aa and unit_type not in aa_skip:
                target_array = self.aa
            else:
                print("Base didn't find event type {}".format(unit_type))
                continue

            if unit_type not in target_array:
                print("Base didn't find event type {}".format(unit_type))
                continue
                
            target_array[unit_type] = max(target_array[unit_type] - count, 0)
            if target_array[unit_type] == 0:
                del target_array[unit_type]

        # now that we have a complete picture of the SAM sites destroyed, determine if any were destroyed
        for sam_site, count in sams_destroyed.items():
            dead_count = aaa.num_sam_dead(sam_site, count)
            try:
                modified_sam_site = db.SAM_CONVERT[sam_site]
            except KeyError:
                modified_sam_site = db.SAM_CONVERT[sam_site]['except']

            if modified_sam_site in self.aa:
                self.aa[modified_sam_site] = max(
                    self.aa[modified_sam_site] - dead_count,
                    0
                )
                if self.aa[modified_sam_site] == 0:
                    del self.aa[modified_sam_site]

    def affect_strength(self, amount):
        self.strength += amount
        if self.strength > BASE_MAX_STRENGTH:
            self.strength = BASE_MAX_STRENGTH
        elif self.strength <= 0:
            self.strength = BASE_MIN_STRENGTH

    def scramble_count(self, multiplier: float, task: Task = None) -> int:
        if task:
            count = sum([v for k, v in self.aircraft.items() if db.unit_task(k) == task])
        else:
            count = self.total_planes

        count = int(math.ceil(count * PLANES_SCRAMBLE_FACTOR * self.strength))
        return min(min(max(count, PLANES_SCRAMBLE_MIN_BASE), int(PLANES_SCRAMBLE_MAX_BASE * multiplier)), count)

    def assemble_count(self):
        return int(self.total_armor * 0.5)

    def assemble_aa_count(self) -> int:
        # previous logic removed because we always want the full air defense capabilities.
        return self.total_aa

    def scramble_sweep(self, multiplier: float) -> typing.Dict[PlaneType, int]:
        return self._find_best_planes(CAP, self.scramble_count(multiplier, CAP))

    def scramble_last_defense(self):
        # return as many CAP-capable aircraft as we can since this is the last defense of the base
        # (but not more than 20 - that's just nuts)
        return self._find_best_planes(CAP, min(self.total_planes, 20))

    def scramble_cas(self, multiplier: float) -> typing.Dict[PlaneType, int]:
        return self._find_best_planes(CAS, self.scramble_count(multiplier, CAS))

    def scramble_interceptors(self, multiplier: float) -> typing.Dict[PlaneType, int]:
        return self._find_best_planes(CAP, self.scramble_count(multiplier, CAP))

    def assemble_attack(self) -> typing.Dict[Armor, int]:
        return self._find_best_armor(PinpointStrike, self.assemble_count())

    def assemble_defense(self) -> typing.Dict[Armor, int]:
        count = int(self.total_armor * min(self.strength + 0.5, 1))
        return self._find_best_armor(PinpointStrike, count)

    def assemble_aa(self, count=None) -> typing.Dict[AirDefence, int]:
        return self._find_best_unit(self.aa, AirDefence, count and min(count, self.total_aa) or self.assemble_aa_count())
