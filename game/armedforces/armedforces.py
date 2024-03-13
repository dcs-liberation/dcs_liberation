from __future__ import annotations

import random
from typing import TYPE_CHECKING, Iterator, Optional
from game.data.groups import GroupTask
from game.armedforces.forcegroup import ForceGroup
from game.layout import LAYOUTS
from game.profiling import logged_duration

if TYPE_CHECKING:
    from game.factions.faction import Faction


class ArmedForces:
    """Represents all ForceGroups which are available to the faction"""

    def __init__(self, faction: Faction):
        self.forces: list[ForceGroup] = []
        with logged_duration(f"Loading armed forces for {faction.name}"):
            self._load_forces(faction)

    def add_or_update_force_group(self, new_group: ForceGroup) -> None:
        """Adds or update a forcegroup depending if a forcegroup with the exact same
        tasking already exists"""
        # Check if a force group with the same tasking already exists
        for force_group in self.forces:
            if force_group.tasks == new_group.tasks:
                # Update existing group if tasks are equal
                force_group.merge_group(new_group)
                return
        # Add a new force group
        self.forces.append(new_group)

    def _load_forces(self, faction: Faction) -> None:
        """Initialize the ArmedForces for the given faction.
        This will create a ForceGroup for each generic Layout and PresetGroup"""

        # Generate ForceGroup for all generic layouts by iterating over
        # all layouts which are usable by the given faction.
        for layout in LAYOUTS.layouts:
            if layout.generic and layout.usable_by_faction(faction):
                # Creates a faction compatible GorceGroup
                self.add_or_update_force_group(ForceGroup.for_layout(layout, faction))

        # Add all preset groups afterwards to prevent them being merged with generics
        for preset_group in faction.preset_groups:
            self.forces.append(preset_group.initialize_for_faction(faction))

    def groups_for_task(self, group_task: GroupTask) -> Iterator[ForceGroup]:
        for force_group in self.forces:
            if group_task in force_group.tasks:
                yield force_group

    def groups_for_tasks(self, tasks: list[GroupTask]) -> list[ForceGroup]:
        groups = []
        for task in tasks:
            for group in self.groups_for_task(task):
                if group not in groups:
                    groups.append(group)
        return sorted(groups, key=lambda g: g.name)

    def random_group_for_task(self, group_task: GroupTask) -> Optional[ForceGroup]:
        unit_groups = list(self.groups_for_task(group_task))
        return random.choice(unit_groups) if unit_groups else None
