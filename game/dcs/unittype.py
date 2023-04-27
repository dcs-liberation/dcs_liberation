from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar, Generic, Iterator, Self, Type, TypeVar

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

    _loaded: ClassVar[bool] = False

    def __str__(self) -> str:
        return self.name

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
    def _each_variant_of(cls, unit: DcsUnitTypeT) -> Iterator[Self]:
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
