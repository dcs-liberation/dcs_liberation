from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from game.server.leaflet import LeafletPoint, LeafletPoly, ShapelyUtil
from game.theater import ConflictTheater
from game.threatzones import ThreatZones

if TYPE_CHECKING:
    from game import Game


class MapZonesJs(BaseModel):
    inclusion: list[LeafletPoly]
    exclusion: list[LeafletPoly]
    sea: list[LeafletPoly]

    class Config:
        title = "MapZones"

    @classmethod
    def empty(cls) -> MapZonesJs:
        return MapZonesJs(inclusion=[], exclusion=[], sea=[])


class UnculledZoneJs(BaseModel):
    position: LeafletPoint
    radius: float

    class Config:
        title = "UnculledZone"

    @staticmethod
    def from_game(game: Game) -> list[UnculledZoneJs]:
        return [
            UnculledZoneJs(
                position=zone.latlng(),
                radius=game.settings.perf_culling_distance * 1000,
            )
            for zone in game.get_culling_zones()
        ]


class ThreatZonesJs(BaseModel):
    full: list[LeafletPoly]
    aircraft: list[LeafletPoly]
    air_defenses: list[LeafletPoly]
    radar_sams: list[LeafletPoly]

    class Config:
        title = "ThreatZones"

    @classmethod
    def from_zones(cls, zones: ThreatZones, theater: ConflictTheater) -> ThreatZonesJs:
        return ThreatZonesJs(
            full=ShapelyUtil.polys_to_leaflet(zones.all, theater),
            aircraft=ShapelyUtil.polys_to_leaflet(zones.airbases, theater),
            air_defenses=ShapelyUtil.polys_to_leaflet(zones.air_defenses, theater),
            radar_sams=ShapelyUtil.polys_to_leaflet(zones.radar_sam_threats, theater),
        )


class ThreatZoneContainerJs(BaseModel):
    blue: ThreatZonesJs
    red: ThreatZonesJs

    class Config:
        title = "ThreatZoneContainer"

    @staticmethod
    def for_game(game: Game) -> ThreatZoneContainerJs:
        return ThreatZoneContainerJs(
            blue=ThreatZonesJs.from_zones(
                game.threat_zone_for(player=True), game.theater
            ),
            red=ThreatZonesJs.from_zones(
                game.threat_zone_for(player=False), game.theater
            ),
        )
