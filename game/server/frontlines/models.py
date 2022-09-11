from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from game.server.leaflet import LeafletPoint
from game.utils import nautical_miles

if TYPE_CHECKING:
    from game import Game
    from game.theater import FrontLine


class FrontLineJs(BaseModel):
    id: UUID
    extents: list[LeafletPoint]

    class Config:
        title = "FrontLine"

    @staticmethod
    def for_front_line(front_line: FrontLine) -> FrontLineJs:
        a = front_line.position.point_from_heading(
            front_line.blue_forward_heading.right.degrees,
            nautical_miles(2).meters,
        )
        b = front_line.position.point_from_heading(
            front_line.blue_forward_heading.left.degrees,
            nautical_miles(2).meters,
        )
        return FrontLineJs(id=front_line.id, extents=[a.latlng(), b.latlng()])

    @staticmethod
    def all_in_game(game: Game) -> list[FrontLineJs]:
        return [FrontLineJs.for_front_line(f) for f in game.theater.conflicts()]
