from datetime import timedelta
from uuid import UUID

from dcs.mapping import LatLng
from fastapi import APIRouter, Depends, HTTPException, status

from game import Game
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.server import GameContext
from game.server.waypoints.models import FlightWaypointJs
from game.utils import meters

router: APIRouter = APIRouter(prefix="/waypoints")


@router.get("/{flight_id}", response_model=list[FlightWaypointJs])
def all_waypoints_for_flight(
    flight_id: UUID, game: Game = Depends(GameContext.get)
) -> list[FlightWaypointJs]:
    flight = game.db.flights.get(flight_id)
    departure = FlightWaypointJs.for_waypoint(
        FlightWaypoint(
            "TAKEOFF",
            FlightWaypointType.TAKEOFF,
            flight.departure.position,
            meters(0),
            "RADIO",
        ),
        game.theater,
    )
    return [departure] + [
        FlightWaypointJs.for_waypoint(w, game.theater)
        for w in flight.flight_plan.waypoints
    ]


@router.post("/{flight_id}/{waypoint_idx}/position")
def set_position(
    flight_id: UUID,
    waypoint_idx: int,
    position: LatLng,
    game: Game = Depends(GameContext.get),
) -> None:
    flight = game.db.flights.get(flight_id)
    if waypoint_idx == 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    waypoint = flight.flight_plan.waypoints[waypoint_idx - 1]
    waypoint.position = game.theater.ll_to_point(position)
    package_model = (
        GameContext.get_model()
        .ato_model_for(flight.blue)
        .find_matching_package_model(flight.package)
    )
    if package_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find PackageModel owning {flight}",
        )
    package_model.update_tot()


@router.get("/{flight_id}/{waypoint_idx}/timing")
def waypoint_timing(
    flight_id: UUID, waypoint_idx: int, game: Game = Depends(GameContext.get)
) -> str | None:
    flight = game.db.flights.get(flight_id)
    if waypoint_idx == 0:
        return f"Depart T+{flight.flight_plan.takeoff_time()}"

    waypoint = flight.flight_plan.waypoints[waypoint_idx - 1]
    prefix = "TOT"
    time = flight.flight_plan.tot_for_waypoint(waypoint)
    if time is None:
        prefix = "Depart"
        time = flight.flight_plan.depart_time_for_waypoint(waypoint)
    if time is None:
        return ""
    return f"{prefix} T+{timedelta(seconds=int(time.total_seconds()))}"
