from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from .models import FrontLineJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/front-lines")


@router.get("/", operation_id="list_front_lines", response_model=list[FrontLineJs])
def list_front_lines(game: Game = Depends(GameContext.require)) -> list[FrontLineJs]:
    return FrontLineJs.all_in_game(game)


@router.get(
    "/{front_line_id}", operation_id="get_front_line_by_id", response_model=FrontLineJs
)
def get_front_line(
    front_line_id: UUID, game: Game = Depends(GameContext.require)
) -> FrontLineJs:
    return FrontLineJs.for_front_line(game.db.front_lines.get(front_line_id))
