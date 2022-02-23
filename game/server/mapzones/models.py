from __future__ import annotations

from dcs.mapping import LatLng
from pydantic import BaseModel

from game.server.leaflet import LeafletPoly


class MapZonesJs(BaseModel):
    inclusion: list[LeafletPoly]
    exclusion: list[LeafletPoly]
    sea: list[LeafletPoly]


class UnculledZoneJs(BaseModel):
    position: LatLng
    radius: float
