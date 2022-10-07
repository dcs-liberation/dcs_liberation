from uuid import UUID

from dcs import Point
from dcs.mapping import LatLng
from fastapi import APIRouter, Body, Depends, HTTPException, status
from starlette.responses import Response

from game import Game
from .models import ControlPointJs
from ..dependencies import GameContext
from ..leaflet import LeafletPoint

router: APIRouter = APIRouter(prefix="/control-points")


@router.get(
    "/", operation_id="list_control_points", response_model=list[ControlPointJs]
)
def list_control_points(
    game: Game = Depends(GameContext.require),
) -> list[ControlPointJs]:
    return ControlPointJs.all_in_game(game)


@router.get(
    "/{cp_id}", operation_id="get_control_point_by_id", response_model=ControlPointJs
)
def get_control_point(
    cp_id: UUID, game: Game = Depends(GameContext.require)
) -> ControlPointJs:
    cp = game.theater.find_control_point_by_id(cp_id)
    if cp is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Game has no control point with ID {cp_id}",
        )
    return ControlPointJs.for_control_point(cp)


@router.get(
    "/{cp_id}/destination-in-range",
    operation_id="control_point_destination_in_range",
    response_model=bool,
)
def destination_in_range(
    cp_id: UUID, lat: float, lng: float, game: Game = Depends(GameContext.require)
) -> bool:
    cp = game.theater.find_control_point_by_id(cp_id)
    if cp is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Game has no control point with ID {cp_id}",
        )

    point = Point.from_latlng(LatLng(lat, lng), game.theater.terrain)
    return cp.destination_in_range(point)


@router.put(
    "/{cp_id}/destination",
    operation_id="set_control_point_destination",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def set_destination(
    cp_id: UUID,
    destination: LeafletPoint = Body(..., title="destination"),
    game: Game = Depends(GameContext.require),
) -> None:
    cp = game.theater.find_control_point_by_id(cp_id)
    if cp is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Game has no control point with ID {cp_id}",
        )
    if not cp.moveable:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"{cp} is not mobile")
    if not cp.captured:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail=f"{cp} is not owned by the player"
        )

    point = Point.from_latlng(
        LatLng(destination.lat, destination.lng), game.theater.terrain
    )
    if not cp.destination_in_range(point):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot move {cp} more than "
            f"{cp.max_move_distance.nautical_miles}nm.",
        )
    cp.target_position = point
    from .. import EventStream

    with EventStream.event_context() as events:
        events.update_control_point(cp)


@router.put(
    "/{cp_id}/cancel-travel",
    operation_id="clear_control_point_destination",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def cancel_travel(cp_id: UUID, game: Game = Depends(GameContext.require)) -> None:
    cp = game.theater.find_control_point_by_id(cp_id)
    if cp is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Game has no control point with ID {cp_id}",
        )
    if not cp.moveable:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"{cp} is not mobile")
    if not cp.captured:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail=f"{cp} is not owned by the player"
        )

    cp.target_position = None
    from .. import EventStream

    with EventStream.event_context() as events:
        events.update_control_point(cp)
