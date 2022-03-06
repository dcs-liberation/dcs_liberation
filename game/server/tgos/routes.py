from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from .models import TgoJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/tgos")


@router.get("/")
def list_tgos(game: Game = Depends(GameContext.require)) -> list[TgoJs]:
    return TgoJs.all_in_game(game)


@router.get("/{tgo_id}")
def get_tgo(tgo_id: UUID, game: Game = Depends(GameContext.require)) -> TgoJs:
    return TgoJs.for_tgo(game.db.tgos.get(tgo_id))
