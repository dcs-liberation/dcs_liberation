from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from game.ato import Flight
from game.server import GameContext
from .models import HoldZonesJs, IpZonesJs, JoinZonesJs

router = APIRouter(prefix="/debug/waypoint-geometries")


# TODO: Maintain map of UUID -> Flight in Game.
def find_flight(game: Game, flight_id: UUID) -> Flight:
    for coalition in game.coalitions:
        for package in coalition.ato.packages:
            for flight in package.flights:
                if flight.id == flight_id:
                    return flight
    raise KeyError(f"No flight found with ID {flight_id}")


@router.get("/hold/{flight_id}")
def hold_zones(flight_id: UUID, game: Game = Depends(GameContext.get)) -> HoldZonesJs:
    flight = find_flight(game, flight_id)
    return HoldZonesJs.for_flight(flight, game)


@router.get("/ip/{flight_id}")
def ip_zones(flight_id: UUID, game: Game = Depends(GameContext.get)) -> IpZonesJs:
    flight = find_flight(game, flight_id)
    return IpZonesJs.for_flight(flight, game)


@router.get("/join/{flight_id}")
def join_zones(flight_id: UUID, game: Game = Depends(GameContext.get)) -> JoinZonesJs:
    flight = find_flight(game, flight_id)
    return JoinZonesJs.for_flight(flight, game)
