from uuid import UUID
from fastapi import APIRouter, Depends

from game import Game
from .models import IadsConnectionJs, IadsNetworkJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/iads-network")


@router.get("/", operation_id="get_iads_network", response_model=IadsNetworkJs)
def get_iads_network(
    game: Game = Depends(GameContext.require),
) -> IadsNetworkJs:
    return IadsNetworkJs.from_network(game.theater.iads_network)


@router.get(
    "/for-tgo/{tgo_id}",
    operation_id="get_iads_connections_for_tgo",
    response_model=list[IadsConnectionJs],
)
def get_iads_connections_for_tgo(
    tgo_id: UUID, game: Game = Depends(GameContext.require)
) -> list[IadsConnectionJs]:
    return IadsConnectionJs.connections_for_tgo(tgo_id, game.theater.iads_network)
