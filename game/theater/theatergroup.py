from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, TYPE_CHECKING, Type

from dcs.triggers import TriggerZone
from dcs.unittype import ShipType, StaticType, UnitType as DcsUnitType, VehicleType

from game.data.radar_db import LAUNCHER_TRACKER_PAIRS, TELARS, TRACK_RADARS
from game.data.units import ANTI_AIR_UNIT_CLASSES
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.dcs.unittype import UnitType
from game.point_with_heading import PointWithHeading
from game.theater.iadsnetwork.iadsrole import IadsRole
from game.utils import Heading, Distance, meters

if TYPE_CHECKING:
    from game.layout.layout import LayoutUnit
    from game.sim import GameUpdateEvents
    from game.theater.theatergroundobject import TheaterGroundObject


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

    def kill(self, events: GameUpdateEvents) -> None:
        self.alive = False
        self.ground_object.invalidate_threat_poly()
        events.update_tgo(self.ground_object)

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
    def is_anti_air(self) -> bool:
        return (
            self.unit_type is not None
            and self.unit_type.unit_class in ANTI_AIR_UNIT_CLASSES
        )

    @property
    def icon(self) -> str:
        return self.type.id

    @property
    def repairable(self) -> bool:
        # Only let units with UnitType be repairable as we just have prices for them
        return self.unit_type is not None

    @property
    def detection_range(self) -> Distance:
        unit_range = getattr(self.type, "detection_range", None)
        return meters(unit_range if unit_range is not None and self.alive else 0)

    @property
    def threat_range(self) -> Distance:
        unit_range = getattr(self.type, "threat_range", None)
        return meters(unit_range if unit_range is not None and self.alive else 0)


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
        return sum(unit.alive for unit in self.units)

    @property
    def has_statics(self) -> bool:
        return any(unit.is_static for unit in self.units)

    def max_detection_range(self) -> Distance:
        """Calculate the maximum detection range of the TheaterGroup"""
        ranges = (u.detection_range for u in self.units if u.is_anti_air)
        return max(ranges, default=meters(0))

    def max_threat_range(self, radar_only: bool = False) -> Distance:
        """Calculate the maximum threat range of the TheaterGroup.
        This also checks for Launcher and Tracker Pairs and if they are functioning or not. Allows to also use only radar emitting units for the calculation with the parameter."""
        max_non_radar = meters(0)
        max_telar_range = meters(0)
        max_tel_range = meters(0)
        live_trs = set()
        launchers: dict[Type[VehicleType], Distance] = {}
        for unit in self.units:
            if not unit.alive or not unit.is_anti_air:
                continue
            if unit.type in TRACK_RADARS:
                live_trs.add(unit.type)
            elif unit.type in TELARS:
                max_telar_range = max(max_telar_range, unit.threat_range)
            elif (
                issubclass(unit.type, VehicleType)
                and unit.type in LAUNCHER_TRACKER_PAIRS
            ):
                launchers[unit.type] = unit.threat_range
            else:
                max_non_radar = max(max_non_radar, unit.threat_range)
        for launcher, threat_range in launchers.items():
            if LAUNCHER_TRACKER_PAIRS[launcher] in live_trs:
                max_tel_range = max(max_tel_range, threat_range)
        if radar_only:
            return max(max_tel_range, max_telar_range)
        return max(max_tel_range, max_telar_range, max_non_radar)


class IadsGroundGroup(TheaterGroup):
    # IADS GroundObject Groups have a specific Role for the system
    iads_role: IadsRole = IadsRole.NO_BEHAVIOR

    @staticmethod
    def from_group(group: TheaterGroup) -> IadsGroundGroup:
        return IadsGroundGroup(
            group.id,
            group.name,
            group.position,
            group.units,
            group.ground_object,
        )
