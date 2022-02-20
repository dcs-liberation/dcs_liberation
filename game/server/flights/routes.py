from uuid import UUID

from fastapi import APIRouter, Depends
from shapely.geometry import LineString, Point as ShapelyPoint

from game import Game
from game.server import GameContext
from game.server.leaflet import LeafletPoly, ShapelyUtil
from gen.flights.flightplan import CasFlightPlan, PatrollingFlightPlan

router: APIRouter = APIRouter(prefix="/flights")


@router.get("/{flight_id}/commit-boundary")
def commit_boundary(
    flight_id: UUID, game: Game = Depends(GameContext.get)
) -> LeafletPoly:
    flight = game.db.flights.get(flight_id)
    if not isinstance(flight.flight_plan, PatrollingFlightPlan):
        return []
    start = flight.flight_plan.patrol_start
    end = flight.flight_plan.patrol_end
    if isinstance(flight.flight_plan, CasFlightPlan):
        center = flight.flight_plan.target.position
        commit_center = ShapelyPoint(center.x, center.y)
    else:
        commit_center = LineString(
            [
                ShapelyPoint(start.x, start.y),
                ShapelyPoint(end.x, end.y),
            ]
        )
    bubble = commit_center.buffer(flight.flight_plan.engagement_distance.meters)
    return ShapelyUtil.poly_to_leaflet(bubble, game.theater)
