import itertools
import logging
from typing import Any

from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType
from game.dcs.unittype import UnitType

BASE_MAX_STRENGTH = 1.0
BASE_MIN_STRENGTH = 0.0


class Base:
    def __init__(self) -> None:
        self.aircraft: dict[AircraftType, int] = {}
        self.armor: dict[GroundUnitType, int] = {}
        self.strength = 1.0

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
            total += unit_type.price * count
        return total

    def total_units_of_type(self, unit_type: UnitType[Any]) -> int:
        return sum(
            [
                c
                for t, c in itertools.chain(self.aircraft.items(), self.armor.items())
                if t == unit_type
            ]
        )

    def commission_units(self, units: dict[Any, int]) -> None:
        for unit_type, unit_count in units.items():
            if unit_count <= 0:
                continue

            target_dict: dict[Any, int]
            if isinstance(unit_type, AircraftType):
                target_dict = self.aircraft
            elif isinstance(unit_type, GroundUnitType):
                target_dict = self.armor
            else:
                logging.error(f"Unexpected unit type of {unit_type}")
                return

            target_dict[unit_type] = target_dict.get(unit_type, 0) + unit_count

    def commit_losses(self, units_lost: dict[Any, int]) -> None:
        for unit_type, count in units_lost.items():
            target_dict: dict[Any, int]
            if unit_type in self.aircraft:
                target_dict = self.aircraft
            elif unit_type in self.armor:
                target_dict = self.armor
            else:
                print("Base didn't find event type {}".format(unit_type))
                continue

            if unit_type not in target_dict:
                print("Base didn't find event type {}".format(unit_type))
                continue

            target_dict[unit_type] = max(target_dict[unit_type] - count, 0)
            if target_dict[unit_type] == 0:
                del target_dict[unit_type]

    def affect_strength(self, amount: float) -> None:
        self.strength += amount
        if self.strength > BASE_MAX_STRENGTH:
            self.strength = BASE_MAX_STRENGTH
        elif self.strength <= 0:
            self.strength = BASE_MIN_STRENGTH

    def set_strength_to_minimum(self) -> None:
        self.strength = BASE_MIN_STRENGTH
