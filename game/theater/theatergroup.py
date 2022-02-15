from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, Any, TYPE_CHECKING, Type

from dcs.triggers import TriggerZone
from dcs.unittype import VehicleType, ShipType, StaticType

from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.dcs.unittype import UnitType
from dcs.unittype import UnitType as DcsUnitType

from game.point_with_heading import PointWithHeading
from game.utils import Heading

if TYPE_CHECKING:
    from game.layout.layout import LayoutUnit, TgoLayoutGroup
    from game.theater import TheaterGroundObject


@dataclass
class TheaterUnit:
    """Representation of a single Unit in the Game"""

    # Every Unit has a unique ID generated from the game
    id: int
    # The name of the Unit. Not required to be unique
    name: str
    # DCS UniType of the unit
    type: Type[DcsUnitType]
    # Position and orientation of the Unit
    position: PointWithHeading
    # The parent ground object
    ground_object: TheaterGroundObject
    # State of the unit, dead or alive
    alive: bool = True

    @staticmethod
    def from_template(
        id: int, dcs_type: Type[DcsUnitType], t: LayoutUnit, go: TheaterGroundObject
    ) -> TheaterUnit:
        return TheaterUnit(
            id,
            t.name,
            dcs_type,
            PointWithHeading.from_point(t.position, Heading.from_degrees(t.heading)),
            go,
        )

    @property
    def unit_type(self) -> Optional[UnitType[Any]]:
        if issubclass(self.type, VehicleType):
            return next(GroundUnitType.for_dcs_type(self.type))
        elif issubclass(self.type, ShipType):
            return next(ShipUnitType.for_dcs_type(self.type))
        # None for not available StaticTypes
        return None

    def kill(self) -> None:
        self.alive = False

    @property
    def unit_name(self) -> str:
        return f"{str(self.id).zfill(4)} | {self.name}"

    @property
    def display_name(self) -> str:
        dead_label = " [DEAD]" if not self.alive else ""
        unit_label = self.unit_type or self.type.name or self.name
        return f"{str(self.id).zfill(4)} | {unit_label}{dead_label}"

    @property
    def short_name(self) -> str:
        dead_label = " [DEAD]" if not self.alive else ""
        return f"<b>{self.type.id[0:18]}</b> {dead_label}"

    @property
    def is_static(self) -> bool:
        return issubclass(self.type, StaticType)

    @property
    def is_vehicle(self) -> bool:
        return issubclass(self.type, VehicleType)

    @property
    def is_ship(self) -> bool:
        return issubclass(self.type, ShipType)

    @property
    def icon(self) -> str:
        return self.type.id

    @property
    def repairable(self) -> bool:
        # Only let units with UnitType be repairable as we just have prices for them
        return self.unit_type is not None


class SceneryUnit(TheaterUnit):
    """Special TheaterUnit for handling scenery ground objects"""

    # Scenery Objects are identified by a special trigger zone
    zone: TriggerZone

    @property
    def display_name(self) -> str:
        dead_label = " [DEAD]" if not self.alive else ""
        return f"{str(self.id).zfill(4)} | {self.name}{dead_label}"

    @property
    def short_name(self) -> str:
        dead_label = " [DEAD]" if not self.alive else ""
        return f"<b>{self.name[0:18]}</b> {dead_label}"

    @property
    def icon(self) -> str:
        return "missing"

    @property
    def repairable(self) -> bool:
        return False


@dataclass
class TheaterGroup:
    """Logical group for multiple TheaterUnits at a specific position"""

    # Every Theater Group has a unique ID generated from the game
    id: int  # Unique ID
    # The name of the Group. Not required to be unique
    name: str
    # Position and orientation of the Group
    position: PointWithHeading
    # All TheaterUnits within the group
    units: list[TheaterUnit]
    # The parent ground object
    ground_object: TheaterGroundObject

    @staticmethod
    def from_template(
        id: int,
        name: str,
        units: list[TheaterUnit],
        go: TheaterGroundObject,
        unit_type: Type[DcsUnitType],
        unit_count: int,
    ) -> TheaterGroup:
        return TheaterGroup(
            id,
            name,
            PointWithHeading.from_point(go.position, go.heading),
            units,
            go,
        )

    @property
    def group_name(self) -> str:
        return f"{str(self.id).zfill(4)} | {self.name}"

    @property
    def unit_count(self) -> int:
        return len(self.units)

    @property
    def alive_units(self) -> int:
        return sum([unit.alive for unit in self.units])
