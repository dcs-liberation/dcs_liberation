from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any, TypeVar, Generic

from shapely import Point, MultiPolygon
from shapely.geometry import shape

from game.data.doctrine import Doctrine, ALL_DOCTRINES
from game.flightplan.ipsolver import IpSolver
from game.flightplan.waypointsolver import WaypointSolver, NoSolutionsError
from game.flightplan.waypointsolverloader import WaypointSolverLoader
from game.theater.theaterloader import TERRAINS_BY_NAME

ReducerT = TypeVar("ReducerT")


def doctrine_from_name(name: str) -> Doctrine:
    for doctrine in ALL_DOCTRINES:
        if doctrine.name == name:
            return doctrine
    raise KeyError


class Reducer(Generic[ReducerT], Iterator[ReducerT], ABC):
    @abstractmethod
    def accept(self) -> None:
        ...

    @abstractmethod
    def reject(self) -> None:
        ...


class MultiPolyReducer(Reducer[MultiPolygon]):
    def __init__(self, multipoly: MultiPolygon) -> None:
        self._multipoly: MultiPolygon | None = multipoly
        self._previous_poly: MultiPolygon | None = None
        self._remove_index = 0

    def __next__(self) -> MultiPolygon:
        if self._multipoly is None:
            raise StopIteration
        return self._multipoly

    def _reduce_poly(self) -> None:
        assert self._multipoly is not None
        polys = list(self._multipoly.geoms)
        if not polys or self._remove_index >= len(polys):
            self._multipoly = None
            return

        del polys[self._remove_index]
        self._previous_poly = self._multipoly
        self._multipoly = MultiPolygon(polys)

    def accept(self) -> None:
        self._reduce_poly()

    def reject(self) -> None:
        self._multipoly = self._previous_poly
        self._previous_poly = None
        self._remove_index += 1
        self._reduce_poly()


class IpSolverReducer(Reducer[IpSolver]):
    def __init__(
        self,
        departure: Point,
        target: Point,
        doctrine: Doctrine,
        threat_zones: MultiPolygon,
    ) -> None:
        self.departure = departure
        self.target = target
        self.doctrine = doctrine
        self.threat_zones_reducer = MultiPolyReducer(threat_zones)

    @staticmethod
    def from_metadata_and_feature_collection(
        metadata: dict[str, Any], feature_collection: dict[str, Any]
    ) -> IpSolverReducer:
        departure: Point | None = None
        target: Point | None = None
        threat_zones: MultiPolygon | None = None
        for feature in feature_collection["features"]:
            description = feature["properties"]["description"]
            geometry = feature["geometry"]
            match description:
                case "departure":
                    departure = shape(geometry)
                case "target":
                    target = shape(geometry)
                case "threat_zones":
                    threat_zones = shape(geometry)

        if departure is None:
            raise KeyError("feature collection has no departure point")
        if target is None:
            raise KeyError("feature collection has no target point")
        if threat_zones is None:
            raise KeyError("feature collection has no threat zones")

        return IpSolverReducer(
            departure,
            target,
            doctrine_from_name(metadata["doctrine"]),
            threat_zones,
        )

    def __next__(self) -> IpSolver:
        return IpSolver(
            self.departure, self.target, self.doctrine, next(self.threat_zones_reducer)
        )

    def accept(self) -> None:
        self.threat_zones_reducer.accept()

    def reject(self) -> None:
        self.threat_zones_reducer.reject()


class WaypointSolverTestCaseReducer:
    def __init__(self, debug_directory: Path, out_dir: Path) -> None:
        self.debug_directory = debug_directory
        self.out_dir = out_dir
        if self.out_dir.exists():
            raise ValueError(f"out_dir {out_dir} already exists")

    @staticmethod
    def _reducer_from_solver(solver: WaypointSolver) -> Reducer[Any]:
        if isinstance(solver, IpSolver):
            return IpSolverReducer(
                solver.departure, solver.target, solver.doctrine, solver.threat_zones
            )
        else:
            raise KeyError(f"Unhandled waypoint solver {solver.__class__.__name__}")

    def reduce(self) -> None:
        loader = WaypointSolverLoader(self.debug_directory / "solver.json")
        solver = loader.load()
        last_broken: WaypointSolver | None = None
        reducer = self._reducer_from_solver(solver)
        for solver in reducer:
            try:
                solver.solve()
                reducer.reject()
            except NoSolutionsError:
                last_broken = solver
                reducer.accept()

        if last_broken is None:
            raise RuntimeError("all cases succeeded, nothing to reduce")

        self.out_dir.mkdir(parents=True)
        last_broken.set_debug_properties(
            self.out_dir, TERRAINS_BY_NAME[loader.load_data()["metadata"]["terrain"]]
        )
        last_broken.dump_debug_info()
