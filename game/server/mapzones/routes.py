from fastapi import APIRouter, Depends, HTTPException, status

from game import Game
from game.server import GameContext
from .models import MapZonesJs, ThreatZoneContainerJs, UnculledZoneJs
from ..leaflet import ShapelyUtil

router: APIRouter = APIRouter(prefix="/map-zones")


@router.get("/terrain", operation_id="get_terrain_zones", response_model=MapZonesJs)
def get_terrain(game: Game = Depends(GameContext.require)) -> MapZonesJs:
    zones = game.theater.landmap
    if zones is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return MapZonesJs(
        inclusion=ShapelyUtil.polys_to_leaflet(zones.inclusion_zones, game.theater),
        exclusion=ShapelyUtil.polys_to_leaflet(zones.exclusion_zones, game.theater),
        sea=ShapelyUtil.polys_to_leaflet(zones.sea_zones, game.theater),
    )


@router.get(
    "/unculled", operation_id="list_unculled_zones", response_model=list[UnculledZoneJs]
)
def get_unculled_zones(
    game: Game = Depends(GameContext.require),
) -> list[UnculledZoneJs]:
    return UnculledZoneJs.from_game(game)


@router.get(
    "/threats", operation_id="get_threat_zones", response_model=ThreatZoneContainerJs
)
def get_threat_zones(
    game: Game = Depends(GameContext.require),
) -> ThreatZoneContainerJs:
    return ThreatZoneContainerJs.for_game(game)
