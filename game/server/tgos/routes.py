from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from .models import TgoJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/tgos")


@router.get("/", operation_id="list_tgos", response_model=list[TgoJs])
def list_tgos(game: Game = Depends(GameContext.require)) -> list[TgoJs]:
    return TgoJs.all_in_game(game)


@router.get("/{tgo_id}", operation_id="get_tgo_by_id", response_model=TgoJs)
def get_tgo(tgo_id: UUID, game: Game = Depends(GameContext.require)) -> TgoJs:
    return TgoJs.for_tgo(game.db.tgos.get(tgo_id))
