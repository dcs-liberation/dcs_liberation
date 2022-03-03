from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from ..dependencies import GameContext, QtCallbacks, QtContext

router: APIRouter = APIRouter(prefix="/package-dialog")


@router.post("/front-line/{front_line_id}")
def new_front_line_package(
    front_line_id: UUID,
    game: Game = Depends(GameContext.get),
    qt: QtCallbacks = Depends(QtContext.get),
) -> None:
    front_line = game.db.front_lines.get(front_line_id)
    qt.create_new_package(front_line)
