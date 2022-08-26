from __future__ import annotations
from collections import defaultdict

import logging
import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterator, Type, Optional

from dcs import Point
from dcs.unit import Unit
from dcs.unittype import UnitType as DcsUnitType

from game.data.groups import GroupRole, GroupTask
from game.data.units import UnitClass
from game.theater.iadsnetwork.iadsrole import IadsRole
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import (
    IadsBuildingGroundObject,
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
            unit.position,
            int(unit.heading),
        )


@dataclass
class TgoLayoutGroup:
    """The layout of a group which will generate a DCS group later. The TgoLayoutGroup has one or many TgoLayoutUnitGroup which represents a set of unit of the same type. Therefore the TgoLayoutGroup is a logical grouping of different unit_types. A TgoLayout can have one or many TgoLayoutGroup"""

    # The group name which will be used later as the DCS group name
    group_name: str

    # The index of the group within the TgoLayout. Used to preserve that the order of
    # the groups generated match the order defined in the layout yaml.
    group_index: int

    # List of all connected TgoLayoutUnitGroup
    unit_groups: list[TgoLayoutUnitGroup] = field(default_factory=list)


@dataclass
class TgoLayoutUnitGroup:
    """The layout of a single type of unit within the TgoLayout

    Each DCS group that is spawned in the mission is composed of one or more
    TgoLayoutGroup. Each TgoLayoutGroup will generate only a single type of unit.

    The merging of multiple TgoLayoutGroups to a single DCS group is defined in the
    TgoLayout with a dict which uses the Dcs group name as key and the corresponding
    TgoLayoutGroups as values.

    Each TgoLayoutGroup will be filled with a single type of unit when generated. The
    types compatible with the position can either be specified precisely (with
    unit_types) or generically (with unit_classes). If neither list specifies units
    that can be fulfilled by the faction, fallback_classes will be used. This allows
    the early-warning radar template, which prefers units that are defined as early
    warning radars like the 55G6, but to fall back to any radar usable by the faction
    if EWRs are not available.

    A TgoLayoutGroup may be optional. Factions or ForceGroups that are not able to
    provide an actual unit for the TgoLayoutGroup will still be able to use the layout;
    the optional TgoLayoutGroup will be omitted.
    """

    name: str
    layout_units: list[LayoutUnit]

    # Define the amount of units to be created. This can be a fixed int or a random
    # choice from a range of two ints. If the list is empty it will use the whole group
    # size / all available LayoutUnits
    unit_count: list[int] = field(default_factory=list)

    # defintion which unit types are supported
    unit_types: list[Type[DcsUnitType]] = field(default_factory=list)
    unit_classes: list[UnitClass] = field(default_factory=list)
    fallback_classes: list[UnitClass] = field(default_factory=list)

    # The index of the TgoLayoutGroup within the Layout
    unit_index: int = field(default_factory=int)

    # Allows a group to have a special SubTask (PointDefence for example)
    sub_task: Optional[GroupTask] = None

    # Defines if this groupTemplate is required or not
    optional: bool = False

    # Should this be filled by accessible units if optional or not
    fill: bool = True

    def possible_types_for_faction(self, faction: Faction) -> list[Type[DcsUnitType]]:
        """Determine the possible dcs unit types for the TgoLayoutGroup and the given faction"""
        unit_types = [t for t in self.unit_types if faction.has_access_to_dcs_type(t)]

        alternative_types = []
        for accessible_unit in faction.accessible_units:
            if accessible_unit.unit_class in self.unit_classes:
                unit_types.append(accessible_unit.dcs_unit_type)
            if accessible_unit.unit_class in self.fallback_classes:
                alternative_types.append(accessible_unit.dcs_unit_type)

        if not unit_types and not alternative_types and not self.optional:
            raise LayoutException(f"{self.name} not usable by faction {faction.name}")

        return unit_types or alternative_types

    @property
    def group_size(self) -> int:
        """The amount of units to be generated. If unit_count is defined in the layout this will be randomized accordingly. Otherwise this will be the maximum size."""
        if self.unit_count:
            if len(self.unit_count) == 1:
                return self.unit_count[0]
            return random.choice(range(min(self.unit_count), max(self.unit_count)))
        return self.max_size

    @property
    def max_size(self) -> int:
        return len(self.layout_units)

    def generate_units(
        self, go: TheaterGroundObject, unit_type: Type[DcsUnitType], amount: int
    ) -> list[TheaterUnit]:
        """Generate units of the given unit type and amount for the TgoLayoutGroup"""
        if amount > len(self.layout_units):
            raise LayoutException(
                f"{self.name} has incorrect unit_count for {unit_type.id}"
            )
        return [
            TheaterUnit.from_template(i, unit_type, self.layout_units[i], go)
            for i in range(amount)
        ]


class TgoLayout:
    """TgoLayout defines how a TheaterGroundObject will be generated from a ForceGroup. This defines the positioning, orientation, type and amount of the actual units

    Each TgoLayout is defined in resources/layouts with a .yaml file which has all the
    information about the Layout next to a .miz file which gives information about the
    actual position (x, y) and orientation (heading) of the units. The layout file also
    defines the structure of the DCS group (or groups) that will be spawned in the
    mission. Complex groups like SAMs protected by point-defense require specific
    grouping when used with plugins like Skynet. One group would define the main
    battery (the search and track radars, launchers, C2 units, etc), another would
    define PD units, and others could define SHORADs or resupply units.

    Each group (representing a DCS group) is further divided into TgoLayoutGroups. As
    a TgoLayoutGroup only represents a single dcs unit type the logical dcs group of multiple unit types will be created with the usage of a dict which has the DCS Group name as key and a list of TgoLayoutGroups which will be merged into this single dcs group.

    As the TgoLayout will be used to create a TheaterGroundObject for a ForceGroup,
    specialized classes inherit from this base class. For example there is a special
    AiDefenseLayout which will be used to create the SamGroundObject from it.
    """

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self.tasks: list[GroupTask] = []  # The supported

        # All TgoGroups this layout has.
        self.groups: list[TgoLayoutGroup] = []

        # A generic layout will be used to create generic ForceGroups during the
        # campaign initialization. For each generic layout a new Group will be created.
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
                for group in self.all_unit_groups
                if not group.optional
            )
        except LayoutException:
            return False

    def create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        """Create the TheaterGroundObject for the TgoLayout

        This function has to be implemented by the inheriting class to create
        a specific TGO like SamGroundObject or BuildingGroundObject
        """
        raise NotImplementedError

    @property
    def all_unit_groups(self) -> Iterator[TgoLayoutUnitGroup]:
        for group in self.groups:
            yield from group.unit_groups


class AntiAirLayout(TgoLayout):
    def create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> IadsGroundObject:

        if GroupTask.EARLY_WARNING_RADAR in self.tasks:
            return EwrGroundObject(name, location, control_point)
        elif any(tasking in self.tasks for tasking in GroupRole.AIR_DEFENSE.tasks):
            return SamGroundObject(name, location, control_point)
        raise RuntimeError(
            f" No Template for AntiAir tasking ({', '.join(task.description for task in self.tasks)})"
        )


class BuildingLayout(TgoLayout):
    def create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> BuildingGroundObject:
        iads_role = IadsRole.for_category(self.category)
        tgo_type = (
            IadsBuildingGroundObject if iads_role.participate else BuildingGroundObject
        )
        return tgo_type(
            name,
            self.category,
            location,
            control_point,
            self.category == "fob",
        )

    @property
    def category(self) -> str:
        for task in self.tasks:
            if task not in [GroupTask.STRIKE_TARGET, GroupTask.OFFSHORE_STRIKE_TARGET]:
                return task.description.lower()
        raise RuntimeError(f"Building Template {self.name} has no building category")


class NavalLayout(TgoLayout):
    def create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        if GroupTask.NAVY in self.tasks:
            return ShipGroundObject(name, location, control_point)
        elif GroupTask.AIRCRAFT_CARRIER in self.tasks:
            return CarrierGroundObject(name, location, control_point)
        elif GroupTask.HELICOPTER_CARRIER in self.tasks:
            return LhaGroundObject(name, location, control_point)
        raise NotImplementedError


class DefensesLayout(TgoLayout):
    def create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        if GroupTask.MISSILE in self.tasks:
            return MissileSiteGroundObject(name, location, control_point)
        elif GroupTask.COASTAL in self.tasks:
            return CoastalSiteGroundObject(name, location, control_point)
        raise NotImplementedError


class GroundForceLayout(TgoLayout):
    def create_ground_object(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        return VehicleGroupGroundObject(name, location, control_point)
