from __future__ import annotations

from typing import Iterable, List

from dcs.triggers import TriggerZoneCircular

from game.theater.theatergroundobject import NAME_BY_CATEGORY


class SceneryGroupError(RuntimeError):
    """Error for when there are insufficient conditions to create a SceneryGroup."""

    pass


class SceneryGroup:
    """Store information about a scenery objective."""

    def __init__(
        self,
        group_zone: TriggerZoneCircular,
        target_zones: Iterable[TriggerZoneCircular],
        category: str,
    ) -> None:

        self.group_zone = group_zone
        self.target_zones = target_zones
        self.centroid = group_zone.position
        self.category = category

    @staticmethod
    def from_trigger_zones(
        trigger_zones: Iterable[TriggerZoneCircular],
    ) -> List[SceneryGroup]:
        """Define scenery objectives based on their encompassing blue/red circle."""
        group_zones = []
        target_zones = []

        scenery_groups = []

        # Aggregate trigger zones into different groups based on color.
        for zone in trigger_zones:
            if SceneryGroup.is_group_zone(zone):
                group_zones.append(zone)
            if SceneryGroup.is_target_zone(zone):
                target_zones.append(zone)

        # For each objective definition.
        for group_zone in group_zones:

            zone_def_radius = group_zone.radius
            zone_def_position = group_zone.position
            zone_def_name = group_zone.name

            if len(group_zone.properties) == 0:
                raise SceneryGroupError(
                    "Undefined SceneryGroup category in TriggerZone: " + zone_def_name
                )

            # Arbitrary campaign design requirement:  First property must define the category.
            zone_def_category = group_zone.properties[1].get("value").lower()

            valid_target_zones = []

            for zone in list(target_zones):
                if zone.position.distance_to_point(zone_def_position) < zone_def_radius:
                    valid_target_zones.append(zone)
                    target_zones.remove(zone)

            if len(valid_target_zones) > 0 and zone_def_category in NAME_BY_CATEGORY:
                scenery_groups.append(
                    SceneryGroup(group_zone, valid_target_zones, zone_def_category)
                )
            elif len(valid_target_zones) == 0:
                raise SceneryGroupError(
                    "No white triggerzones found in: " + zone_def_name
                )
            elif zone_def_category not in NAME_BY_CATEGORY:
                raise SceneryGroupError(
                    "Incorrect TriggerZone category definition for: "
                    + zone_def_name
                    + " in campaign definition.  TriggerZone category: "
                    + zone_def_category
                )

        return scenery_groups

    @staticmethod
    def is_group_zone(zone: TriggerZoneCircular) -> bool:
        # Blue in RGB is [0 Red], [0 Green], [1 Blue]. Ignore the fourth position: Transparency.
        return zone.color[1] == 0 and zone.color[2] == 0 and zone.color[3] == 1

    @staticmethod
    def is_target_zone(zone: TriggerZoneCircular) -> bool:
        # White in RGB is [1 Red], [1 Green], [1 Blue]. Ignore the fourth position: Transparency.
        return zone.color[1] == 1 and zone.color[2] == 1 and zone.color[3] == 1
