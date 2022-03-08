from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from dcs import Point
from shapely.ops import unary_union

from game.utils import dcs_to_shapely_point

if TYPE_CHECKING:
    from game.theater import ConflictTheater, TheaterGroundObject
    from game.threatzones import ThreatPoly


class SamEngagementZones:
    def __init__(
        self,
        threat_zones: ThreatPoly,
        individual_zones: list[tuple[TheaterGroundObject, ThreatPoly]],
    ) -> None:
        self.threat_zones = threat_zones
        self.individual_zones = individual_zones

    def covers(self, position: Point) -> bool:
        return self.threat_zones.intersects(dcs_to_shapely_point(position))

    def iter_threatening_sams(self, position: Point) -> Iterator[TheaterGroundObject]:
        for tgo, zone in self.individual_zones:
            if zone.intersects(dcs_to_shapely_point(position)):
                yield tgo

    @classmethod
    def from_theater(cls, theater: ConflictTheater, player: bool) -> SamEngagementZones:
        commit_regions = []
        individual_zones = []
        for cp in theater.control_points_for(player):
            for tgo in cp.connected_objectives:
                if (region := tgo.threat_poly()) is not None:
                    commit_regions.append(region)
                    individual_zones.append((tgo, region))
        return SamEngagementZones(unary_union(commit_regions), individual_zones)
