from __future__ import annotations

from dcs.mapping import LatLng
from pydantic import BaseModel

from game.server.leaflet import LeafletPoly, ShapelyUtil
from game.theater import ConflictTheater
from game.threatzones import ThreatZones


class MapZonesJs(BaseModel):
    inclusion: list[LeafletPoly]
    exclusion: list[LeafletPoly]
    sea: list[LeafletPoly]


class UnculledZoneJs(BaseModel):
    position: LatLng
    radius: float


class ThreatZonesJs(BaseModel):
    full: list[LeafletPoly]
    aircraft: list[LeafletPoly]
    air_defenses: list[LeafletPoly]
    radar_sams: list[LeafletPoly]

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
