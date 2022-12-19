"""Maps generated units back to their Liberation types."""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Dict, Optional, Any, TYPE_CHECKING

from dcs.triggers import TriggerZone
from dcs.unit import Unit
from dcs.unitgroup import FlyingGroup, VehicleGroup, ShipGroup

from game.dcs.groundunittype import GroundUnitType
from game.squadrons import Pilot
from game.theater import Airfield, ControlPoint, TheaterUnit
from game.ato.flight import Flight
from game.theater.theatergroup import SceneryUnit

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


@dataclass(frozen=True)
class TheaterUnitMapping:
    dcs_group_id: int
    theater_unit: TheaterUnit
    dcs_unit: Unit


@dataclass(frozen=True)
class SceneryObjectMapping:
    ground_unit: TheaterUnit
    trigger_zone: TriggerZone


@dataclass(frozen=True)
class ConvoyUnit:
    unit_type: GroundUnitType
    convoy: Convoy


@dataclass(frozen=True)
class AirliftUnits:
    cargo: tuple[GroundUnitType, ...]
    transfer: TransferOrder


class UnitMap:
    def __init__(self) -> None:
        self.aircraft: Dict[str, FlyingUnit] = {}
        self.airfields: Dict[str, Airfield] = {}
        self.front_line_units: Dict[str, FrontLineUnit] = {}
        self.theater_objects: Dict[str, TheaterUnitMapping] = {}
        self.scenery_objects: Dict[str, SceneryObjectMapping] = {}
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

    def add_theater_unit_mapping(
        self, dcs_group_id: int, theater_unit: TheaterUnit, dcs_unit: Unit
    ) -> None:
        # Deaths for units at TGOs are recorded in the corresponding GroundUnit within
        # the GroundGroup, so we have to match the dcs unit with the liberation unit
        name = str(dcs_unit.name)
        if name in self.theater_objects:
            raise RuntimeError(f"Duplicate TGO unit: {name}")
        self.theater_objects[name] = TheaterUnitMapping(
            dcs_group_id, theater_unit, dcs_unit
        )

    def theater_units(self, name: str) -> Optional[TheaterUnitMapping]:
        return self.theater_objects.get(name, None)

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

    def add_scenery(self, scenery_unit: SceneryUnit, trigger_zone: TriggerZone) -> None:
        name = str(trigger_zone.name)
        if name in self.scenery_objects:
            raise RuntimeError(f"Duplicate scenery object {name} (TriggerZone)")
        self.scenery_objects[name] = SceneryObjectMapping(scenery_unit, trigger_zone)

    def scenery_object(self, name: str) -> Optional[SceneryObjectMapping]:
        return self.scenery_objects.get(name, None)
