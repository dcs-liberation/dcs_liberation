from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from game.missiongenerator.frontlineconflictdescription import (
    FrontLineConflictDescription,
)
from game.server.leaflet import LeafletPoint

if TYPE_CHECKING:
    from game import Game
    from game.theater import FrontLine, ConflictTheater


class FrontLineJs(BaseModel):
    id: UUID
    extents: list[LeafletPoint]

    class Config:
        title = "FrontLine"

    @staticmethod
    def for_front_line(theater: ConflictTheater, front_line: FrontLine) -> FrontLineJs:
        bounds = FrontLineConflictDescription.frontline_bounds(front_line, theater)
        return FrontLineJs(
            id=front_line.id,
            extents=[bounds.left_position.latlng(), bounds.right_position.latlng()],
        )

    @staticmethod
    def all_in_game(game: Game) -> list[FrontLineJs]:
        return [
            FrontLineJs.for_front_line(game.theater, f)
            for f in game.theater.conflicts()
        ]
