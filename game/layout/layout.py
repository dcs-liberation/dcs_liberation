from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Type

from dcs import Point
from dcs.unit import Unit
from dcs.unittype import UnitType as DcsUnitType

from game.data.groups import GroupRole, GroupTask
from game.data.units import UnitClass
from game.point_with_heading import PointWithHeading
from game.theater.theatergroundobject import (
    SamGroundObject,
    EwrGroundObject,
    BuildingGroundObject,
    MissileSiteGroundObject,
    ShipGroundObject,
    CarrierGroundObject,
    LhaGroundObject,
    CoastalSiteGroundObject,
    VehicleGroupGroundObject,
    IadsGroundObject,
)
from game.theater.theatergroup import TheaterUnit
from game.utils import Heading

if TYPE_CHECKING:
    from game.factions.faction import Faction
    from game.theater.theatergroundobject import TheaterGroundObject
    from game.theater.controlpoint import ControlPoint


class LayoutException(Exception):
    pass


@dataclass
class LayoutUnit:
    """The Position and Orientation of a single unit within the GroupLayout"""

    name: str
    position: Point
    heading: int

    @staticmethod
    def from_unit(unit: Unit) -> LayoutUnit:
        """Creates a LayoutUnit from a DCS Unit"""
        return LayoutUnit(
            unit.name,
            Point(int(unit.position.x), int(unit.position.y)),
            int(unit.heading),
        )


@dataclass
class GroupLayout:
    """The Layout of a TheaterGroup"""

    name: str
    units: list[LayoutUnit]

    # The group this template will be merged into
    group: int = 1

    # Define the amount of random units to be created by the randomizer.
    # This can be a fixed int or a random value from a range of two ints as tuple
    unit_count: list[int] = field(default_factory=list)

    # defintion which unit types are supported
    unit_types: list[Type[DcsUnitType]] = field(default_factory=list)
    unit_classes: list[UnitClass] = field(default_factory=list)
    alternative_classes: list[UnitClass] = field(default_factory=list)

    # Defines if this groupTemplate is required or not
    optional: bool = False

    # if enabled the specific group will be generated during generation
    # Can only be set to False if Optional = True
    enabled: bool = True

    # TODO Caching for faction!
    def possible_types_for_faction(self, faction: Faction) -> list[Type[DcsUnitType]]:
        """TODO Description"""
        unit_types = [t for t in self.unit_types if faction.has_access_to_dcs_type(t)]

        alternative_types = []
        for accessible_unit in faction.accessible_units:
            if accessible_unit.unit_class in self.unit_classes:
                unit_types.append(accessible_unit.dcs_unit_type)
            if accessible_unit.unit_class in self.alternative_classes:
                alternative_types.append(accessible_unit.dcs_unit_type)

        if not unit_types and not alternative_types and not self.optional:
            raise LayoutException

        return unit_types or alternative_types

    @property
    def unit_counter(self) -> int:
        """TODO Documentation"""
        default = len(self.units)
        if self.unit_count:
            if len(self.unit_count) == 1:
                count = self.unit_count[0]
            else:
                count = random.choice(range(min(self.unit_count), max(self.unit_count)))
            if count > default:
                logging.error(
                    f"UnitCount for Group Layout {self.name} "
                    f"exceeds max available units for this group"
                )
                return default
            return count
        return default

    @property
    def max_size(self) -> int:
        return len(self.units)

    def generate_units(
        self, go: TheaterGroundObject, unit_type: Type[DcsUnitType], amount: int
    ) -> list[TheaterUnit]:
        """TODO Documentation"""
        return [
            TheaterUnit.from_template(i, unit_type, self.units[i], go)
            for i in range(amount)
        ]


class TheaterLayout:
    """TODO Documentation"""

    def __init__(self, name: str, role: GroupRole, description: str = "") -> None:
        self.name = name
        self.role = role
        self.description = description
        self.tasks: list[GroupTask] = []  # The supported tasks
        self.groups: list[GroupLayout] = []

        # If the template is generic it will be used the generate the general
        # UnitGroups during faction initialization. Generic Groups allow to be mixed
        self.generic: bool = False

    def usable_by_faction(self, faction: Faction) -> bool:
        # Special handling for Buildings
        if (
            isinstance(self, BuildingLayout)
            and self.category not in faction.building_set
        ):
            return False

        # Check if faction has at least 1 possible unit for non-optional groups
        try:
            return all(
                len(group.possible_types_for_faction(faction)) > 0
                for group in self.groups
                if not group.optional
            )
        except LayoutException:
            return False

    def create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        """TODO Documentation"""
        raise NotImplementedError

    def add_group(self, new_group: GroupLayout, index: int = 0) -> None:
        """Adds a group in the correct order to the template"""
        if len(self.groups) > index:
            self.groups.insert(index, new_group)
        else:
            self.groups.append(new_group)

    @property
    def size(self) -> int:
        return sum([len(group.units) for group in self.groups])


class AntiAirLayout(TheaterLayout):
    def create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> IadsGroundObject:

        if GroupTask.EARLY_WARNING_RADAR in self.tasks:
            return EwrGroundObject(name, position, position.heading, control_point)
        elif any(tasking in self.tasks for tasking in GroupRole.AIR_DEFENSE.tasks):
            return SamGroundObject(name, position, position.heading, control_point)
        raise RuntimeError(
            f" No Template for AntiAir tasking ({', '.join(task.description for task in self.tasks)})"
        )


class BuildingLayout(TheaterLayout):
    def create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> BuildingGroundObject:
        return BuildingGroundObject(
            name,
            self.category,
            position,
            Heading.from_degrees(0),
            control_point,
            self.category == "fob",
        )

    @property
    def category(self) -> str:
        for task in self.tasks:
            if task not in [GroupTask.STRIKE_TARGET, GroupTask.OFFSHORE_STRIKE_TARGET]:
                return task.description.lower()
        raise RuntimeError(f"Building Template {self.name} has no building category")


class NavalLayout(TheaterLayout):
    def create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        if GroupTask.NAVY in self.tasks:
            return ShipGroundObject(name, position, control_point)
        elif GroupTask.AIRCRAFT_CARRIER in self.tasks:
            return CarrierGroundObject(name, control_point)
        elif GroupTask.HELICOPTER_CARRIER in self.tasks:
            return LhaGroundObject(name, control_point)
        raise NotImplementedError


class DefensesLayout(TheaterLayout):
    def create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        if GroupTask.MISSILE in self.tasks:
            return MissileSiteGroundObject(
                name, position, position.heading, control_point
            )
        elif GroupTask.COASTAL in self.tasks:
            return CoastalSiteGroundObject(
                name, position, control_point, position.heading
            )
        raise NotImplementedError


class GroundForceLayout(TheaterLayout):
    def create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        return VehicleGroupGroundObject(name, position, position.heading, control_point)
