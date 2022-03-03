from __future__ import annotations

from pydantic import BaseModel

from game.server.leaflet import LeafletPoint


class FrontLineJs(BaseModel):
    extents: list[LeafletPoint]
