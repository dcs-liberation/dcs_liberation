from __future__ import annotations

from typing import Iterable

from dcs import Point
from dcs.triggers import TriggerZoneCircular

from game.theater.theatergroundobject import NAME_BY_CATEGORY


class SceneryGroup:
    """Store information about a scenery objective."""

    def __init__(
        self,
        name: str,
        centroid: Point,
        category: str,
        target_zones: Iterable[TriggerZoneCircular],
    ) -> None:
        if not target_zones:
            raise ValueError(f"{name} has no valid target zones")

        if category not in NAME_BY_CATEGORY:
            raise ValueError(
                f"Campaign objective {name} uses unknown scenery objective "
                f"category: {category}"
            )

        self.name = name
        self.centroid = centroid
        self.category = category
        self.target_zones = list(target_zones)

    @staticmethod
    def category_of(group_zone: TriggerZoneCircular) -> str:
        try:
            # The first (1-indexed because lua) property of the group zone defines the
            # TGO category.
            category = group_zone.properties[1].get("value").lower()
        except IndexError as ex:
            raise RuntimeError(
                f"{group_zone.name} does not define an objective category"
            ) from ex
        return category

    @staticmethod
    def from_group_zone(
        group_zone: TriggerZoneCircular,
        unclaimed_target_zones: list[TriggerZoneCircular],
    ) -> SceneryGroup:
        return SceneryGroup(
            group_zone.name,
            group_zone.position,
            SceneryGroup.category_of(group_zone),
            SceneryGroup.claim_targets_for(group_zone, unclaimed_target_zones),
        )

    @staticmethod
    def from_trigger_zones(
        trigger_zones: Iterable[TriggerZoneCircular],
    ) -> list[SceneryGroup]:
        """Define scenery objectives based on their encompassing blue circle."""
        group_zones, target_zones = SceneryGroup.collect_scenery_zones(trigger_zones)
        return [SceneryGroup.from_group_zone(z, target_zones) for z in group_zones]

    @staticmethod
    def claim_targets_for(
        group_zone: TriggerZoneCircular,
        unclaimed_target_zones: list[TriggerZoneCircular],
    ) -> list[TriggerZoneCircular]:
        claimed_zones = []
        for zone in list(unclaimed_target_zones):
            if zone.position.distance_to_point(group_zone.position) < group_zone.radius:
                claimed_zones.append(zone)
                unclaimed_target_zones.remove(zone)
        return claimed_zones

    @staticmethod
    def collect_scenery_zones(
        zones: Iterable[TriggerZoneCircular],
    ) -> tuple[list[TriggerZoneCircular], list[TriggerZoneCircular]]:
        group_zones = []
        target_zones = []
        for zone in zones:
            if SceneryGroup.is_group_zone(zone):
                group_zones.append(zone)
            if SceneryGroup.is_target_zone(zone):
                target_zones.append(zone)
            # No error on else. We're iterating over all the trigger zones in the miz,
            # and others might be used for something else.
        return group_zones, target_zones

    @staticmethod
    def zone_has_color_rgb(
        zone: TriggerZoneCircular, r: float, g: float, b: float
    ) -> bool:
        # TriggerZone.color is a dict with keys 1 through 4, each being a component of
        # RGBA. It's absurd that it's a dict, but that's a lua quirk that's leaking from
        # pydcs.
        return (zone.color[1], zone.color[2], zone.color[3]) == (r, g, b)

    @staticmethod
    def is_group_zone(zone: TriggerZoneCircular) -> bool:
        return SceneryGroup.zone_has_color_rgb(zone, r=0, g=0, b=1)

    @staticmethod
    def is_target_zone(zone: TriggerZoneCircular) -> bool:
        return SceneryGroup.zone_has_color_rgb(zone, r=1, g=1, b=1)
