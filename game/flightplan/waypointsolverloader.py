import json
from functools import cached_property
from pathlib import Path
from typing import Any

from dcs.mapping import Point as DcsPoint, LatLng
from dcs.terrain import Terrain
from numpy import float64, array
from numpy._typing import NDArray
from shapely import transform
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry

from game.data.doctrine import Doctrine, ALL_DOCTRINES
from .ipsolver import IpSolver
from .waypointsolver import WaypointSolver
from ..theater.theaterloader import TERRAINS_BY_NAME


def doctrine_from_name(name: str) -> Doctrine:
    for doctrine in ALL_DOCTRINES:
        if doctrine.name == name:
            return doctrine
    raise KeyError


def geometry_ll_to_xy(geometry: BaseGeometry, terrain: Terrain) -> BaseGeometry:
    if geometry.is_empty:
        return geometry

    def ll_to_xy(points: NDArray[float64]) -> NDArray[float64]:
        ll_points = []
        for point in points:
            # Longitude is unintuitively first because it's the "X" coordinate:
            # https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.1
            p = DcsPoint.from_latlng(LatLng(point[1], point[0]), terrain)
            ll_points.append([p.x, p.y])
        return array(ll_points)

    return transform(geometry, ll_to_xy)


class WaypointSolverLoader:
    def __init__(self, debug_info_path: Path) -> None:
        self.debug_info_path = debug_info_path

    def load_data(self) -> dict[str, Any]:
        with self.debug_info_path.open(encoding="utf-8") as debug_info_file:
            return json.load(debug_info_file)

    @staticmethod
    def load_geometries(
        feature_collection: dict[str, Any], terrain: Terrain
    ) -> dict[str, BaseGeometry]:
        geometries = {}
        for feature in feature_collection["features"]:
            description = feature["properties"]["description"]
            geometry = shape(feature["geometry"])
            geometries[description] = geometry_ll_to_xy(geometry, terrain)
        return geometries

    @cached_property
    def terrain(self) -> Terrain:
        return TERRAINS_BY_NAME[self.load_data()["metadata"]["terrain"]]

    def load(self) -> WaypointSolver:
        data = self.load_data()
        metadata = data["metadata"]
        name = metadata.pop("name")
        terrain_name = metadata.pop("terrain")
        terrain = TERRAINS_BY_NAME[terrain_name]
        if "doctrine" in metadata:
            metadata["doctrine"] = doctrine_from_name(metadata["doctrine"])
        geometries = self.load_geometries(data, terrain)
        builder: type[WaypointSolver] = {
            "IpSolver": IpSolver,
        }[name]
        metadata.update(geometries)
        return builder(**metadata)
