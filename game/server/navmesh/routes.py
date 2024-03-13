from fastapi import APIRouter, Depends

from game import Game
from game.server import GameContext
from .models import NavMeshJs

router: APIRouter = APIRouter(prefix="/navmesh")


@router.get("/", operation_id="get_navmesh", response_model=NavMeshJs)
def get(for_player: bool, game: Game = Depends(GameContext.require)) -> NavMeshJs:
    mesh = game.coalition_for(for_player).nav_mesh
    return NavMeshJs.from_navmesh(mesh, game)
