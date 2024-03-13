from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from game.server.leaflet import LeafletPoly, ShapelyUtil

if TYPE_CHECKING:
    from game import Game
    from game.navmesh import NavMesh


class NavMeshPolyJs(BaseModel):
    poly: LeafletPoly
    threatened: bool

    class Config:
        title = "NavMeshPoly"


class NavMeshJs(BaseModel):
    polys: list[NavMeshPolyJs]

    class Config:
        title = "NavMesh"

    @staticmethod
    def from_navmesh(navmesh: NavMesh, game: Game) -> NavMeshJs:
        return NavMeshJs(
            polys=[
                NavMeshPolyJs(
                    poly=ShapelyUtil.poly_to_leaflet(p.poly, game.theater),
                    threatened=p.threatened,
                )
                for p in navmesh.polys
            ]
        )


class NavMeshesJs(BaseModel):
    blue: NavMeshJs
    red: NavMeshJs

    class Config:
        title = "NavMeshes"

    @staticmethod
    def from_game(game: Game) -> NavMeshesJs:
        return NavMeshesJs(
            blue=NavMeshJs.from_navmesh(game.blue.nav_mesh, game),
            red=NavMeshJs.from_navmesh(game.red.nav_mesh, game),
        )
