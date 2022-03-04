from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from .models import TgoJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/tgos")


@router.get("/")
def list_tgos(game: Game = Depends(GameContext.get)) -> list[TgoJs]:
    tgos = []
    for control_point in game.theater.controlpoints:
        for tgo in control_point.connected_objectives:
            if not tgo.is_control_point:
                tgos.append(TgoJs.for_tgo(tgo))
    return tgos


@router.get("/{tgo_id}")
def get_tgo(tgo_id: UUID, game: Game = Depends(GameContext.get)) -> TgoJs:
    return TgoJs.for_tgo(game.db.tgos.get(tgo_id))
