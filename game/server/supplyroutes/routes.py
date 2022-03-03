from fastapi import APIRouter, Depends

from game import Game
from .models import SupplyRouteJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/supply-routes")


@router.get("/")
def list_supply_routes(game: Game = Depends(GameContext.get)) -> list[SupplyRouteJs]:
    seen = set()
    routes = []
    for control_point in game.theater.controlpoints:
        seen.add(control_point)
        for destination, route in control_point.convoy_routes.items():
            if destination in seen:
                continue
            routes.append(
                SupplyRouteJs.for_link(
                    game, control_point, destination, list(route), sea=False
                )
            )
        for destination, route in control_point.shipping_lanes.items():
            if destination in seen:
                continue
            if not destination.is_friendly_to(control_point):
                continue
            routes.append(
                SupplyRouteJs.for_link(
                    game, control_point, destination, list(route), sea=True
                )
            )
    return routes
