from fastapi import APIRouter, Depends

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
