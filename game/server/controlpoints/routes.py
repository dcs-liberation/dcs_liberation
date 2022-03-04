from fastapi import APIRouter, Depends, HTTPException, status

from game import Game
from .models import ControlPointJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/control-points")


@router.get("/")
def list_control_points(game: Game = Depends(GameContext.get)) -> list[ControlPointJs]:
    control_points = []
    for control_point in game.theater.controlpoints:
        control_points.append(ControlPointJs.for_control_point(control_point))
    return control_points


@router.get("/{cp_id}")
def get_control_point(
    cp_id: int, game: Game = Depends(GameContext.get)
) -> ControlPointJs:
    cp = game.theater.find_control_point_by_id(cp_id)
    if cp is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Game has no control point with ID {cp_id}",
        )
    return ControlPointJs.for_control_point(cp)
