from fastapi import APIRouter, Depends

from game import Game
from game.utils import nautical_miles
from .models import FrontLineJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/front-lines")


@router.get("/")
def list_front_lines(game: Game = Depends(GameContext.get)) -> list[FrontLineJs]:
    front_lines = []
    for front_line in game.theater.conflicts():
        a = front_line.position.point_from_heading(
            front_line.attack_heading.right.degrees, nautical_miles(2).meters
        )
        b = front_line.position.point_from_heading(
            front_line.attack_heading.left.degrees, nautical_miles(2).meters
        )
        front_lines.append(FrontLineJs(extents=[a.latlng(), b.latlng()]))
    return front_lines
