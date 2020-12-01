"""Maps generated units back to their Liberation types."""
from dataclasses import dataclass
from typing import Dict, Optional, Type

from dcs.unitgroup import FlyingGroup, Group
from dcs.unittype import UnitType

from game import db
from game.theater import Airfield, ControlPoint
from gen.flights.flight import Flight


@dataclass
class FrontLineUnit:
    unit_type: Type[UnitType]
    origin: ControlPoint


class UnitMap:
    def __init__(self) -> None:
        self.aircraft: Dict[str, Flight] = {}
        self.airfields: Dict[str, Airfield] = {}
        self.front_line_units: Dict[str, FrontLineUnit] = {}

    def add_aircraft(self, group: FlyingGroup, flight: Flight) -> None:
        for unit in group.units:
            # The actual name is a String (the pydcs translatable string), which
            # doesn't define __eq__.
            name = str(unit.name)
            if name in self.aircraft:
                raise RuntimeError(f"Duplicate unit name: {name}")
            self.aircraft[name] = flight

    def flight(self, unit_name: str) -> Optional[Flight]:
        return self.aircraft.get(unit_name, None)

    def add_airfield(self, airfield: Airfield) -> None:
        if airfield.name in self.airfields:
            raise RuntimeError(f"Duplicate airfield: {airfield.name}")
        self.airfields[airfield.name] = airfield

    def airfield(self, name: str) -> Optional[Airfield]:
        return self.airfields.get(name, None)

    def add_front_line_units(self, group: Group, origin: ControlPoint) -> None:
        for unit in group.units:
            # The actual name is a String (the pydcs translatable string), which
            # doesn't define __eq__.
            name = str(unit.name)
            if name in self.front_line_units:
                raise RuntimeError(f"Duplicate front line unit: {name}")
            unit_type = db.unit_type_from_name(unit.type)
            if unit_type is None:
                raise RuntimeError(f"Unknown unit type: {unit.type}")
            self.front_line_units[name] = FrontLineUnit(unit_type, origin)

    def front_line_unit(self, name: str) -> Optional[FrontLineUnit]:
        return self.front_line_units.get(name, None)
