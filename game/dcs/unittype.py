from __future__ import annotations

import logging
from abc import ABC
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import ClassVar, Generic, Iterator, Self, Type, TypeVar, Any

import yaml
from dcs.unittype import UnitType as DcsUnitType

from game.data.units import UnitClass

DcsUnitTypeT = TypeVar("DcsUnitTypeT", bound=Type[DcsUnitType])


@dataclass(frozen=True)
class UnitType(ABC, Generic[DcsUnitTypeT]):
    dcs_unit_type: DcsUnitTypeT
    variant_id: str
    display_name: str
    description: str
    year_introduced: str
    country_of_origin: str
    manufacturer: str
    role: str
    price: int
    unit_class: UnitClass
    hit_points: int

    _loaded: ClassVar[bool] = False

    def __str__(self) -> str:
        return self.display_name

    @property
    def dcs_id(self) -> str:
        return self.dcs_unit_type.id

    @classmethod
    def register(cls, unit_type: Self) -> None:
        raise NotImplementedError

    @classmethod
    def named(cls, name: str) -> Self:
        raise NotImplementedError

    @classmethod
    def for_dcs_type(cls, dcs_unit_type: DcsUnitTypeT) -> Iterator[Self]:
        raise NotImplementedError

    @staticmethod
    def each_dcs_type() -> Iterator[DcsUnitTypeT]:
        raise NotImplementedError

    @classmethod
    def _data_directory(cls) -> Path:
        raise NotImplementedError

    @classmethod
    def _each_variant_of(cls, unit: DcsUnitTypeT) -> Iterator[Self]:
        data_path = cls._data_directory() / f"{unit.id}.yaml"
        if not data_path.exists():
            logging.warning(f"No data for {unit.id}; it will not be available")
            return

        with data_path.open(encoding="utf-8") as data_file:
            data = yaml.safe_load(data_file)

        for variant_id, variant_data in data.get("variants", {unit.id: {}}).items():
            if variant_data is None:
                variant_data = {}
            yield cls._variant_from_dict(unit, variant_id, data | variant_data)

    @classmethod
    def _variant_from_dict(
        cls, dcs_unit_type: DcsUnitTypeT, variant_id: str, data: dict[str, Any]
    ) -> Self:
        raise NotImplementedError

    @classmethod
    def _load_all(cls) -> None:
        for unit_type in cls.each_dcs_type():
            for data in cls._each_variant_of(unit_type):
                cls.register(data)
        cls._loaded = True

    @cached_property
    def eplrs_capable(self) -> bool:
        return getattr(self.dcs_unit_type, "eplrs", False)

    @classmethod
    def exists(cls, name: str) -> bool:
        if not cls._loaded:
            cls._load_all()
        try:
            cls.named(name)
            return True
        except (KeyError, AssertionError):
            return False
