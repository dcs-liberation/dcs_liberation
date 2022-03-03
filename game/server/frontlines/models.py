from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from game.server.leaflet import LeafletPoint
from game.theater import FrontLine
from game.utils import nautical_miles


class FrontLineJs(BaseModel):
    id: UUID
    extents: list[LeafletPoint]

    @staticmethod
    def for_front_line(front_line: FrontLine) -> FrontLineJs:
        a = front_line.position.point_from_heading(
            front_line.attack_heading.right.degrees, nautical_miles(2).meters
        )
        b = front_line.position.point_from_heading(
            front_line.attack_heading.left.degrees, nautical_miles(2).meters
        )
        return FrontLineJs(id=front_line.id, extents=[a.latlng(), b.latlng()])
