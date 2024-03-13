from fastapi import APIRouter, Depends

from game import Game
from .models import SupplyRouteJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/supply-routes")


@router.get("/", operation_id="list_supply_routes", response_model=list[SupplyRouteJs])
def list_supply_routes(
    game: Game = Depends(GameContext.require),
) -> list[SupplyRouteJs]:
    return SupplyRouteJs.all_in_game(game)
