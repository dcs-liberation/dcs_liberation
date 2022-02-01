from __future__ import annotations

import itertools
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional, Any

import dcs
import yaml
from dcs import Point
from dcs.unitgroup import StaticGroup

from game.data.groups import GroupRole, GroupTask
from game.data.units import UnitClass
from game.groundforces.template import (
    GroundObjectTemplate,
    GroupTemplate,
    UnitTemplate,
    AntiAirTemplate,
    BuildingTemplate,
    NavalTemplate,
    GroundForceTemplate,
    DefensesTemplate,
)
from game.profiling import logged_duration

TEMPLATE_DIR = "resources/templates/"


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
            "generic": self.generic,
            "role": self.role.value,
            "tasks": [task.value for task in self.tasks],
            "groups": [group.to_dict() for group in self.groups],
            "template_file": self.template_file,
        }
        if not self.description:
            d.pop("description")
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


TEMPLATE_TYPES = {
    GroupRole.AntiAir: AntiAirTemplate,
    GroupRole.Building: BuildingTemplate,
    GroupRole.Naval: NavalTemplate,
    GroupRole.GroundForce: GroundForceTemplate,
    GroupRole.Defenses: DefensesTemplate,
}


class TemplateLoader:
    # list of templates per category. e.g. AA or similar
    _templates: dict[str, GroundObjectTemplate] = {}

    def __init__(self) -> None:
        self._templates = {}

    def initialize(self) -> None:
        if not self._templates:
            with logged_duration("Loading templates"):
                self.load_templates()

    @property
    def templates(self) -> Iterator[GroundObjectTemplate]:
        self.initialize()
        yield from self._templates.values()

    def load_templates(self) -> None:
        mappings: dict[str, list[TemplateMapping]] = {}
        with logged_duration("Parsing mapping yamls"):
            for file in Path(TEMPLATE_DIR).rglob("*.yaml"):
                if not file.is_file():
                    continue
                with file.open("r", encoding="utf-8") as f:
                    mapping_dict = yaml.safe_load(f)

                template_map = TemplateMapping.from_dict(mapping_dict, f.name)

                if template_map.template_file in mappings:
                    mappings[template_map.template_file].append(template_map)
                else:
                    mappings[template_map.template_file] = [template_map]

        with logged_duration(f"Loading templates multithreaded"):
            with ThreadPoolExecutor(max_workers=4) as exe:
                for miz, maps in mappings.items():
                    exe.submit(self._load_from_miz, miz, maps)

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

    def _load_from_miz(self, miz: str, mappings: list[TemplateMapping]) -> None:
        template_position: dict[str, Point] = {}
        temp_mis = dcs.Mission()
        with logged_duration("dcs mission loading"):
            # TODO This takes a lot of time... maybe this should be serialized to json
            # Example the whole routine: 0:00:00.934417, the .load_file() method: 0:00:00.920409
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
                    mapping, group_id, group_mapping = self.mapping_for_group(
                        mappings, dcs_group.name
                    )
                except KeyError:
                    logging.error(f"No mapping for dcs group {dcs_group.name}")
                    continue

                template = self._templates.get(mapping.name, None)
                if template is None:
                    # Create a new template
                    template = TEMPLATE_TYPES[mapping.role](
                        mapping.name, mapping.role, mapping.description
                    )
                    template.generic = mapping.generic
                    template.tasks = mapping.tasks
                    self._templates[template.name] = template

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

    def by_name(self, template_name: str) -> Iterator[GroundObjectTemplate]:
        for template in self.templates:
            if template.name == template_name:
                yield template

    def by_task(self, group_task: GroupTask) -> Iterator[GroundObjectTemplate]:
        for template in self.templates:
            if not group_task or group_task in template.tasks:
                yield template

    def by_tasks(self, group_tasks: list[GroupTask]) -> Iterator[GroundObjectTemplate]:
        unique_templates = []
        for group_task in group_tasks:
            for template in self.by_task(group_task):
                if template not in unique_templates:
                    unique_templates.append(template)
        yield from unique_templates
