from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from ..dependencies import GameContext, QtCallbacks, QtContext

router: APIRouter = APIRouter(prefix="/qt")


@router.post("/create-package/front-line/{front_line_id}")
def new_front_line_package(
    front_line_id: UUID,
    game: Game = Depends(GameContext.get),
    qt: QtCallbacks = Depends(QtContext.get),
) -> None:
    qt.create_new_package(game.db.front_lines.get(front_line_id))


@router.post("/create-package/tgo/{tgo_id}")
def new_tgo_package(
    tgo_id: UUID,
    game: Game = Depends(GameContext.get),
    qt: QtCallbacks = Depends(QtContext.get),
) -> None:
    qt.create_new_package(game.db.tgos.get(tgo_id))


@router.post("/info/tgo/{tgo_id}")
def show_tgo_info(
    tgo_id: UUID,
    game: Game = Depends(GameContext.get),
    qt: QtCallbacks = Depends(QtContext.get),
) -> None:
    qt.show_tgo_info(game.db.tgos.get(tgo_id))
