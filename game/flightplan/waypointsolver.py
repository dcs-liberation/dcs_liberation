from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any

from dcs import Point
from dcs.mapping import Point as DcsPoint
from dcs.terrain import Terrain
from numpy import float64, array
from numpy._typing import NDArray
from shapely import transform, to_geojson
from shapely.geometry.base import BaseGeometry

if TYPE_CHECKING:
    from .waypointstrategy import WaypointStrategy


class NoSolutionsError(RuntimeError):
    pass


class WaypointSolver:
    def __init__(self) -> None:
        self.strategies: list[WaypointStrategy] = []
        self.debug_output_directory: Path | None = None
        self._terrain: Terrain | None = None

    def add_strategy(self, strategy: WaypointStrategy) -> None:
        self.strategies.append(strategy)

    def set_debug_properties(self, path: Path, terrain: Terrain) -> None:
        self.debug_output_directory = path
        self._terrain = terrain

    def to_geojson(self, geometry: BaseGeometry) -> dict[str, Any]:
        if geometry.is_empty:
            return json.loads(to_geojson(geometry))

        assert self._terrain is not None
        origin = DcsPoint(0, 0, self._terrain)

        def xy_to_ll(points: NDArray[float64]) -> NDArray[float64]:
            ll_points = []
            for point in points:
                p = origin.new_in_same_map(point[0], point[1])
                latlng = p.latlng()
                # Longitude is unintuitively first because it's the "X" coordinate:
                # https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.1
                ll_points.append([latlng.lng, latlng.lat])
            return array(ll_points)

        transformed = transform(geometry, xy_to_ll)
        return json.loads(to_geojson(transformed))

    def describe_metadata(self) -> dict[str, Any]:
        return {}

    def describe_inputs(self) -> Iterator[tuple[str, BaseGeometry]]:
        yield from []

    def describe_debug(self) -> dict[str, Any]:
        assert self._terrain is not None
        metadata = {"name": self.__class__.__name__, "terrain": self._terrain.name}
        metadata.update(self.describe_metadata())
        return {
            "type": "FeatureCollection",
            # The GeoJSON spec forbids us from adding a "properties" field to a feature
            # collection, but it doesn't restrict us from adding our own custom fields.
            # https://gis.stackexchange.com/a/209263
            #
            # It's possible that some consumers won't work with this, but we don't read
            # collections directly with shapely and geojson.io is happy with it, so it
            # works where we need it to.
            "metadata": metadata,
            "features": list(self.describe_features()),
        }

    def describe_features(self) -> Iterator[dict[str, Any]]:
        for description, geometry in self.describe_inputs():
            yield {
                "type": "Feature",
                "properties": {
                    "description": description,
                },
                "geometry": self.to_geojson(geometry),
            }

    def dump_debug_info(self) -> None:
        path = self.debug_output_directory
        if path is None:
            return

        path.mkdir(exist_ok=True, parents=True)

        inputs_path = path / "solver.json"
        with inputs_path.open("w", encoding="utf-8") as inputs_file:
            json.dump(self.describe_debug(), inputs_file)

        features = list(self.describe_features())
        for idx, strategy in enumerate(self.strategies):
            strategy_path = path / f"{idx}.json"
            with strategy_path.open("w", encoding="utf-8") as strategy_debug_file:
                json.dump(
                    {
                        "type": "FeatureCollection",
                        "metadata": {
                            "name": strategy.__class__.__name__,
                            "prerequisites": [
                                p.describe_debug_info(self.to_geojson)
                                for p in strategy.prerequisites
                            ],
                        },
                        # Include the solver's features in the strategy feature
                        # collection for easy copy/paste into geojson.io.
                        "features": features
                        + [
                            d.to_geojson(self.to_geojson)
                            for d in strategy.iter_debug_info()
                        ],
                    },
                    strategy_debug_file,
                )

    def solve(self) -> Point:
        if not self.strategies:
            raise ValueError(
                "WaypointSolver.solve() called before any strategies were added"
            )

        for strategy in self.strategies:
            if (point := strategy.find()) is not None:
                return point

        self.dump_debug_info()
        debug_details = "No debug output directory set"
        if (debug_path := self.debug_output_directory) is not None:
            debug_details = f"Debug details written to {debug_path}"
        raise NoSolutionsError(f"No solutions found for waypoint. {debug_details}")
