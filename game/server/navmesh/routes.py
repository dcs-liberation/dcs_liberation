from fastapi import APIRouter, Depends

from game import Game
from game.server import GameContext
from .models import NavMeshPolyJs
from ..leaflet import ShapelyUtil

router: APIRouter = APIRouter(prefix="/navmesh")


@router.get("/", response_model=list[NavMeshPolyJs])
def get(
    for_player: bool, game: Game = Depends(GameContext.require)
) -> list[NavMeshPolyJs]:
    mesh = game.coalition_for(for_player).nav_mesh
    return [
        NavMeshPolyJs(
            poly=ShapelyUtil.poly_to_leaflet(p.poly, game.theater),
            threatened=p.threatened,
        )
        for p in mesh.polys
    ]
