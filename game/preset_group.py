from __future__ import annotations

from game.data.groups import GroupTask
from dcs.triggers import TriggerZone

from typing import Iterable, List, Optional

from game.utils import Heading


class PresetTrigger:
    """A Trigger placed in the campaign.miz which defines a complex preset location with more information"""

    def __init__(
        self,
        zone: TriggerZone,
        scenery_zones: list[TriggerZone],
        task: GroupTask,
        template: str = "",
        unit_group: str = "",
        heading: Heading = Heading.from_degrees(0),
    ) -> None:

        self.zone = zone
        self.scenery_zones = scenery_zones
        self.position = zone.position
        self.heading = heading
        self.task = task
        self.template = template
        self.unit_group = unit_group

    @property
    def is_scenery_object(self) -> bool:
        return len(self.scenery_zones) > 0

    @staticmethod
    def from_trigger_zones(trigger_zones: Iterable[TriggerZone]) -> List[PresetTrigger]:
        """Define scenery objectives based on their encompassing blue/red circle."""
        zone_definitions = []
        white_zones = []
        presets = []

        # Aggregate trigger zones into different groups based on color.
        for zone in trigger_zones:
            if PresetTrigger.is_blue(zone):
                zone_definitions.append(zone)
            if PresetTrigger.is_white(zone):
                white_zones.append(zone)

        # For each objective definition.
        for zone_def in zone_definitions:
            if len(zone_def.properties) == 0:
                raise RuntimeError(
                    "Complex PresetTriggerZone is missing properties" + zone_def.name
                )

            group_task: Optional[GroupTask] = None
            template = ""
            unit_group = ""
            heading = 0
            for zone_property in zone_def.properties.values():
                key = zone_property.get("key")
                value = zone_property.get("value")
                if key == "Template":
                    template = value
                elif key == "UnitGroup":
                    unit_group = value
                elif key == "Heading":
                    heading = int(value)
                elif group_task is None:
                    # Try to find the property with the task
                    for task in GroupTask:
                        if value.lower() == task.value.lower():
                            group_task = task

            if not group_task:
                raise RuntimeError(f"The TriggerZone {zone_def.name} has no valid task")

            scenery_zones = []
            for zone in list(white_zones):
                if zone.position.distance_to_point(zone_def.position) < zone_def.radius:
                    scenery_zones.append(zone)
                    white_zones.remove(zone)

            presets.append(
                PresetTrigger(
                    zone_def,
                    scenery_zones,
                    group_task,
                    template,
                    unit_group,
                    Heading.from_degrees(heading),
                )
            )

        return presets

    @staticmethod
    def is_blue(zone: TriggerZone) -> bool:
        # Blue in RGB is [0 Red], [0 Green], [1 Blue]. Ignore the fourth position: Transparency.
        return zone.color[1] == 0 and zone.color[2] == 0 and zone.color[3] == 1

    @staticmethod
    def is_white(zone: TriggerZone) -> bool:
        # White in RGB is [1 Red], [1 Green], [1 Blue]. Ignore the fourth position: Transparency.
        return zone.color[1] == 1 and zone.color[2] == 1 and zone.color[3] == 1
