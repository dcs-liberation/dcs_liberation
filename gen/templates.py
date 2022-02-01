from __future__ import annotations

import itertools
import logging
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Any, TYPE_CHECKING, Optional, Union

import dcs
import yaml
from dcs import Point
from dcs.unit import Unit
from dcs.unitgroup import StaticGroup
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
    from game.theater import TheaterGroundObject, ControlPoint


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
    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self.tasks: list[GroupTask] = []  # The supported tasks
        self.groups: list[GroupTemplate] = []

        # If the template is generic it will be used the generate the general
        # UnitGroups during faction initialization. Generic Groups allow to be mixed
        self.generic: bool = False

    def generate(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
        game: Game,
        merge_groups: bool = True,
    ) -> TheaterGroundObject:

        # Create the ground_object based on the type
        ground_object = self._create_ground_object(name, position, control_point)
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
                ground_group.name = f"{self.name} {group_id}"
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
                unit.name = f"{self.name} {group_id}-{unit_count + u_id}"
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

    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
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
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> IadsGroundObject:

        if GroupTask.EWR in self.tasks:
            return EwrGroundObject(name, position, position.heading, control_point)
        elif any(tasking in self.tasks for tasking in ROLE_TASKINGS[GroupRole.AntiAir]):
            return SamGroundObject(name, position, position.heading, control_point)
        raise RuntimeError(
            f" No Template for AntiAir tasking ({', '.join(task.value for task in self.tasks)})"
        )


class BuildingTemplate(GroundObjectTemplate):
    def _create_ground_object(
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
            if task not in [GroupTask.StrikeTarget, GroupTask.OffShoreStrikeTarget]:
                return task.value.lower()
        raise RuntimeError(f"Building Template {self.name} has no building category")


class NavalTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        if GroupTask.Navy in self.tasks:
            return ShipGroundObject(name, position, control_point)
        elif GroupTask.AircraftCarrier in self.tasks:
            return CarrierGroundObject(name, control_point)
        elif GroupTask.HelicopterCarrier in self.tasks:
            return LhaGroundObject(name, control_point)
        raise NotImplementedError


class DefensesTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        if GroupTask.Missile in self.tasks:
            return MissileSiteGroundObject(
                name, position, position.heading, control_point
            )
        elif GroupTask.Coastal in self.tasks:
            return CoastalSiteGroundObject(
                name, position, control_point, position.heading
            )
        raise NotImplementedError


class GroundForceTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        return VehicleGroupGroundObject(name, position, position.heading, control_point)


TEMPLATE_TYPES = {
    GroupRole.AntiAir: AntiAirTemplate,
    GroupRole.Building: BuildingTemplate,
    GroupRole.Naval: NavalTemplate,
    GroupRole.GroundForce: GroundForceTemplate,
    GroupRole.Defenses: DefensesTemplate,
}


@dataclass
class GroupTemplateMapping:
    # The group name used in the template.miz
    name: str

    # Defines if the group is required for the template or can be skipped
    optional: bool = False

    # All static units for the group
    statics: list[str] = field(default_factory=list)

    # Defines to which tgo group the groupTemplate will be added
    # This allows to merge groups back together. Default: Merge all to group 1
    group: int = field(default=1)

    # Randomization settings. If left empty the template will be generated with the
    # exact values (amount of units and unit_type) defined in the template.miz
    # How many units the template should generate. Will be used for randomization
    unit_count: list[int] = field(default_factory=list)
    # All unit types the template supports.
    unit_types: list[str] = field(default_factory=list)
    # All unit classes the template supports.
    unit_classes: list[UnitClass] = field(default_factory=list)
    alternative_classes: list[UnitClass] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = self.__dict__
        if not self.optional:
            d.pop("optional")
        if not self.statics:
            d.pop("statics")
        if not self.unit_types:
            d.pop("unit_types")
        if not self.unit_classes:
            d.pop("unit_classes")
        else:
            d["unit_classes"] = [unit_class.value for unit_class in self.unit_classes]
        if not self.alternative_classes:
            d.pop("alternative_classes")
        else:
            d["alternative_classes"] = [
                unit_class.value for unit_class in self.alternative_classes
            ]
        if not self.unit_count:
            d.pop("unit_count")
        return d

    @staticmethod
    def from_dict(d: dict[str, Any]) -> GroupTemplateMapping:
        optional = d["optional"] if "optional" in d else False
        statics = d["statics"] if "statics" in d else []
        unit_count = d["unit_count"] if "unit_count" in d else []
        unit_types = d["unit_types"] if "unit_types" in d else []
        group = d["group"] if "group" in d else 1
        unit_classes = (
            [UnitClass(u) for u in d["unit_classes"]] if "unit_classes" in d else []
        )
        alternative_classes = (
            [UnitClass(u) for u in d["alternative_classes"]]
            if "alternative_classes" in d
            else []
        )
        return GroupTemplateMapping(
            d["name"],
            optional,
            statics,
            group,
            unit_count,
            unit_types,
            unit_classes,
            alternative_classes,
        )


@dataclass
class TemplateMapping:
    # The name of the Template
    name: str

    # An optional description to give more information about the template
    description: str

    # An optional description to give more information about the template
    category: str

    # Optional field to define if the template can be used to create generic groups
    generic: bool

    # The role the template can be used for
    role: GroupRole

    # All taskings the template can be used for
    tasks: list[GroupTask]

    # All Groups the template has
    groups: list[GroupTemplateMapping] = field(default_factory=list)

    # Define the miz file for the template. Optional. If empty use the mapping name
    template_file: str = field(default="")

    def to_dict(self) -> dict[str, Any]:
        d = {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "generic": self.generic,
            "role": self.role.value,
            "tasks": [task.value for task in self.tasks],
            "groups": [group.to_dict() for group in self.groups],
            "template_file": self.template_file,
        }
        if not self.description:
            d.pop("description")
        if not self.category:
            d.pop("category")
        if not self.generic:
            # Only save if true
            d.pop("generic")
        if not self.template_file:
            d.pop("template_file")
        return d

    @staticmethod
    def from_dict(d: dict[str, Any], file_name: str) -> TemplateMapping:
        groups = [GroupTemplateMapping.from_dict(group) for group in d["groups"]]
        description = d["description"] if "description" in d else ""
        category = d["category"] if "category" in d else ""
        generic = d["generic"] if "generic" in d else False
        template_file = (
            d["template_file"]
            if "template_file" in d
            else file_name.replace("yaml", "miz")
        )
        tasks = [GroupTask(task) for task in d["tasks"]]
        return TemplateMapping(
            d["name"],
            description,
            category,
            generic,
            GroupRole(d["role"]),
            tasks,
            groups,
            template_file,
        )

    def export(self, mapping_folder: str) -> None:
        file_name = self.name
        for char in ["\\", "/", " ", "'", '"']:
            file_name = file_name.replace(char, "_")

        f = mapping_folder + file_name + ".yaml"
        with open(f, "w", encoding="utf-8") as data_file:
            yaml.dump(self.to_dict(), data_file, Dumper=MappingDumper, sort_keys=False)


# Custom Dumper to fix pyyaml indent https://github.com/yaml/pyyaml/issues/234
class MappingDumper(yaml.Dumper):
    def increase_indent(self, flow: bool = False, *args: Any, **kwargs: Any) -> None:
        return super().increase_indent(flow=flow, indentless=False)


class GroundObjectTemplates:
    # list of templates per category. e.g. AA or similar
    _templates: dict[GroupRole, list[GroundObjectTemplate]]

    def __init__(self) -> None:
        self._templates = {}

    @property
    def templates(self) -> Iterator[tuple[GroupRole, GroundObjectTemplate]]:
        for category, templates in self._templates.items():
            for template in templates:
                yield category, template

    @classmethod
    def from_folder(cls, folder: str) -> GroundObjectTemplates:
        templates = GroundObjectTemplates()
        mappings: dict[str, list[TemplateMapping]] = {}
        for file in Path(folder).rglob("*.yaml"):
            if not file.is_file():
                continue
            with file.open("r", encoding="utf-8") as f:
                mapping_dict = yaml.safe_load(f)

            template_map = TemplateMapping.from_dict(mapping_dict, f.name)

            if template_map.template_file in mappings:
                mappings[template_map.template_file].append(template_map)
            else:
                mappings[template_map.template_file] = [template_map]

        for miz, maps in mappings.items():
            for role, template in cls.load_from_miz(miz, maps).templates:
                templates.add_template(role, template)
        return templates

    @staticmethod
    def mapping_for_group(
        mappings: list[TemplateMapping], group_name: str
    ) -> tuple[TemplateMapping, int, GroupTemplateMapping]:
        for mapping in mappings:
            for g_id, group_mapping in enumerate(mapping.groups):
                if (
                    group_mapping.name == group_name
                    or group_name in group_mapping.statics
                ):
                    return mapping, g_id, group_mapping
        raise KeyError

    @classmethod
    def load_from_miz(
        cls, miz: str, mappings: list[TemplateMapping]
    ) -> GroundObjectTemplates:
        template_position: dict[str, Point] = {}
        templates = GroundObjectTemplates()
        temp_mis = dcs.Mission()
        temp_mis.load_file(miz)

        for country in itertools.chain(
            temp_mis.coalition["red"].countries.values(),
            temp_mis.coalition["blue"].countries.values(),
        ):
            for dcs_group in itertools.chain(
                temp_mis.country(country.name).vehicle_group,
                temp_mis.country(country.name).ship_group,
                temp_mis.country(country.name).static_group,
            ):
                try:
                    mapping, group_id, group_mapping = cls.mapping_for_group(
                        mappings, dcs_group.name
                    )
                except KeyError:
                    logging.error(f"No mapping for dcs group {dcs_group.name}")
                    continue
                template = templates.by_name(mapping.name)
                if not template:
                    template = TEMPLATE_TYPES[mapping.role](
                        mapping.name, mapping.description
                    )
                    template.generic = mapping.generic
                    template.tasks = mapping.tasks
                    templates.add_template(mapping.role, template)

                for i, unit in enumerate(dcs_group.units):
                    group_template = None
                    for group in template.groups:
                        if group.name == dcs_group.name or (
                            isinstance(dcs_group, StaticGroup)
                            and dcs_group.units[0].type in group.unit_types
                        ):
                            # MovingGroups are matched by name, statics by unit_type
                            group_template = group
                    if not group_template:
                        group_template = GroupTemplate(
                            dcs_group.name,
                            [],
                            True if isinstance(dcs_group, StaticGroup) else False,
                            group_mapping.group,
                            group_mapping.unit_count,
                            group_mapping.unit_types,
                            group_mapping.unit_classes,
                            group_mapping.alternative_classes,
                        )
                        group_template.optional = group_mapping.optional
                        # Add the group at the correct position
                        template.add_group(group_template, group_id)
                    unit_template = UnitTemplate.from_unit(unit)
                    if i == 0 and template.name not in template_position:
                        template_position[template.name] = unit.position
                    unit_template.position = (
                        unit_template.position - template_position[template.name]
                    )
                    group_template.units.append(unit_template)

        return templates

    @property
    def all(self) -> Iterator[GroundObjectTemplate]:
        for templates in self._templates.values():
            yield from templates

    def by_name(self, template_name: str) -> Optional[GroundObjectTemplate]:
        for template in self.all:
            if template.name == template_name:
                return template
        return None

    def add_template(self, role: GroupRole, template: GroundObjectTemplate) -> None:
        if role not in self._templates:
            self._templates[role] = [template]
        else:
            self._templates[role].append(template)

    def for_role_and_task(
        self, group_role: GroupRole, group_task: Optional[GroupTask] = None
    ) -> Iterator[GroundObjectTemplate]:
        if group_role not in self._templates:
            return None
        for template in self._templates[group_role]:
            if not group_task or group_task in template.tasks:
                yield template

    def for_role_and_tasks(
        self, group_role: GroupRole, group_tasks: list[GroupTask]
    ) -> Iterator[GroundObjectTemplate]:
        unique_templates = []
        for group_task in group_tasks:
            for template in self.for_role_and_task(group_role, group_task):
                if template not in unique_templates:
                    unique_templates.append(template)
        yield from unique_templates
