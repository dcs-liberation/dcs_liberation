import itertools
import logging
import math
import typing
from typing import Dict, Type

from dcs.task import AWACS, CAP, CAS, Embarking, PinpointStrike, Task, Transport
from dcs.unittype import FlyingType, UnitType, VehicleType
from dcs.vehicles import AirDefence, Armor

from game import db
from game.db import PRICES

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
        # TODO: Appears unused.
        self.aa: Dict[AirDefence, int] = {}
        self.strength = 1

    @property
    def total_aircraft(self) -> int:
        return sum(self.aircraft.values())

    @property
    def total_armor(self) -> int:
        return sum(self.armor.values())

    @property
    def total_armor_value(self) -> int:
        total = 0
        for unit_type, count in self.armor.items():
            try:
                total += PRICES[unit_type] * count
            except KeyError:
                logging.exception(f"No price found for {unit_type.id}")
        return total

    @property
    def total_aa(self) -> int:
        return sum(self.aa.values())

    def total_units(self, task: Task) -> int:
        return sum(
            [
                c
                for t, c in itertools.chain(
                    self.aircraft.items(), self.armor.items(), self.aa.items()
                )
                if t in db.UNIT_BY_TASK[task]
            ]
        )

    def total_units_of_type(self, unit_type) -> int:
        return sum(
            [
                c
                for t, c in itertools.chain(
                    self.aircraft.items(), self.armor.items(), self.aa.items()
                )
                if t == unit_type
            ]
        )

    @property
    def all_units(self):
        return itertools.chain(
            self.aircraft.items(), self.armor.items(), self.aa.items()
        )

    def commision_units(self, units: typing.Dict[typing.Any, int]):

        for unit_type, unit_count in units.items():
            if unit_count <= 0:
                continue

            for_task = db.unit_task(unit_type)

            target_dict = None
            if (
                for_task == AWACS
                or for_task == CAS
                or for_task == CAP
                or for_task == Embarking
                or for_task == Transport
            ):
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
