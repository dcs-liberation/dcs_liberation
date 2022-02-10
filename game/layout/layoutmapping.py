from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Type

from dcs.unittype import UnitType as DcsUnitType

from game import db
from game.data.groups import GroupRole, GroupTask
from game.data.units import UnitClass


@dataclass
class GroupLayoutMapping:
    # The group name used in the template.miz
    name: str

    # Defines if the group is required for the template or can be skipped
    optional: bool = False

    # All static units for the group
    statics: list[str] = field(default_factory=list)

    # Defines to which tgo group the groupTemplate will be added
    # This allows to merge groups back together. Default: Merge all to group 1
    group: int = field(default=1)

    # How many units should be generated from the grouplayout. If only one value is
    # added this will be an exact amount. If 2 values are used it will be a random
    # amount between these values.
    unit_count: list[int] = field(default_factory=list)

    # All unit types the template supports.
    unit_types: list[Type[DcsUnitType]] = field(default_factory=list)

    # All unit classes the template supports.
    unit_classes: list[UnitClass] = field(default_factory=list)

    # TODO Clarify if this is required. Only used for EWRs to also Use SR when no
    #  dedicated EWRs are available to the faction
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
    def from_dict(d: dict[str, Any]) -> GroupLayoutMapping:
        optional = d["optional"] if "optional" in d else False
        statics = d["statics"] if "statics" in d else []
        unit_count = d["unit_count"] if "unit_count" in d else []
        unit_types = []
        if "unit_types" in d:
            for u in d["unit_types"]:
                unit_type = db.unit_type_from_name(u)
                if unit_type:
                    unit_types.append(unit_type)
        group = d["group"] if "group" in d else 1
        unit_classes = (
            [UnitClass(u) for u in d["unit_classes"]] if "unit_classes" in d else []
        )
        alternative_classes = (
            [UnitClass(u) for u in d["alternative_classes"]]
            if "alternative_classes" in d
            else []
        )
        return GroupLayoutMapping(
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
class LayoutMapping:
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
    groups: list[GroupLayoutMapping]

    # Define the miz file for the template. Optional. If empty use the mapping name
    layout_file: str

    def to_dict(self) -> dict[str, Any]:
        d = {
            "name": self.name,
            "description": self.description,
            "generic": self.generic,
            "role": self.role.value,
            "tasks": [task.description for task in self.tasks],
            "groups": [group.to_dict() for group in self.groups],
            "layout_file": self.layout_file,
        }
        if not self.description:
            d.pop("description")
        if not self.generic:
            # Only save if true
            d.pop("generic")
        if not self.layout_file:
            d.pop("layout_file")
        return d

    @staticmethod
    def from_dict(d: dict[str, Any], file_name: str) -> LayoutMapping:
        groups = [GroupLayoutMapping.from_dict(group) for group in d["groups"]]
        description = d["description"] if "description" in d else ""
        generic = d["generic"] if "generic" in d else False
        layout_file = (
            d["layout_file"] if "layout_file" in d else file_name.replace("yaml", "miz")
        )
        tasks = [GroupTask.by_description(task) for task in d["tasks"]]
        return LayoutMapping(
            d["name"],
            description,
            generic,
            GroupRole(d["role"]),
            tasks,
            groups,
            layout_file,
        )
