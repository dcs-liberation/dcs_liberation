from __future__ import annotations
from collections import defaultdict

from dataclasses import dataclass, field
from typing import Any, Optional, Type

from dcs.unittype import UnitType as DcsUnitType

from game.data.groups import GroupRole, GroupTask
from game.data.units import UnitClass
from game.dcs.helpers import unit_type_from_name


@dataclass
class GroupLayoutMapping:
    # The group name used in the template.miz
    name: str

    # Defines if the group is required for the template or can be skipped
    optional: bool = False

    # Should this be filled by accessible units if optional or not
    fill: bool = True

    # Allows a group to have a special SubTask (PointDefence for example)
    sub_task: Optional[GroupTask] = None

    # All static units for the group
    statics: list[str] = field(default_factory=list)

    # How many units should be generated from the grouplayout. If only one value is
    # added this will be an exact amount. If 2 values are used it will be a random
    # amount between these values.
    unit_count: list[int] = field(default_factory=list)

    # All unit types the template supports.
    unit_types: list[Type[DcsUnitType]] = field(default_factory=list)

    # All unit classes the template supports.
    unit_classes: list[UnitClass] = field(default_factory=list)

    # Fallback Classes which are used when the unit_classes and unit_types do not fit any accessible unit from the faction. Only used for EWRs to also Use SR when no
    #  dedicated EWRs are available to the faction
    fallback_classes: list[UnitClass] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict[str, Any]) -> GroupLayoutMapping:
        optional = d["optional"] if "optional" in d else False
        fill = d["fill"] if "fill" in d else True
        sub_task = GroupTask.by_description(d["sub_task"]) if "sub_task" in d else None
        statics = d["statics"] if "statics" in d else []
        unit_count = d["unit_count"] if "unit_count" in d else []
        unit_types = []
        if "unit_types" in d:
            for u in d["unit_types"]:
                unit_type = unit_type_from_name(u)
                if unit_type:
                    unit_types.append(unit_type)
        unit_classes = (
            [UnitClass(u) for u in d["unit_classes"]] if "unit_classes" in d else []
        )
        fallback_classes = (
            [UnitClass(u) for u in d["fallback_classes"]]
            if "fallback_classes" in d
            else []
        )
        return GroupLayoutMapping(
            d["name"],
            optional,
            fill,
            sub_task,
            statics,
            unit_count,
            unit_types,
            unit_classes,
            fallback_classes,
        )


@dataclass
class LayoutMapping:
    # The name of the Template
    name: str

    # An optional description to give more information about the template
    description: str

    # Optional field to define if the template can be used to create generic groups
    generic: bool

    # All taskings the template can be used for
    tasks: list[GroupTask]

    # All Groups the template has
    groups: dict[str, list[GroupLayoutMapping]]

    # Define the miz file for the template. Optional. If empty use the mapping name
    layout_file: str

    @property
    def primary_role(self) -> GroupRole:
        return self.tasks[0].role

    @staticmethod
    def from_dict(d: dict[str, Any], file_name: str) -> LayoutMapping:
        groups: dict[str, list[GroupLayoutMapping]] = defaultdict(list)
        for group in d["groups"]:
            for group_name, group_layouts in group.items():
                groups[group_name].extend(
                    [
                        GroupLayoutMapping.from_dict(group_layout)
                        for group_layout in group_layouts
                    ]
                )

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
            tasks,
            groups,
            layout_file,
        )

    def group_for_name(self, name: str) -> tuple[int, int, str, GroupLayoutMapping]:
        g_id = 0
        for group_name, group_mappings in self.groups.items():
            for u_id, group_mapping in enumerate(group_mappings):
                if group_mapping.name == name or name in group_mapping.statics:
                    return g_id, u_id, group_name, group_mapping
            g_id += 1
        raise KeyError
