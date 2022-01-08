"""Maps generated units back to their Liberation types."""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Dict, Optional, Any, TYPE_CHECKING, Union, TypeVar, Generic

from dcs.unit import Vehicle, Ship
from dcs.unitgroup import FlyingGroup, VehicleGroup, StaticGroup, ShipGroup, MovingGroup

from game.dcs.groundunittype import GroundUnitType
from game.squadrons import Pilot
from game.theater import Airfield, ControlPoint, TheaterGroundObject
from game.theater.theatergroundobject import BuildingGroundObject, SceneryGroundObject
from game.ato.flight import Flight

if TYPE_CHECKING:
    from game.transfers import CargoShip, Convoy, TransferOrder


@dataclass(frozen=True)
class FlyingUnit:
    flight: Flight
    pilot: Optional[Pilot]


@dataclass(frozen=True)
class FrontLineUnit:
    unit_type: GroundUnitType
    origin: ControlPoint


UnitT = TypeVar("UnitT", Ship, Vehicle)


@dataclass(frozen=True)
class GroundObjectUnit(Generic[UnitT]):
    ground_object: TheaterGroundObject[Any]
    group: MovingGroup[UnitT]
    unit: UnitT


@dataclass(frozen=True)
class ConvoyUnit:
    unit_type: GroundUnitType
    convoy: Convoy


@dataclass(frozen=True)
class AirliftUnits:
    cargo: tuple[GroundUnitType, ...]
    transfer: TransferOrder


@dataclass(frozen=True)
class Building:
    ground_object: BuildingGroundObject


class UnitMap:
    def __init__(self) -> None:
        self.aircraft: Dict[str, FlyingUnit] = {}
        self.airfields: Dict[str, Airfield] = {}
        self.front_line_units: Dict[str, FrontLineUnit] = {}
        self.ground_object_units: Dict[str, GroundObjectUnit[Any]] = {}
        self.buildings: Dict[str, Building] = {}
        self.convoys: Dict[str, ConvoyUnit] = {}
        self.cargo_ships: Dict[str, CargoShip] = {}
        self.airlifts: Dict[str, AirliftUnits] = {}

    def add_aircraft(self, group: FlyingGroup[Any], flight: Flight) -> None:
        for pilot, unit in zip(flight.roster.pilots, group.units):
            # The actual name is a String (the pydcs translatable string), which
            # doesn't define __eq__.
            name = str(unit.name)
            if name in self.aircraft:
                raise RuntimeError(f"Duplicate unit name: {name}")
            self.aircraft[name] = FlyingUnit(flight, pilot)
        if flight.cargo is not None:
            self.add_airlift_units(group, flight.cargo)

    def flight(self, unit_name: str) -> Optional[FlyingUnit]:
        return self.aircraft.get(unit_name, None)

    def add_airfield(self, airfield: Airfield) -> None:
        if airfield.name in self.airfields:
            raise RuntimeError(f"Duplicate airfield: {airfield.name}")
        self.airfields[airfield.name] = airfield

    def airfield(self, name: str) -> Optional[Airfield]:
        return self.airfields.get(name, None)

    def add_front_line_units(
        self, group: VehicleGroup, origin: ControlPoint, unit_type: GroundUnitType
    ) -> None:
        for unit in group.units:
            # The actual name is a String (the pydcs translatable string), which
            # doesn't define __eq__.
            name = str(unit.name)
            if name in self.front_line_units:
                raise RuntimeError(f"Duplicate front line unit: {name}")
            self.front_line_units[name] = FrontLineUnit(unit_type, origin)

    def front_line_unit(self, name: str) -> Optional[FrontLineUnit]:
        return self.front_line_units.get(name, None)

    def add_ground_object_units(
        self,
        ground_object: TheaterGroundObject[Any],
        persistence_group: Union[ShipGroup, VehicleGroup],
        miz_group: Union[ShipGroup, VehicleGroup],
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

    def ground_object_unit(self, name: str) -> Optional[GroundObjectUnit[Any]]:
        return self.ground_object_units.get(name, None)

    def add_convoy_units(self, group: VehicleGroup, convoy: Convoy) -> None:
        for unit, unit_type in zip(group.units, convoy.iter_units()):
            # The actual name is a String (the pydcs translatable string), which
            # doesn't define __eq__.
            name = str(unit.name)
            if name in self.convoys:
                raise RuntimeError(f"Duplicate convoy unit: {name}")
            self.convoys[name] = ConvoyUnit(unit_type, convoy)

    def convoy_unit(self, name: str) -> Optional[ConvoyUnit]:
        return self.convoys.get(name, None)

    def add_cargo_ship(self, group: ShipGroup, ship: CargoShip) -> None:
        if len(group.units) > 1:
            # Cargo ship "groups" are single units. Killing the one ship kills the whole
            # transfer. If we ever want to add escorts or create multiple cargo ships in
            # a convoy of ships that logic needs to change.
            raise ValueError("Expected cargo ship to be a single unit group.")
        unit = group.units[0]
        # The actual name is a String (the pydcs translatable string), which
        # doesn't define __eq__.
        name = str(unit.name)
        if name in self.cargo_ships:
            raise RuntimeError(f"Duplicate cargo ship: {name}")
        self.cargo_ships[name] = ship

    def cargo_ship(self, name: str) -> Optional[CargoShip]:
        return self.cargo_ships.get(name, None)

    def add_airlift_units(
        self, group: FlyingGroup[Any], transfer: TransferOrder
    ) -> None:
        capacity_each = math.ceil(transfer.size / len(group.units))
        for idx, transport in enumerate(group.units):
            # Slice the units in groups based on the capacity of each unit. Cargo is
            # assigned arbitrarily to units in the order of the group. The last unit in
            # the group will receive a partial load if there is not enough cargo to fill
            # every transport.
            base_idx = idx * capacity_each
            cargo = tuple(
                itertools.islice(
                    transfer.iter_units(), base_idx, base_idx + capacity_each
                )
            )
            # The actual name is a String (the pydcs translatable string), which
            # doesn't define __eq__.
            name = str(transport.name)
            if name in self.airlifts:
                raise RuntimeError(f"Duplicate airlift unit: {name}")
            self.airlifts[name] = AirliftUnits(cargo, transfer)

    def airlift_unit(self, name: str) -> Optional[AirliftUnits]:
        return self.airlifts.get(name, None)

    def add_building(
        self, ground_object: BuildingGroundObject, group: StaticGroup
    ) -> None:
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

    def add_scenery(self, ground_object: SceneryGroundObject) -> None:
        assert ground_object.zone
        name = str(ground_object.zone.name)
        if name in self.buildings:
            raise RuntimeError(
                f"Duplicate TGO unit: {name}. TriggerZone name: "
                f"{ground_object.dcs_identifier}"
            )

        self.buildings[name] = Building(ground_object)

    def building_or_fortification(self, name: str) -> Optional[Building]:
        return self.buildings.get(name, None)
