from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field
from typing import Iterator, Any, TYPE_CHECKING, Optional

from dcs import Point
from dcs.unit import Unit
from dcs.unittype import VehicleType, ShipType
from game.data.radar_db import UNITS_WITH_RADAR
from game.data.units import UnitClass
from game.data.groups import GroupRole, GroupTask, ROLE_TASKINGS

from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.dcs.unittype import UnitType
from game.theater.theatergroundobject import (
    SamGroundObject,
    EwrGroundObject,
    BuildingGroundObject,
    GroundGroup,
    MissileSiteGroundObject,
    ShipGroundObject,
    CarrierGroundObject,
    LhaGroundObject,
    CoastalSiteGroundObject,
    VehicleGroupGroundObject,
    IadsGroundObject,
    GroundUnit,
)
from game.point_with_heading import PointWithHeading

from game.utils import Heading
from game import db

if TYPE_CHECKING:
    from game import Game
    from game.factions.faction import Faction
    from game.theater import TheaterGroundObject, ControlPoint, PresetLocation


@dataclass
class UnitTemplate:
    name: str
    position: Point
    heading: int

    @staticmethod
    def from_unit(unit: Unit) -> UnitTemplate:
        return UnitTemplate(
            unit.name,
            Point(int(unit.position.x), int(unit.position.y)),
            int(unit.heading),
        )


@dataclass
class GroupTemplate:
    name: str
    units: list[UnitTemplate]

    # Is Static group
    static: bool = False

    # The group this template will be merged into
    group: int = 1

    # Define the amount of random units to be created by the randomizer.
    # This can be a fixed int or a random value from a range of two ints as tuple
    unit_count: list[int] = field(default_factory=list)

    # defintion which unit types are supported
    unit_types: list[str] = field(default_factory=list)
    unit_classes: list[UnitClass] = field(default_factory=list)
    alternative_classes: list[UnitClass] = field(default_factory=list)

    # Defines if this groupTemplate is required or not
    optional: bool = False

    # Used to determine if the group should be generated or not
    _possible_types: list[str] = field(default_factory=list)
    _enabled: bool = True
    _unit_type: Optional[str] = None
    _unit_counter: Optional[int] = None

    def initialize_for_faction(
        self, faction: Faction, faction_sensitive: bool = True
    ) -> bool:
        # Sensitive defines if the initialization should check if the unit is available
        # to this faction or not. It is disabled for migration only atm.
        unit_types = [
            t
            for t in self.unit_types
            if not faction_sensitive or faction.has_access_to_unit_type(t)
        ]

        alternative_types = []
        for accessible_unit in faction.accessible_units:
            if accessible_unit.unit_class in self.unit_classes:
                unit_types.append(accessible_unit.dcs_id)
            if accessible_unit.unit_class in self.alternative_classes:
                alternative_types.append(accessible_unit.dcs_id)

        if not unit_types and not alternative_types and not self.optional:
            raise StopIteration

        types = unit_types or alternative_types
        self.set_possible_types(types)
        return len(types) > 0

    @property
    def should_be_generated(self) -> bool:
        if self.optional:
            return self._enabled
        return True

    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def is_enabled(self) -> bool:
        return self._enabled

    def set_unit_type(self, unit_type: str) -> None:
        self._unit_type = unit_type

    def set_possible_types(self, unit_types: list[str]) -> None:
        self._possible_types = unit_types

    def can_use_unit(self, unit_type: UnitType[Any]) -> bool:
        return (
            self.can_use_unit_type(unit_type.dcs_id)
            or unit_type.unit_class in self.unit_classes
        )

    def can_use_unit_type(self, unit_type: str) -> bool:
        return unit_type in self.unit_types

    def reset_unit_counter(self) -> None:
        count = len(self.units)
        if self.unit_count:
            if len(self.unit_count) == 1:
                count = self.unit_count[0]
            else:
                count = random.choice(range(min(self.unit_count), max(self.unit_count)))
        self._unit_counter = count

    @property
    def unit_type(self) -> str:
        if self._unit_type:
            # Forced type
            return self._unit_type
        unit_types = self._possible_types or self.unit_types
        if unit_types:
            # Random type
            return random.choice(unit_types)
        raise RuntimeError("TemplateGroup has no unit_type")

    @property
    def size(self) -> int:
        if not self._unit_counter:
            self.reset_unit_counter()
        assert self._unit_counter is not None
        return self._unit_counter

    @property
    def max_size(self) -> int:
        return len(self.units)

    def use_unit(self) -> None:
        if self._unit_counter is None:
            self.reset_unit_counter()
        if self._unit_counter and self._unit_counter > 0:
            self._unit_counter -= 1
        else:
            raise IndexError

    @property
    def can_be_modified(self) -> bool:
        return len(self._possible_types) > 1 or len(self.unit_count) > 1

    @property
    def statics(self) -> Iterator[str]:
        for unit_type in self._possible_types or self.unit_types:
            if db.static_type_from_name(unit_type):
                yield unit_type

    @property
    def possible_units(self) -> Iterator[UnitType[Any]]:
        for unit_type in self._possible_types or self.unit_types:
            dcs_unit_type = db.unit_type_from_name(unit_type)
            if dcs_unit_type is None:
                raise RuntimeError(f"Unit Type {unit_type} not a valid dcs type")
            try:
                if issubclass(dcs_unit_type, VehicleType):
                    yield next(GroundUnitType.for_dcs_type(dcs_unit_type))
                elif issubclass(dcs_unit_type, ShipType):
                    yield next(ShipUnitType.for_dcs_type(dcs_unit_type))
            except StopIteration:
                continue

    def generate_units(self, go: TheaterGroundObject) -> list[GroundUnit]:
        self.reset_unit_counter()
        units = []
        unit_type = self.unit_type
        for u_id, unit in enumerate(self.units):
            tgo_unit = GroundUnit.from_template(u_id, unit_type, unit, go)
            try:
                # Check if unit can be assigned
                self.use_unit()
            except IndexError:
                # Do not generate the unit as no more units are available
                continue
            units.append(tgo_unit)
        return units


class GroundObjectTemplate:
    def __init__(self, name: str, role: GroupRole, description: str = "") -> None:
        self.name = name
        self.role = role
        self.description = description
        self.tasks: list[GroupTask] = []  # The supported tasks
        self.groups: list[GroupTemplate] = []

        # If the template is generic it will be used the generate the general
        # UnitGroups during faction initialization. Generic Groups allow to be mixed
        self.generic: bool = False

    def generate(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
        game: Game,
        merge_groups: bool = True,
    ) -> TheaterGroundObject:

        # Create the ground_object based on the type
        ground_object = self._create_ground_object(name, location, control_point)
        # Generate all groups using the randomization if it defined
        for g_id, group in enumerate(self.groups):
            if not group.should_be_generated:
                continue
            # Static and non Static groups have to be separated
            unit_count = 0
            group_id = (group.group - 1) if merge_groups else g_id
            if not merge_groups or len(ground_object.groups) <= group_id:
                # Requested group was not yet created
                ground_group = GroundGroup.from_template(
                    game.next_group_id(),
                    group,
                    ground_object,
                )
                # Set Group Name
                ground_group.name = f"{name} {group_id}"
                ground_object.groups.append(ground_group)
                units = ground_group.units
            else:
                ground_group = ground_object.groups[group_id]
                units = group.generate_units(ground_object)
                unit_count = len(ground_group.units)
                ground_group.units.extend(units)

            # Assign UniqueID, name and align relative to ground_object
            for u_id, unit in enumerate(units):
                unit.id = game.next_unit_id()
                unit.name = unit.unit_type.name if unit.unit_type else unit.type
                unit.position = PointWithHeading.from_point(
                    Point(
                        ground_object.position.x + unit.position.x,
                        ground_object.position.y + unit.position.y,
                    ),
                    # Align heading to GroundObject defined by the campaign designer
                    unit.position.heading + ground_object.heading,
                )
                if (
                    isinstance(self, AntiAirTemplate)
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

        return ground_object

    def for_faction(self, faction: Faction) -> GroundObjectTemplate:
        # Initializes the template for the given Faction. This will remove all incompatible groups if they are optional
        # Will return None if the template is not compatible with the given Faction
        faction_template = copy.deepcopy(self)
        faction_template.groups[:] = [
            group_template
            for group_template in faction_template.groups
            if group_template.initialize_for_faction(faction)
        ]
        if (
            not (
                isinstance(faction_template, BuildingTemplate)
                # Special handling for strike targets. Skip if not supported by faction
                and GroupTask.StrikeTarget in faction_template.tasks
                and faction_template.category not in faction.building_set
            )
            and faction_template.groups
        ):
            return faction_template
        # Raise StopIteration if template is not usable for faction
        raise StopIteration

    def _create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        raise NotImplementedError

    def add_group(self, new_group: GroupTemplate, index: int = 0) -> None:
        """Adds a group in the correct order to the template"""
        if len(self.groups) > index:
            self.groups.insert(index, new_group)
        else:
            self.groups.append(new_group)

    def estimated_price_for(self, go: TheaterGroundObject) -> float:
        # Price can only be estimated because of randomization
        price = 0
        for group in self.groups:
            if group.should_be_generated:
                for unit in group.generate_units(go):
                    if unit.unit_type:
                        price += unit.unit_type.price
        return price

    @property
    def size(self) -> int:
        return sum([len(group.units) for group in self.groups])

    @property
    def statics(self) -> Iterator[str]:
        for group in self.groups:
            yield from group.statics

    @property
    def units(self) -> Iterator[UnitType[Any]]:
        for group in self.groups:
            yield from group.possible_units


class AntiAirTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> IadsGroundObject:

        if GroupTask.EWR in self.tasks:
            return EwrGroundObject(name, location, control_point)
        elif any(tasking in self.tasks for tasking in ROLE_TASKINGS[GroupRole.AntiAir]):
            return SamGroundObject(name, location, control_point)
        raise RuntimeError(
            f" No Template for AntiAir tasking ({', '.join(task.value for task in self.tasks)})"
        )


class BuildingTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> BuildingGroundObject:
        return BuildingGroundObject(
            name,
            self.category,
            location,
            control_point,
            self.category == "fob",
        )

    @property
    def category(self) -> str:
        for task in self.tasks:
            if task not in [GroupTask.StrikeTarget, GroupTask.OffShoreStrikeTarget]:
                return task.value.lower()
        raise RuntimeError(f"Building Template {self.name} has no building category")


class NavalTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        if GroupTask.Navy in self.tasks:
            return ShipGroundObject(name, location, control_point)
        elif GroupTask.AircraftCarrier in self.tasks:
            return CarrierGroundObject(name, control_point)
        elif GroupTask.HelicopterCarrier in self.tasks:
            return LhaGroundObject(name, control_point)
        raise NotImplementedError


class DefensesTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        if GroupTask.Missile in self.tasks:
            return MissileSiteGroundObject(name, location, control_point)
        elif GroupTask.Coastal in self.tasks:
            return CoastalSiteGroundObject(name, location, control_point)
        raise NotImplementedError


class GroundForceTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        return VehicleGroupGroundObject(name, location, control_point)
