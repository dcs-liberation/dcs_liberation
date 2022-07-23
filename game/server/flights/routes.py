from uuid import UUID

from fastapi import APIRouter, Depends
from shapely.geometry import LineString, Point as ShapelyPoint

from game import Game
from game.ato.flightplans.airassault import AirAssaultFlightPlan
from game.ato.flightplans.cas import CasFlightPlan
from game.ato.flightplans.patrolling import PatrollingFlightPlan
from game.server import GameContext
from game.server.flights.models import FlightJs
from game.server.leaflet import LeafletPoly, ShapelyUtil

router: APIRouter = APIRouter(prefix="/flights")


@router.get("/", operation_id="list_flights", response_model=list[FlightJs])
def list_flights(
    with_waypoints: bool = False, game: Game = Depends(GameContext.require)
) -> list[FlightJs]:
    return FlightJs.all_in_game(game, with_waypoints)


@router.get("/{flight_id}", operation_id="get_flight_by_id", response_model=FlightJs)
def get_flight(
    flight_id: UUID,
    with_waypoints: bool = False,
    game: Game = Depends(GameContext.require),
) -> FlightJs:
    flight = game.db.flights.get(flight_id)
    return FlightJs.for_flight(flight, with_waypoints)


@router.get(
    "/{flight_id}/commit-boundary",
    operation_id="get_commit_boundary_for_flight",
    response_model=LeafletPoly,
)
def commit_boundary(
    flight_id: UUID, game: Game = Depends(GameContext.require)
) -> LeafletPoly:
    flight = game.db.flights.get(flight_id)
    if isinstance(flight.flight_plan, CasFlightPlan) or isinstance(
        flight.flight_plan, AirAssaultFlightPlan
    ):
        # Special Commit boundary for CAS and AirAssault
        center = flight.flight_plan.layout.target.position
        commit_center = ShapelyPoint(center.x, center.y)
    elif isinstance(flight.flight_plan, PatrollingFlightPlan):
        # Commit boundary for standard patrolling flight plan
        start = flight.flight_plan.layout.patrol_start
        end = flight.flight_plan.layout.patrol_end
        commit_center = LineString(
            [
                ShapelyPoint(start.x, start.y),
                ShapelyPoint(end.x, end.y),
            ]
        )
    else:
        return []
    bubble = commit_center.buffer(flight.flight_plan.engagement_distance.meters)
    return ShapelyUtil.poly_to_leaflet(bubble, game.theater)
