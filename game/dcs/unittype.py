from dataclasses import dataclass
from functools import cached_property
from typing import TypeVar, Generic, Type

from dcs.unittype import UnitType as DcsUnitType

DcsUnitTypeT = TypeVar("DcsUnitTypeT", bound=Type[DcsUnitType])


@dataclass(frozen=True)
class UnitType(Generic[DcsUnitTypeT]):
    dcs_unit_type: DcsUnitTypeT
    name: str
    description: str
    year_introduced: str
    country_of_origin: str
    manufacturer: str
    role: str
    price: int

    def __str__(self) -> str:
        return self.name

    @cached_property
    def eplrs_capable(self) -> bool:
        return getattr(self.dcs_unit_type, "eplrs", False)
