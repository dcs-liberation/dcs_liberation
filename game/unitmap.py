"""Maps generated units back to their Liberation types."""
from dataclasses import dataclass
from typing import Dict, Optional, Type

from dcs.unit import Unit
from dcs.unitgroup import FlyingGroup, Group, StaticGroup
from dcs.unittype import VehicleType

from game import db
from game.theater import Airfield, ControlPoint, TheaterGroundObject
from game.theater.theatergroundobject import BuildingGroundObject
from gen.flights.flight import Flight


@dataclass(frozen=True)
class FrontLineUnit:
    unit_type: Type[VehicleType]
    origin: ControlPoint


@dataclass(frozen=True)
class GroundObjectUnit:
    ground_object: TheaterGroundObject
    group: Group
    unit: Unit


@dataclass(frozen=True)
class Building:
    ground_object: BuildingGroundObject


class UnitMap:
    def __init__(self) -> None:
        self.aircraft: Dict[str, Flight] = {}
        self.airfields: Dict[str, Airfield] = {}
        self.front_line_units: Dict[str, FrontLineUnit] = {}
        self.ground_object_units: Dict[str, GroundObjectUnit] = {}
        self.buildings: Dict[str, Building] = {}

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
            if not issubclass(unit_type, VehicleType):
                raise RuntimeError(
                    f"{name} is a {unit_type.__name__}, expected a VehicleType")
            self.front_line_units[name] = FrontLineUnit(unit_type, origin)

    def front_line_unit(self, name: str) -> Optional[FrontLineUnit]:
        return self.front_line_units.get(name, None)

    def add_ground_object_units(self, ground_object: TheaterGroundObject,
                                group: Group) -> None:
        for unit in group.units:
            # The actual name is a String (the pydcs translatable string), which
            # doesn't define __eq__.
            name = str(unit.name)
            if name in self.ground_object_units:
                raise RuntimeError(f"Duplicate TGO unit: {name}")
            self.ground_object_units[name] = GroundObjectUnit(ground_object,
                                                              group, unit)

    def ground_object_unit(self, name: str) -> Optional[GroundObjectUnit]:
        return self.ground_object_units.get(name, None)

    def add_building(self, ground_object: BuildingGroundObject,
                     building: StaticGroup) -> None:
        # The actual name is a String (the pydcs translatable string), which
        # doesn't define __eq__.
        name = str(building.name)
        if name in self.buildings:
            raise RuntimeError(f"Duplicate TGO unit: {name}")
        self.buildings[name] = Building(ground_object)

    def building(self, name: str) -> Optional[Building]:
        return self.buildings.get(name, None)
