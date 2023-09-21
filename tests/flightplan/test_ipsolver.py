import random
from pathlib import Path

import pytest
from dcs.terrain import Caucasus
from shapely import Point, MultiPolygon

from game.data.doctrine import ALL_DOCTRINES
from game.flightplan.ipsolver import IpSolver
from game.flightplan.waypointstrategy import point_at_heading
from game.utils import Heading, Distance
from .conftest import capture_fuzz_failures


@pytest.fixture(name="fuzzed_solver")
def fuzzed_solver_fixture(
    fuzzed_target_distance: Distance, fuzzed_threat_poly: MultiPolygon, tmp_path: Path
) -> IpSolver:
    target_heading = Heading.from_degrees(random.uniform(0, 360))
    departure = Point(0, 0)
    target = point_at_heading(departure, target_heading, fuzzed_target_distance)
    solver = IpSolver(
        departure, target, random.choice(ALL_DOCTRINES), fuzzed_threat_poly
    )
    solver.set_debug_properties(tmp_path, Caucasus())
    return solver


@pytest.mark.fuzztest
@pytest.mark.parametrize("run_number", range(500))
def test_fuzz_ipsolver(fuzzed_solver: IpSolver, run_number: int) -> None:
    with capture_fuzz_failures(fuzzed_solver):
        fuzzed_solver.solve()


def test_can_construct_solver_with_empty_threat() -> None:
    IpSolver(Point(0, 0), Point(0, 0), ALL_DOCTRINES[0], MultiPolygon([]))
