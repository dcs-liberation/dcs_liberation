from dataclasses import dataclass
from typing import TypeVar, Generic, Type

from dcs.unittype import UnitType as DcsUnitType

DcsUnitTypeT = TypeVar("DcsUnitTypeT", bound=DcsUnitType)


@dataclass(frozen=True)
class UnitType(Generic[DcsUnitTypeT]):
    dcs_unit_type: Type[DcsUnitTypeT]
    name: str
    description: str
    year_introduced: str
    country_of_origin: str
    manufacturer: str
    role: str
    price: int

    def __str__(self) -> str:
        return self.name
