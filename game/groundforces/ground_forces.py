from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING, Iterator, Optional

from game import db
from game.data.groups import GroupRole, GroupTask
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.groundforces.ground_force_group import GroundForceGroup
from game.groundforces.template import GroundObjectTemplate
from game.profiling import logged_duration

if TYPE_CHECKING:
    from game.factions.faction import Faction


class GroundForces:
    # All available ground groups
    groups: dict[GroupRole, list[GroundForceGroup]] = {}

    def __init__(self, faction: Faction):
        with logged_duration(f"Loading ground forces for {faction.name}"):
            self._load_ground_forces(faction)

    def _add_group(self, new_group: GroundForceGroup, merge: bool = True) -> None:
        if not new_group.templates:
            # Empty templates will throw an error on generation
            logging.error(
                f"Skipping Unit group {new_group.name} as no templates are available to generate the group"
            )
            return
        if new_group.role in self.groups:
            for group in self.groups[new_group.role]:
                if merge and all(task in group.tasks for task in new_group.tasks):
                    # Update existing group if same tasking
                    group.update_from_unit_group(new_group)
                    return
            # Add new Unit_group
            self.groups[new_group.role].append(new_group)
        else:
            self.groups[new_group.role] = [new_group]

    def _load_ground_forces(self, faction: Faction) -> None:
        # This function will create all the UnitGroups for the faction
        # It will create a unit group for each global Template, Building or
        # Legacy supported templates (not yet migrated from the generators).
        # For every preset_group there will be a separate UnitGroup so no mixed
        # UnitGroups will be generated for them. Special groups like complex SAM Systems
        self.groups = {}

        # Generate UnitGroups for all global templates
        for template in db.TEMPLATES.templates:
            # Build groups for generic templates and buildings
            if template.generic or template.role == GroupRole.Building:
                try:
                    # If template is faction compatible add a group from the template
                    group_template = template.for_faction(faction)
                    self._add_group_for_template(group_template)
                except StopIteration:
                    # Template is not usable by faction, skip
                    continue

        # Add preset groups
        for preset_group in faction.preset_groups:
            # Add as separate group, do not merge with generic groups!
            preset_group.load_templates(faction)
            self._add_group(preset_group, False)

    def _add_group_for_template(self, template: GroundObjectTemplate) -> None:
        group = GroundForceGroup(
            f"{template.role.value}: {', '.join([t.value for t in template.tasks])}",
            [u for u in template.units if isinstance(u, GroundUnitType)],
            [u for u in template.units if isinstance(u, ShipUnitType)],
            list(template.statics),
            template.role,
        )
        group.tasks = template.tasks
        group.set_templates([template])
        self._add_group(group)

    def groups_by_name(self, group_name: str) -> Iterator[GroundForceGroup]:
        for groups in self.groups.values():
            for unit_group in groups:
                if unit_group.name == group_name:
                    yield unit_group

    def groups_for_task(self, group_task: GroupTask) -> Iterator[GroundForceGroup]:
        for groups in self.groups.values():
            for unit_group in groups:
                if group_task in unit_group.tasks:
                    yield unit_group

    def groups_for_role_and_task(
        self, group_role: GroupRole, group_task: Optional[GroupTask] = None
    ) -> list[GroundForceGroup]:
        if group_role not in self.groups:
            return []
        groups = []
        for unit_group in self.groups[group_role]:
            if not group_task or group_task in unit_group.tasks:
                groups.append(unit_group)
        return groups

    def groups_for_role_and_tasks(
        self, group_role: GroupRole, tasks: list[GroupTask]
    ) -> list[GroundForceGroup]:
        groups = []
        for task in tasks:
            for group in self.groups_for_role_and_task(group_role, task):
                if group not in groups:
                    groups.append(group)
        return groups

    def random_group_for_role(
        self, group_role: GroupRole
    ) -> Optional[GroundForceGroup]:
        unit_groups = self.groups_for_role_and_task(group_role)
        return random.choice(unit_groups) if unit_groups else None

    def random_group_for_role_and_task(
        self, group_role: GroupRole, group_task: GroupTask
    ) -> Optional[GroundForceGroup]:
        unit_groups = self.groups_for_role_and_task(group_role, group_task)
        return random.choice(unit_groups) if unit_groups else None

    def random_group_for_role_and_tasks(
        self, group_role: GroupRole, tasks: list[GroupTask]
    ) -> Optional[GroundForceGroup]:
        unit_groups = self.groups_for_role_and_tasks(group_role, tasks)
        return random.choice(unit_groups) if unit_groups else None
