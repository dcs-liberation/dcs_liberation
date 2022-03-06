from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from .models import FrontLineJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/front-lines")


@router.get("/")
def list_front_lines(game: Game = Depends(GameContext.require)) -> list[FrontLineJs]:
    return FrontLineJs.all_in_game(game)


@router.get("/{front_line_id}")
def get_front_line(
    front_line_id: UUID, game: Game = Depends(GameContext.require)
) -> FrontLineJs:
    return FrontLineJs.for_front_line(game.db.front_lines.get(front_line_id))
