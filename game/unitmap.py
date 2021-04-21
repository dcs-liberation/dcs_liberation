"""Maps generated units back to their Liberation types."""
from dataclasses import dataclass
from typing import Dict, Optional, Type

from dcs.unit import Unit
from dcs.unitgroup import FlyingGroup, Group, VehicleGroup
from dcs.unittype import VehicleType

from game import db
from game.theater import Airfield, ControlPoint, TheaterGroundObject
from game.theater.theatergroundobject import BuildingGroundObject
from game.transfers import Convoy, RoadTransferOrder
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
class ConvoyUnit:
    unit_type: Type[VehicleType]
    convoy: Convoy


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
        self.convoys: Dict[str, ConvoyUnit] = {}

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
                    f"{name} is a {unit_type.__name__}, expected a VehicleType"
                )
            self.front_line_units[name] = FrontLineUnit(unit_type, origin)

    def front_line_unit(self, name: str) -> Optional[FrontLineUnit]:
        return self.front_line_units.get(name, None)

    def add_ground_object_units(
        self,
        ground_object: TheaterGroundObject,
        persistence_group: Group,
        miz_group: Group,
    ) -> None:
        """Adds a group associated with a TGO to the unit map.

        Args:
            ground_object: The TGO the group is associated with.
            persistence_group: The Group tracked by the TGO itself.
            miz_group: The Group spawned for the miz to match persistence_group.
        """
        # Deaths for units at TGOs are recorded in the Group that is contained
        # by the TGO, but when groundobjectsgen populates the miz it creates new
        # groups based on that template, so the units and groups in the miz are
        # not a direct match for the units and groups that persist in the TGO.
        #
        # This means that we need to map the spawned unit names back to the
        # original TGO units, not the ones in the miz.
        if len(persistence_group.units) != len(miz_group.units):
            raise ValueError("Persistent group does not match generated group")
        unit_pairs = zip(persistence_group.units, miz_group.units)
        for persistent_unit, miz_unit in unit_pairs:
            # The actual name is a String (the pydcs translatable string), which
            # doesn't define __eq__.
            name = str(miz_unit.name)
            if name in self.ground_object_units:
                raise RuntimeError(f"Duplicate TGO unit: {name}")
            self.ground_object_units[name] = GroundObjectUnit(
                ground_object, persistence_group, persistent_unit
            )

    def ground_object_unit(self, name: str) -> Optional[GroundObjectUnit]:
        return self.ground_object_units.get(name, None)

    def add_convoy_units(self, group: Group, convoy: Convoy) -> None:
        for unit in group.units:
            # The actual name is a String (the pydcs translatable string), which
            # doesn't define __eq__.
            name = str(unit.name)
            if name in self.convoys:
                raise RuntimeError(f"Duplicate convoy unit: {name}")
            unit_type = db.unit_type_from_name(unit.type)
            if unit_type is None:
                raise RuntimeError(f"Unknown unit type: {unit.type}")
            if not issubclass(unit_type, VehicleType):
                raise RuntimeError(
                    f"{name} is a {unit_type.__name__}, expected a VehicleType"
                )
            self.convoys[name] = ConvoyUnit(unit_type, convoy)

    def convoy_unit(self, name: str) -> Optional[ConvoyUnit]:
        return self.convoys.get(name, None)

    def add_building(self, ground_object: BuildingGroundObject, group: Group) -> None:
        # The actual name is a String (the pydcs translatable string), which
        # doesn't define __eq__.
        # The name of the initiator in the DCS dead event will have " object"
        # appended for statics.
        name = f"{group.name} object"
        if name in self.buildings:
            raise RuntimeError(f"Duplicate TGO unit: {name}")
        self.buildings[name] = Building(ground_object)

    def add_fortification(
        self, ground_object: BuildingGroundObject, group: VehicleGroup
    ) -> None:
        if len(group.units) != 1:
            raise ValueError("Fortification groups must have exactly one unit.")
        unit = group.units[0]
        # The actual name is a String (the pydcs translatable string), which
        # doesn't define __eq__.
        name = str(unit.name)
        if name in self.buildings:
            raise RuntimeError(f"Duplicate TGO unit: {name}")
        self.buildings[name] = Building(ground_object)

    def building_or_fortification(self, name: str) -> Optional[Building]:
        return self.buildings.get(name, None)
