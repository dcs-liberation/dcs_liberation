from __future__ import annotations

from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import Any, ClassVar, Generic, Iterator, Type, TypeVar

from dcs.unittype import UnitType as DcsUnitType

from game.data.units import UnitClass

DcsUnitTypeT = TypeVar("DcsUnitTypeT", bound=Type[DcsUnitType])


@dataclass(frozen=True)
class UnitType(ABC, Generic[DcsUnitTypeT]):
    dcs_unit_type: DcsUnitTypeT
    name: str
    description: str
    year_introduced: str
    country_of_origin: str
    manufacturer: str
    role: str
    price: int
    unit_class: UnitClass

    _by_name: ClassVar[dict[str, UnitType[Any]]] = {}
    _by_unit_type: ClassVar[dict[Type[DcsUnitType], list[UnitType[Any]]]] = defaultdict(
        list
    )
    _loaded: ClassVar[bool] = False

    def __str__(self) -> str:
        return self.name

    @property
    def dcs_id(self) -> str:
        return self.dcs_unit_type.id

    @classmethod
    def register(cls, unit_type: UnitType[Any]) -> None:
        cls._by_name[unit_type.name] = unit_type
        cls._by_unit_type[unit_type.dcs_unit_type].append(unit_type)

    @classmethod
    def named(cls, name: str) -> UnitType[Any]:
        raise NotImplementedError

    @classmethod
    def for_dcs_type(cls, dcs_unit_type: DcsUnitTypeT) -> Iterator[UnitType[Any]]:
        raise NotImplementedError

    @staticmethod
    def each_dcs_type() -> Iterator[DcsUnitTypeT]:
        raise NotImplementedError

    @classmethod
    def _each_variant_of(cls, unit: DcsUnitTypeT) -> Iterator[UnitType[Any]]:
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
