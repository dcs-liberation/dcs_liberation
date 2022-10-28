from __future__ import annotations

from typing import Iterable

from dcs import Point
from dcs.triggers import TriggerZone, TriggerZoneCircular, TriggerZoneQuadPoint
from shapely.geometry import Point as ShapelyPoint, Polygon

from game.theater.theatergroundobject import NAME_BY_CATEGORY


class SceneryGroup:
    """Store information about a scenery objective."""

    def __init__(
        self,
        name: str,
        centroid: Point,
        category: str,
        target_zones: Iterable[TriggerZone],
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
    def category_of(group_zone: TriggerZone) -> str:
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
        group_zone: TriggerZone,
        unclaimed_target_zones: list[TriggerZone],
    ) -> SceneryGroup:
        return SceneryGroup(
            group_zone.name,
            group_zone.position,
            SceneryGroup.category_of(group_zone),
            SceneryGroup.claim_targets_for(group_zone, unclaimed_target_zones),
        )

    @staticmethod
    def from_trigger_zones(
        trigger_zones: Iterable[TriggerZone],
    ) -> list[SceneryGroup]:
        """Define scenery objectives based on their encompassing blue circle."""
        group_zones, target_zones = SceneryGroup.collect_scenery_zones(trigger_zones)
        return [SceneryGroup.from_group_zone(z, target_zones) for z in group_zones]

    @staticmethod
    def claim_targets_for(
        group_zone: TriggerZone,
        unclaimed_target_zones: list[TriggerZone],
    ) -> list[TriggerZone]:
        claimed_zones = []
        group_poly = SceneryGroup.poly_for_zone(group_zone)
        for target in list(unclaimed_target_zones):
            # If the target zone is a quad point, the position is arbitrary but visible
            # to the designer. It is the "X" that marks the trigger zone in the ME. The
            # ME seems to place this at the centroid of the zone. If that X is in the
            # group zone, that's claimed.
            #
            # See https://github.com/pydcs/dcs/pull/243#discussion_r1001369516 for more
            # info.
            if group_poly.contains(ShapelyPoint(target.position.x, target.position.y)):
                claimed_zones.append(target)
                unclaimed_target_zones.remove(target)
        return claimed_zones

    @staticmethod
    def collect_scenery_zones(
        zones: Iterable[TriggerZone],
    ) -> tuple[list[TriggerZone], list[TriggerZone]]:
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
    def zone_has_color_rgb(zone: TriggerZone, r: float, g: float, b: float) -> bool:
        # TriggerZone.color is a dict with keys 1 through 4, each being a component of
        # RGBA. It's absurd that it's a dict, but that's a lua quirk that's leaking from
        # pydcs.
        return (zone.color[1], zone.color[2], zone.color[3]) == (r, g, b)

    @staticmethod
    def is_group_zone(zone: TriggerZone) -> bool:
        return SceneryGroup.zone_has_color_rgb(zone, r=0, g=0, b=1)

    @staticmethod
    def is_target_zone(zone: TriggerZone) -> bool:
        return SceneryGroup.zone_has_color_rgb(zone, r=1, g=1, b=1)

    @staticmethod
    def poly_for_zone(zone: TriggerZone) -> Polygon:
        if isinstance(zone, TriggerZoneCircular):
            return SceneryGroup.poly_for_circular_zone(zone)
        elif isinstance(zone, TriggerZoneQuadPoint):
            return SceneryGroup.poly_for_quad_point_zone(zone)
        else:
            raise ValueError(
                f"Invalid trigger zone type found for {zone.name}: "
                f"{zone.__class__.__name__}"
            )

    @staticmethod
    def poly_for_circular_zone(zone: TriggerZoneCircular) -> Polygon:
        return ShapelyPoint(zone.position.x, zone.position.y).buffer(zone.radius)

    @staticmethod
    def poly_for_quad_point_zone(zone: TriggerZoneQuadPoint) -> Polygon:
        return Polygon([(p.x, p.y) for p in zone.verticies])
