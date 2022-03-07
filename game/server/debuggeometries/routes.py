from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from game.server import GameContext
from .models import HoldZonesJs, IpZonesJs, JoinZonesJs

router: APIRouter = APIRouter(prefix="/debug/waypoint-geometries")


@router.get(
    "/hold/{flight_id}", operation_id="get_debug_hold_zones", response_model=HoldZonesJs
)
def hold_zones(
    flight_id: UUID, game: Game = Depends(GameContext.require)
) -> HoldZonesJs:
    return HoldZonesJs.for_flight(game.db.flights.get(flight_id), game)


@router.get(
    "/ip/{flight_id}", operation_id="get_debug_ip_zones", response_model=IpZonesJs
)
def ip_zones(flight_id: UUID, game: Game = Depends(GameContext.require)) -> IpZonesJs:
    return IpZonesJs.for_flight(game.db.flights.get(flight_id), game)


@router.get(
    "/join/{flight_id}", operation_id="get_debug_join_zones", response_model=JoinZonesJs
)
def join_zones(
    flight_id: UUID, game: Game = Depends(GameContext.require)
) -> JoinZonesJs:
    return JoinZonesJs.for_flight(game.db.flights.get(flight_id), game)
