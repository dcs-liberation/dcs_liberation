from __future__ import annotations

import random
from typing import TYPE_CHECKING, Iterator, Optional
from game import db
from game.data.groups import GroupRole, GroupTask
from game.armedforces.forcegroup import ForceGroup
from game.profiling import logged_duration

if TYPE_CHECKING:
    from game.factions.faction import Faction


# TODO More comments and rename
class ArmedForces:
    """TODO Description"""

    # All available force groups for a specific Role
    forces: dict[GroupRole, list[ForceGroup]]

    def __init__(self, faction: Faction):
        with logged_duration(f"Loading armed forces for {faction.name}"):
            self._load_forces(faction)

    def add_or_update_force_group(self, new_group: ForceGroup) -> None:
        """TODO Description"""
        if new_group.role in self.forces:
            # Check if a force group with the same units exists
            for force_group in self.forces[new_group.role]:
                if (
                    force_group.units == new_group.units
                    and force_group.tasks == new_group.tasks
                ):
                    # Update existing group if units and tasks are equal
                    force_group.update_group(new_group)
                    return
        # Add a new force group
        self.add_force_group(new_group)

    def add_force_group(self, force_group: ForceGroup) -> None:
        """Adds a force group to the forces"""
        if force_group.role in self.forces:
            self.forces[force_group.role].append(force_group)
        else:
            self.forces[force_group.role] = [force_group]

    def _load_forces(self, faction: Faction) -> None:
        """Initialize all armed_forces for the given faction"""
        # This function will create a ForgeGroup for each global Layout and PresetGroup
        self.forces = {}

        preset_layouts = [
            layout
            for preset_group in faction.preset_groups
            for layout in preset_group.layouts
        ]

        # Generate Troops for all generic layouts and presets
        for layout in db.LAYOUTS.layouts:
            if (
                layout.generic or layout in preset_layouts
            ) and layout.usable_by_faction(faction):
                # Creates a faction compatible GorceGroup
                self.add_or_update_force_group(ForceGroup.for_layout(layout, faction))

    def groups_for_task(self, group_task: GroupTask) -> Iterator[ForceGroup]:
        for groups in self.forces.values():
            for unit_group in groups:
                if group_task in unit_group.tasks:
                    yield unit_group

    def groups_for_tasks(self, tasks: list[GroupTask]) -> list[ForceGroup]:
        groups = []
        for task in tasks:
            for group in self.groups_for_task(task):
                if group not in groups:
                    groups.append(group)
        return groups

    def random_group_for_task(self, group_task: GroupTask) -> Optional[ForceGroup]:
        unit_groups = list(self.groups_for_task(group_task))
        return random.choice(unit_groups) if unit_groups else None
