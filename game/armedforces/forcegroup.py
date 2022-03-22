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
from game.layout import LAYOUTS
from game.layout.layout import AntiAirLayout, TgoLayout, TgoLayoutGroup
from game.point_with_heading import PointWithHeading
from game.theater.theatergroup import TheaterGroup

if TYPE_CHECKING:
    from game import Game
    from game.factions.faction import Faction
    from game.theater import TheaterGroundObject, ControlPoint


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
        for group in layout.all_groups:
            if group.optional and not group.fill:
                continue
            for unit_type in group.possible_types_for_faction(faction):
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

    def has_unit_for_layout_group(self, group: TgoLayoutGroup) -> bool:
        for unit in self.units:
            if (
                unit.dcs_unit_type in group.unit_types
                or unit.unit_class in group.unit_classes
            ):
                return True
        return False

    @classmethod
    def for_faction_by_name(cls, name: str, faction: Faction) -> ForceGroup:
        """Load a PresetGroup as ForceGroup with faction sensitive handling"""
        force_group = cls.named(name)
        for layout in force_group.layouts:
            for groups in layout.groups.values():
                for group in groups:
                    if group.fill and not force_group.has_unit_for_layout_group(group):
                        for unit_type in group.possible_types_for_faction(faction):
                            if issubclass(unit_type, VehicleType):
                                force_group.units.append(
                                    next(GroundUnitType.for_dcs_type(unit_type))
                                )
                            elif issubclass(unit_type, ShipType):
                                force_group.units.append(
                                    next(ShipUnitType.for_dcs_type(unit_type))
                                )
                            elif issubclass(unit_type, StaticType):
                                force_group.statics.append(unit_type)
        return force_group

    @classmethod
    def named(cls, name: str) -> ForceGroup:
        if not cls._loaded:
            cls._load_all()
        return cls._by_name[name]

    def has_access_to_dcs_type(self, type: Type[DcsUnitType]) -> bool:
        return (
            any(unit.dcs_unit_type == type for unit in self.units)
            or type in self.statics
        )

    def dcs_unit_types_for_group(
        self, group: TgoLayoutGroup
    ) -> list[Type[DcsUnitType]]:
        """Return all available DCS Unit Types which can be used in the given
        TgoLayoutGroup"""
        unit_types = [t for t in group.unit_types if self.has_access_to_dcs_type(t)]

        alternative_types = []
        for accessible_unit in self.units:
            if accessible_unit.unit_class in group.unit_classes:
                unit_types.append(accessible_unit.dcs_unit_type)
            if accessible_unit.unit_class in group.fallback_classes:
                alternative_types.append(accessible_unit.dcs_unit_type)

        return unit_types or alternative_types

    def unit_types_for_group(self, group: TgoLayoutGroup) -> Iterator[UnitType[Any]]:
        for dcs_type in self.dcs_unit_types_for_group(group):
            if issubclass(dcs_type, VehicleType):
                yield next(GroundUnitType.for_dcs_type(dcs_type))
            elif issubclass(dcs_type, ShipType):
                yield next(ShipUnitType.for_dcs_type(dcs_type))

    def statics_for_group(self, group: TgoLayoutGroup) -> Iterator[Type[DcsUnitType]]:
        for dcs_type in self.dcs_unit_types_for_group(group):
            if issubclass(dcs_type, StaticType):
                yield dcs_type

    def random_dcs_unit_type_for_group(
        self, group: TgoLayoutGroup
    ) -> Type[DcsUnitType]:
        """Return random DCS Unit Type which can be used in the given TgoLayoutGroup"""
        return random.choice(self.dcs_unit_types_for_group(group))

    def update_group(self, new_group: ForceGroup) -> None:
        """Update the group from another group.
        This will merge units, statics and layouts."""
        self.units = list(set(self.units + new_group.units))
        self.statics = list(set(self.statics + new_group.statics))
        self.layouts = list(set(self.layouts + new_group.layouts))

    def generate(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
        game: Game,
    ) -> TheaterGroundObject:
        """Create a random TheaterGroundObject from the available templates"""
        layout = random.choice(self.layouts)
        return self.create_ground_object_for_layout(
            layout, name, position, control_point, game
        )

    def create_ground_object_for_layout(
        self,
        layout: TgoLayout,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
        game: Game,
    ) -> TheaterGroundObject:
        """Create a TheaterGroundObject for the given template"""
        go = layout.create_ground_object(name, position, control_point)
        # Generate all groups using the randomization if it defined
        for group_name, groups in layout.groups.items():
            for group in groups:
                # Choose a random unit_type for the group
                try:
                    unit_type = self.random_dcs_unit_type_for_group(group)
                except IndexError:
                    if group.optional:
                        # If group is optional it is ok when no unit_type is available
                        continue
                    # if non-optional this is a error
                    raise RuntimeError(
                        f"No accessible unit for {self.name} - {group.name}"
                    )
                tgo_group_name = f"{name} ({group_name})"
                self.create_theater_group_for_tgo(
                    go, group, tgo_group_name, game, unit_type
                )

        return go

    def create_theater_group_for_tgo(
        self,
        ground_object: TheaterGroundObject,
        group: TgoLayoutGroup,
        group_name: str,
        game: Game,
        unit_type: Type[DcsUnitType],
        unit_count: Optional[int] = None,
    ) -> None:
        """Create a TheaterGroup and add it to the given TGO"""
        # Random UnitCounter if not forced
        if unit_count is None:
            unit_count = group.group_size
        # Generate Units
        units = group.generate_units(ground_object, unit_type, unit_count)
        # Get or create the TheaterGroup
        ground_group = ground_object.group_by_name(group_name)
        if ground_group is not None:
            # TheaterGroup with this name exists already. Extend it
            ground_group.units.extend(units)
        else:
            # TheaterGroup with the name was not created yet
            ground_object.groups.append(
                TheaterGroup.from_template(
                    game.next_group_id(),
                    group_name,
                    units,
                    ground_object,
                    unit_type,
                    unit_count,
                )
            )

        # Assign UniqueID, name and align relative to ground_object
        for unit in units:
            unit.id = game.next_unit_id()
            unit.name = unit.unit_type.name if unit.unit_type else unit.type.name
            unit.position = PointWithHeading.from_point(
                ground_object.position + unit.position,
                # Align heading to GroundObject defined by the campaign designer
                unit.position.heading + ground_object.heading,
            )
            if (
                isinstance(self, AntiAirLayout)
                and unit.unit_type
                and unit.unit_type.dcs_unit_type in UNITS_WITH_RADAR
            ):
                # Head Radars towards the center of the conflict
                unit.position.heading = (
                    game.theater.heading_to_conflict_from(unit.position)
                    or unit.position.heading
                )
            # Rotate unit around the center to align the orientation of the group
            unit.position.rotate(ground_object.position, ground_object.heading)

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

            units = [UnitType.named(unit) for unit in data.get("units")]
            if not units:
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
