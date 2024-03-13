from fastapi import APIRouter, Depends

from game import Game
from game.server import GameContext
from .models import GameJs

router: APIRouter = APIRouter(prefix="/game")


@router.get("/", operation_id="get_game_state", response_model=GameJs)
def game_state(game: Game | None = Depends(GameContext.get)) -> GameJs | None:
    if game is None:
        return None
    return GameJs.from_game(game)
