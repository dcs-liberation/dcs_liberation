from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from game.server import GameContext
from .models import HoldZonesJs, IpZonesJs, JoinZonesJs

router: APIRouter = APIRouter(prefix="/debug/waypoint-geometries")


@router.get("/hold/{flight_id}")
def hold_zones(flight_id: UUID, game: Game = Depends(GameContext.get)) -> HoldZonesJs:
    return HoldZonesJs.for_flight(game.db.flights.get(flight_id), game)


@router.get("/ip/{flight_id}")
def ip_zones(flight_id: UUID, game: Game = Depends(GameContext.get)) -> IpZonesJs:
    return IpZonesJs.for_flight(game.db.flights.get(flight_id), game)


@router.get("/join/{flight_id}")
def join_zones(flight_id: UUID, game: Game = Depends(GameContext.get)) -> JoinZonesJs:
    return JoinZonesJs.for_flight(game.db.flights.get(flight_id), game)
