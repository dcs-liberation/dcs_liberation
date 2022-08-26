from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar, Iterator, Optional, TYPE_CHECKING, Type

import yaml
from dcs.unittype import ShipType, StaticType, UnitType as DcsUnitType, VehicleType

from game.data.groups import GroupTask
from game.data.radar_db import UNITS_WITH_RADAR
from game.dcs.groundunittype import GroundUnitType
from game.dcs.helpers import static_type_from_name
from game.dcs.shipunittype import ShipUnitType
from game.dcs.unittype import UnitType
from game.theater.theatergroundobject import (
    IadsGroundObject,
    IadsBuildingGroundObject,
    NavalGroundObject,
)
from game.layout import LAYOUTS
from game.layout.layout import TgoLayout, TgoLayoutUnitGroup
from game.point_with_heading import PointWithHeading
from game.theater.theatergroup import IadsGroundGroup, IadsRole, TheaterGroup
from game.utils import escape_string_for_lua

if TYPE_CHECKING:
    from game import Game
    from game.factions.faction import Faction
    from game.theater import TheaterGroundObject, ControlPoint, PresetLocation


@dataclass
class ForceGroup:
    """A logical group of multiple units and layouts which have a specific tasking.

    ForceGroups will be generated during game and coalition initialization based on
    generic layouts and preset forcegroups.

    Every ForceGroup must have at least one unit, one task and one layout.

    A preset ForceGroup can for example be a S-300 SAM Battery which used many
    different unit types which all together handle a specific tasking (AirDefense)
    For this example the ForceGroup would consist of SR, TR, LN and so on next to
    statics. This group also has the Tasking LORAD and can have multiple (at least one)
    layouts which will be used to generate the actual DCS Group from it.
    """

    name: str
    units: list[UnitType[Any]]
    statics: list[Type[DcsUnitType]]
    tasks: list[GroupTask] = field(default_factory=list)
    layouts: list[TgoLayout] = field(default_factory=list)

    _by_name: ClassVar[dict[str, ForceGroup]] = {}
    _loaded: bool = False

    @staticmethod
    def for_layout(layout: TgoLayout, faction: Faction) -> ForceGroup:
        """Create a ForceGroup from the given TgoLayout which is usable by the faction

        This will iterate through all possible TgoLayoutGroups and check if the
        unit_types are accessible by the faction. All accessible units will be added to
        the force group
        """
        units: set[UnitType[Any]] = set()
        statics: set[Type[DcsUnitType]] = set()
        for unit_group in layout.all_unit_groups:
            if unit_group.optional and not unit_group.fill:
                continue
            for unit_type in unit_group.possible_types_for_faction(faction):
                if issubclass(unit_type, VehicleType):
                    units.add(next(GroundUnitType.for_dcs_type(unit_type)))
                elif issubclass(unit_type, ShipType):
                    units.add(next(ShipUnitType.for_dcs_type(unit_type)))
                elif issubclass(unit_type, StaticType):
                    statics.add(unit_type)

        return ForceGroup(
            ", ".join([t.description for t in layout.tasks]),
            list(units),
            list(statics),
            layout.tasks,
            [layout],
        )

    def __str__(self) -> str:
        return self.name

    def has_unit_for_layout_group(self, unit_group: TgoLayoutUnitGroup) -> bool:
        for unit in self.units:
            if (
                unit.dcs_unit_type in unit_group.unit_types
                or unit.unit_class in unit_group.unit_classes
            ):
                return True
        return False

    def initialize_for_faction(self, faction: Faction) -> ForceGroup:
        """Initialize a ForceGroup for the given Faction.
        This adds accessible units to LayoutGroups with the fill property"""
        for layout in self.layouts:
            for unit_group in layout.all_unit_groups:
                if unit_group.fill and not self.has_unit_for_layout_group(unit_group):
                    for unit_type in unit_group.possible_types_for_faction(faction):
                        if issubclass(unit_type, VehicleType):
                            self.units.append(
                                next(GroundUnitType.for_dcs_type(unit_type))
                            )
                        elif issubclass(unit_type, ShipType):
                            self.units.append(
                                next(ShipUnitType.for_dcs_type(unit_type))
                            )
                        elif issubclass(unit_type, StaticType):
                            self.statics.append(unit_type)
        return self

    @classmethod
    def from_preset_group(cls, name: str) -> ForceGroup:
        if not cls._loaded:
            cls._load_all()
        preset_group = cls._by_name[name]
        # Return a copy of the PresetGroup as new ForceGroup
        return ForceGroup(
            name=str(preset_group.name),
            units=list(preset_group.units),
            statics=list(preset_group.statics),
            tasks=list(preset_group.tasks),
            layouts=list(preset_group.layouts),
        )

    def has_access_to_dcs_type(self, type: Type[DcsUnitType]) -> bool:
        return (
            any(unit.dcs_unit_type == type for unit in self.units)
            or type in self.statics
        )

    def dcs_unit_types_for_group(
        self, unit_group: TgoLayoutUnitGroup
    ) -> list[Type[DcsUnitType]]:
        """Return all available DCS Unit Types which can be used in the given
        TgoLayoutGroup"""
        unit_types = [
            t for t in unit_group.unit_types if self.has_access_to_dcs_type(t)
        ]

        alternative_types = []
        for accessible_unit in self.units:
            if accessible_unit.unit_class in unit_group.unit_classes:
                unit_types.append(accessible_unit.dcs_unit_type)
            if accessible_unit.unit_class in unit_group.fallback_classes:
                alternative_types.append(accessible_unit.dcs_unit_type)

        return unit_types or alternative_types

    def unit_types_for_group(
        self, unit_group: TgoLayoutUnitGroup
    ) -> Iterator[UnitType[Any]]:
        for dcs_type in self.dcs_unit_types_for_group(unit_group):
            if issubclass(dcs_type, VehicleType):
                yield next(GroundUnitType.for_dcs_type(dcs_type))
            elif issubclass(dcs_type, ShipType):
                yield next(ShipUnitType.for_dcs_type(dcs_type))

    def statics_for_group(
        self, unit_group: TgoLayoutUnitGroup
    ) -> Iterator[Type[DcsUnitType]]:
        for dcs_type in self.dcs_unit_types_for_group(unit_group):
            if issubclass(dcs_type, StaticType):
                yield dcs_type

    def random_dcs_unit_type_for_group(
        self, unit_group: TgoLayoutUnitGroup
    ) -> Type[DcsUnitType]:
        """Return random DCS Unit Type which can be used in the given TgoLayoutGroup"""
        return random.choice(self.dcs_unit_types_for_group(unit_group))

    def merge_group(self, new_group: ForceGroup) -> None:
        """Merge the group with another similar group."""
        # Unified name for the resulting group
        self.name = ", ".join([t.description for t in self.tasks])
        # merge units, statics and layouts
        self.units = list(set(self.units + new_group.units))
        self.statics = list(set(self.statics + new_group.statics))
        self.layouts = list(set(self.layouts + new_group.layouts))

    def generate(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
        game: Game,
    ) -> TheaterGroundObject:
        """Create a random TheaterGroundObject from the available templates"""
        layout = random.choice(self.layouts)
        return self.create_ground_object_for_layout(
            layout, name, location, control_point, game
        )

    def create_ground_object_for_layout(
        self,
        layout: TgoLayout,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
        game: Game,
    ) -> TheaterGroundObject:
        """Create a TheaterGroundObject for the given template"""
        go = layout.create_ground_object(name, location, control_point)
        # Generate all groups using the randomization if it defined
        for tgo_group in layout.groups:
            for unit_group in tgo_group.unit_groups:
                # Choose a random unit_type for the group
                try:
                    unit_type = self.random_dcs_unit_type_for_group(unit_group)
                except IndexError:
                    if unit_group.optional:
                        # If group is optional it is ok when no unit_type is available
                        continue
                    # if non-optional this is a error
                    raise RuntimeError(
                        f"No accessible unit for {self.name} - {unit_group.name}"
                    )
                tgo_group_name = f"{name} ({tgo_group.group_name})"
                self.create_theater_group_for_tgo(
                    go, unit_group, tgo_group_name, game, unit_type
                )

        return go

    def create_theater_group_for_tgo(
        self,
        ground_object: TheaterGroundObject,
        unit_group: TgoLayoutUnitGroup,
        group_name: str,
        game: Game,
        unit_type: Type[DcsUnitType],
        unit_count: Optional[int] = None,
    ) -> None:
        """Create a TheaterGroup and add it to the given TGO"""
        # Random UnitCounter if not forced
        if unit_count is None:
            # Choose a random group_size based on the layouts unit_count
            unit_count = unit_group.group_size
        if unit_count == 0:
            # No units to be created so dont create a theater group for them
            return
        # Generate Units
        units = unit_group.generate_units(ground_object, unit_type, unit_count)
        # Get or create the TheaterGroup
        ground_group = ground_object.group_by_name(group_name)
        if ground_group is not None:
            # TheaterGroup with this name exists already. Extend it
            ground_group.units.extend(units)
        else:
            # TheaterGroup with the name was not created yet
            ground_group = TheaterGroup.from_template(
                game.next_group_id(), group_name, units, ground_object
            )
            # Special handling when part of the IADS (SAM, EWR, IADS Building, Navy)
            if (
                isinstance(ground_object, IadsGroundObject)
                or isinstance(ground_object, IadsBuildingGroundObject)
                or isinstance(ground_object, NavalGroundObject)
            ):
                # Recreate the TheaterGroup as IadsGroundGroup
                ground_group = IadsGroundGroup.from_group(ground_group)
                if unit_group.sub_task is not None:
                    # Use the special sub_task of the TheaterGroup
                    iads_task = unit_group.sub_task
                else:
                    # Use the primary task of the ForceGroup
                    iads_task = self.tasks[0]
                # Set the iads_role according the the task for the group
                ground_group.iads_role = IadsRole.for_task(iads_task)

            ground_object.groups.append(ground_group)

        # A layout has to be created with an orientation of 0 deg.
        # Therefore the the clockwise rotation angle is always the heading of the
        # groundobject without any calculation needed
        rotation = ground_object.heading

        # Assign UniqueID, name and align relative to ground_object
        for unit in units:
            unit.id = game.next_unit_id()
            # Add unit name escaped so that we do not have scripting issues later
            unit.name = escape_string_for_lua(
                unit.unit_type.name if unit.unit_type else unit.type.name
            )
            unit.position = PointWithHeading.from_point(
                ground_object.position + unit.position,
                # Align heading to GroundObject defined by the campaign designer
                unit.position.heading + rotation,
            )
            if (
                unit.unit_type is not None
                and isinstance(unit.unit_type, GroundUnitType)
                and unit.unit_type.reversed_heading
            ):
                # Reverse the heading of the unit
                unit.position.heading = unit.position.heading.opposite
            # Rotate unit around the center to align the orientation of the group
            unit.position.rotate(ground_object.position, rotation)

    @classmethod
    def _load_all(cls) -> None:
        for file in Path("resources/groups").glob("*.yaml"):
            if not file.is_file():
                raise RuntimeError(f"{file.name} is not a valid ForceGroup")

            with file.open(encoding="utf-8") as data_file:
                data = yaml.safe_load(data_file)

            name = data["name"]

            group_tasks = [GroupTask.by_description(n) for n in data.get("tasks")]
            if not group_tasks:
                logging.error(f"ForceGroup {name} has no valid tasking")
                continue

            units: list[UnitType[Any]] = []
            for unit in data.get("units"):
                if GroundUnitType.exists(unit):
                    units.append(GroundUnitType.named(unit))
                elif ShipUnitType.exists(unit):
                    units.append(ShipUnitType.named(unit))
                else:
                    logging.error(f"Unit {unit} of ForceGroup {name} is invalid")
            if len(units) == 0:
                logging.error(f"ForceGroup {name} has no valid units")
                continue

            statics = []
            for static in data.get("statics", []):
                static_type = static_type_from_name(static)
                if static_type is None:
                    logging.error(f"Static {static} for {file} is not valid")
                else:
                    statics.append(static_type)

            layouts = [LAYOUTS.by_name(n) for n in data.get("layouts")]
            if not layouts:
                logging.error(f"ForceGroup {name} has no valid layouts")
                continue

            force_group = ForceGroup(
                name=name,
                units=units,
                statics=statics,
                tasks=group_tasks,
                layouts=layouts,
            )

            cls._by_name[force_group.name] = force_group

        cls._loaded = True
