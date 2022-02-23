from __future__ import annotations

from pydantic import BaseModel

from game.server.leaflet import LeafletPoly


class NavMeshPolyJs(BaseModel):
    poly: LeafletPoly
    threatened: bool
