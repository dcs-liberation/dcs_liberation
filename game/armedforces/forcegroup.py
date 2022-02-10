from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, TYPE_CHECKING, Type, Any, Iterator, Optional

import yaml
from dcs import Point

from game import db
from game.data.groups import GroupRole, GroupTask
from game.data.radar_db import UNITS_WITH_RADAR
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.dcs.unittype import UnitType
from game.point_with_heading import PointWithHeading
from game.layout.layout import TheaterLayout, AntiAirLayout, GroupLayout
from dcs.unittype import UnitType as DcsUnitType, VehicleType, ShipType, StaticType

from game.theater.theatergroup import TheaterGroup

if TYPE_CHECKING:
    from game import Game
    from game.factions.faction import Faction
    from game.theater import TheaterGroundObject, ControlPoint


@dataclass
class ForceGroup:
    """A logical group of multiple units and layouts which have a specific tasking"""

    name: str
    units: list[UnitType[Any]]
    statics: list[Type[DcsUnitType]]
    role: GroupRole
    tasks: list[GroupTask] = field(default_factory=list)
    layouts: list[TheaterLayout] = field(default_factory=list)

    _by_name: ClassVar[dict[str, ForceGroup]] = {}
    _by_role: ClassVar[dict[GroupRole, list[ForceGroup]]] = {}
    _loaded: bool = False

    @staticmethod
    def for_layout(layout: TheaterLayout, faction: Faction) -> ForceGroup:
        """TODO Documentation"""
        units: set[UnitType[Any]] = set()
        statics: set[Type[DcsUnitType]] = set()
        for group in layout.groups:
            for unit_type in group.possible_types_for_faction(faction):
                if issubclass(unit_type, VehicleType):
                    units.add(next(GroundUnitType.for_dcs_type(unit_type)))
                elif issubclass(unit_type, ShipType):
                    units.add(next(ShipUnitType.for_dcs_type(unit_type)))
                elif issubclass(unit_type, StaticType):
                    statics.add(unit_type)

        return ForceGroup(
            f"{layout.role.value}: {', '.join([t.description for t in layout.tasks])}",
            list(units),
            list(statics),
            layout.role,
            layout.tasks,
            [layout],
        )

    def __str__(self) -> str:
        return self.name

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

    def dcs_unit_types_for_group(self, group: GroupLayout) -> list[Type[DcsUnitType]]:
        """TODO Description"""
        unit_types = [t for t in group.unit_types if self.has_access_to_dcs_type(t)]

        alternative_types = []
        for accessible_unit in self.units:
            if accessible_unit.unit_class in group.unit_classes:
                unit_types.append(accessible_unit.dcs_unit_type)
            if accessible_unit.unit_class in group.alternative_classes:
                alternative_types.append(accessible_unit.dcs_unit_type)

        return unit_types or alternative_types

    def unit_types_for_group(self, group: GroupLayout) -> Iterator[UnitType[Any]]:
        for dcs_type in self.dcs_unit_types_for_group(group):
            if issubclass(dcs_type, VehicleType):
                yield next(GroundUnitType.for_dcs_type(dcs_type))
            elif issubclass(dcs_type, ShipType):
                yield next(ShipUnitType.for_dcs_type(dcs_type))

    def statics_for_group(self, group: GroupLayout) -> Iterator[Type[DcsUnitType]]:
        for dcs_type in self.dcs_unit_types_for_group(group):
            if issubclass(dcs_type, StaticType):
                yield dcs_type

    def random_dcs_unit_type_for_group(self, group: GroupLayout) -> Type[DcsUnitType]:
        """TODO Description"""
        return random.choice(self.dcs_unit_types_for_group(group))

    def update_group(self, new_group: ForceGroup) -> None:
        """Update the group from another group. This will merge statics and layouts."""
        # Merge layouts and statics
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
        layout: TheaterLayout,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
        game: Game,
    ) -> TheaterGroundObject:
        """Create a TheaterGroundObject for the given template"""
        go = layout.create_ground_object(name, position, control_point)
        # Generate all groups using the randomization if it defined
        for group in layout.groups:
            # Choose a random unit_type for the group
            try:
                unit_type = self.random_dcs_unit_type_for_group(group)
            except IndexError:
                if group.optional:
                    # If group is optional it is ok when no unit_type is available
                    continue
                # if non-optional this is a error
                raise RuntimeError(f"No accessible unit for {self.name} - {group.name}")
            self.create_theater_group_for_tgo(go, group, name, game, unit_type)

        return go

    def create_theater_group_for_tgo(
        self,
        ground_object: TheaterGroundObject,
        group: GroupLayout,
        name: str,
        game: Game,
        unit_type: Type[DcsUnitType],
        unit_count: Optional[int] = None,
    ) -> None:
        """Create a TheaterGroup and add it to the given TGO"""
        # Random UnitCounter if not forced
        if unit_count is None:
            unit_count = group.unit_counter
        # Static and non Static groups have to be separated
        group_id = group.group - 1
        if len(ground_object.groups) <= group_id:
            # Requested group was not yet created
            ground_group = TheaterGroup.from_template(
                game.next_group_id(), group, ground_object, unit_type, unit_count
            )
            # Set Group Name
            ground_group.name = f"{name} {group_id}"
            ground_object.groups.append(ground_group)
            units = ground_group.units
        else:
            ground_group = ground_object.groups[group_id]
            units = group.generate_units(ground_object, unit_type, unit_count)
            ground_group.units.extend(units)

        # Assign UniqueID, name and align relative to ground_object
        for u_id, unit in enumerate(units):
            unit.id = game.next_unit_id()
            unit.name = unit.unit_type.name if unit.unit_type else unit.type.name
            unit.position = PointWithHeading.from_point(
                Point(
                    ground_object.position.x + unit.position.x,
                    ground_object.position.y + unit.position.y,
                ),
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
        for file in Path("resources/units/groups").glob("*.yaml"):
            if not file.is_file():
                raise RuntimeError(f"{file.name} is not a valid ForceGroup")

            with file.open(encoding="utf-8") as data_file:
                data = yaml.safe_load(data_file)

            group_role = GroupRole(data.get("role"))

            group_tasks = [GroupTask.by_description(n) for n in data.get("tasks", [])]

            units = [UnitType.named(unit) for unit in data.get("units", [])]

            statics = []
            for static in data.get("statics", []):
                static_type = db.static_type_from_name(static)
                if static_type is None:
                    logging.error(f"Static {static} for {file} is not valid")
                else:
                    statics.append(static_type)

            layouts = [next(db.LAYOUTS.by_name(n)) for n in data.get("layouts")]

            force_group = ForceGroup(
                name=data.get("name"),
                units=units,
                statics=statics,
                role=group_role,
                tasks=group_tasks,
                layouts=layouts,
            )

            cls._by_name[force_group.name] = force_group
            if group_role in cls._by_role:
                cls._by_role[group_role].append(force_group)
            else:
                cls._by_role[group_role] = [force_group]

        cls._loaded = True
