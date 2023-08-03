import json
from pathlib import Path

import pytest

from game.flightplan.ipsolver import IpSolver
from game.flightplan.waypointsolverloader import WaypointSolverLoader


def test_waypointsolverloader(tmp_path: Path) -> None:
    debug_info_path = tmp_path / "solver.json"
    debug_info_path.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "metadata": {
                    "name": "IpSolver",
                    "terrain": "Falklands",
                    "doctrine": "coldwar",
                },
                "features": [
                    {
                        "type": "Feature",
                        "properties": {"description": "departure"},
                        "geometry": {
                            "type": "Point",
                            "coordinates": [-59.17351849883801, -52.46892777233296],
                        },
                    },
                    {
                        "type": "Feature",
                        "properties": {"description": "target"},
                        "geometry": {
                            "type": "Point",
                            "coordinates": [-59.12970828579045, -52.51860490233211],
                        },
                    },
                    {
                        "type": "Feature",
                        "properties": {"description": "threat_zones"},
                        "geometry": {"type": "MultiPolygon", "coordinates": []},
                    },
                ],
            }
        )
    )
    solver = WaypointSolverLoader(debug_info_path).load()
    assert isinstance(solver, IpSolver)
    assert solver.doctrine.name == "coldwar"
    assert solver.threat_zones.is_empty
    assert solver.departure.x == pytest.approx(0, abs=1e-8)
    assert solver.departure.y == pytest.approx(0, abs=1e-8)
    assert solver.target.x == pytest.approx(-5436.058, abs=0.001)
    assert solver.target.y == pytest.approx(3138.51, abs=0.001)
