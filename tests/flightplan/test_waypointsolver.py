import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from dcs.terrain import Caucasus
from shapely.geometry import Point, MultiPolygon
from shapely.geometry.base import BaseGeometry

from game.flightplan.waypointsolver import WaypointSolver, NoSolutionsError
from game.flightplan.waypointstrategy import WaypointStrategy


class NoSolutionsStrategy(WaypointStrategy):
    def __init__(self) -> None:
        super().__init__(MultiPolygon([]))

    def find(self) -> Point | None:
        return None


class PointStrategy(WaypointStrategy):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(MultiPolygon([]))
        self.point = Point(x, y)

    def find(self) -> Point | None:
        return self.point


class OriginStrategy(PointStrategy):
    def __init__(self) -> None:
        super().__init__(0, 0)


class DebuggableStrategy(NoSolutionsStrategy):
    def __init__(self, distance_factor: int) -> None:
        super().__init__()
        center = Point(0, 0)
        self.exclude("foo", center.buffer(1 * distance_factor))
        self.exclude(
            "bar",
            center.buffer(3 * distance_factor).difference(
                center.buffer(2 * distance_factor)
            ),
        )


class SolverWithInputs(WaypointSolver):
    def describe_inputs(self) -> Iterator[tuple[str, BaseGeometry]]:
        yield "foo", Point(0, 0)
        yield "bar", Point(1, 1)


def test_solver_tries_strategies_in_order() -> None:
    solver = WaypointSolver()
    solver.add_strategy(OriginStrategy())
    solver.add_strategy(PointStrategy(1, 1))
    assert solver.solve() == Point(0, 0)


def test_individual_failed_strategies_do_not_fail_solver() -> None:
    solver = WaypointSolver()
    solver.add_strategy(NoSolutionsStrategy())
    solver.add_strategy(OriginStrategy())
    assert solver.solve() == Point(0, 0)


def test_no_solutions_raises() -> None:
    solver = WaypointSolver()
    solver.add_strategy(NoSolutionsStrategy())
    with pytest.raises(NoSolutionsError):
        solver.solve()


def test_no_strategies_raises() -> None:
    solver = WaypointSolver()
    with pytest.raises(ValueError):
        solver.solve()


def test_success_does_not_dump_debug_info(tmp_path: Path) -> None:
    solver = WaypointSolver()
    solver.set_debug_properties(tmp_path, Caucasus())
    solver.add_strategy(OriginStrategy())
    solver.solve()
    assert not list(tmp_path.iterdir())


def test_no_solutions_dumps_debug_info(tmp_path: Path) -> None:
    center = Point(0, 0)
    solver = WaypointSolver()
    solver.set_debug_properties(tmp_path, Caucasus())
    strategy_0 = DebuggableStrategy(distance_factor=1)
    strategy_1 = DebuggableStrategy(distance_factor=2)
    strategy_1.prerequisite(center).is_safe()
    solver.add_strategy(strategy_0)
    solver.add_strategy(strategy_1)
    with pytest.raises(NoSolutionsError):
        solver.solve()

    strategy_0_path = tmp_path / "0.json"
    strategy_1_path = tmp_path / "1.json"
    assert set(tmp_path.iterdir()) == {
        tmp_path / "solver.json",
        strategy_0_path,
        strategy_1_path,
    }

    with strategy_0_path.open("r", encoding="utf-8") as metadata_file:
        data = json.load(metadata_file)
    assert data["type"] == "FeatureCollection"
    assert data["metadata"]["name"] == "DebuggableStrategy"
    assert data["metadata"]["prerequisites"] == []
    assert len(data.keys()) == 3
    features = data["features"]
    assert len(features) == 2
    for debug_info, feature in zip(strategy_0.iter_debug_info(), features):
        assert debug_info.to_geojson(solver.to_geojson) == feature

    with strategy_1_path.open("r", encoding="utf-8") as metadata_file:
        data = json.load(metadata_file)
    assert data["type"] == "FeatureCollection"
    assert data["metadata"]["name"] == "DebuggableStrategy"
    assert data["metadata"]["prerequisites"] == [
        {
            "requirement": "is safe",
            "satisfied": True,
            "subject": solver.to_geojson(center),
        }
    ]
    assert len(data.keys()) == 3
    features = data["features"]
    assert len(features) == 2
    for debug_info, feature in zip(strategy_1.iter_debug_info(), features):
        assert debug_info.to_geojson(solver.to_geojson) == feature


def test_no_solutions_dumps_inputs(tmp_path: Path) -> None:
    solver = SolverWithInputs()
    solver.set_debug_properties(tmp_path, Caucasus())
    solver.add_strategy(NoSolutionsStrategy())
    with pytest.raises(NoSolutionsError):
        solver.solve()

    inputs_path = tmp_path / "solver.json"
    with inputs_path.open(encoding="utf-8") as inputs_file:
        data = json.load(inputs_file)
    assert data == {
        "type": "FeatureCollection",
        "metadata": {
            "name": "SolverWithInputs",
            "terrain": "Caucasus",
        },
        "features": [
            {
                "type": "Feature",
                "properties": {"description": "foo"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [34.265515188456, 45.129497060328966],
                },
            },
            {
                "type": "Feature",
                "properties": {"description": "bar"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [34.265528100962584, 45.1295059189547],
                },
            },
        ],
    }


def test_solver_inputs_appear_in_strategy_features(tmp_path: Path) -> None:
    solver = SolverWithInputs()
    solver.set_debug_properties(tmp_path, Caucasus())
    solver.add_strategy(PointStrategy(2, 2))
    solver.dump_debug_info()

    strategy_path = tmp_path / "0.json"
    with strategy_path.open(encoding="utf-8") as inputs_file:
        data = json.load(inputs_file)
    assert data == {
        "type": "FeatureCollection",
        "metadata": {
            "name": "PointStrategy",
            "prerequisites": [],
        },
        "features": [
            {
                "type": "Feature",
                "properties": {"description": "foo"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [34.265515188456, 45.129497060328966],
                },
            },
            {
                "type": "Feature",
                "properties": {"description": "bar"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [34.265528100962584, 45.1295059189547],
                },
            },
            {
                "type": "Feature",
                "properties": {"description": "solution"},
                "geometry": {
                    "coordinates": [34.265541013473154, 45.12951477757893],
                    "type": "Point",
                },
            },
        ],
    }


def test_to_geojson(tmp_path: Path) -> None:
    solver = WaypointSolver()
    solver.set_debug_properties(tmp_path, Caucasus())
    assert solver.to_geojson(Point(0, 0)) == {
        "coordinates": [34.265515188456, 45.129497060328966],
        "type": "Point",
    }

    assert solver.to_geojson(MultiPolygon([])) == {
        "type": "MultiPolygon",
        "coordinates": [],
    }
