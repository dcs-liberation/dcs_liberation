import random
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from dcs.terrain import Caucasus
from shapely import Point, MultiPolygon, Polygon, unary_union

from game.data.doctrine import ALL_DOCTRINES
from game.flightplan.ipsolver import IpSolver
from game.flightplan.waypointsolver import NoSolutionsError
from game.flightplan.waypointstrategy import point_at_heading
from game.utils import Heading, nautical_miles, feet, Distance, meters
from tests.flightplan.waypointsolvertestcasereducer import WaypointSolverTestCaseReducer

# The Falklands is nearly 1000 nmi diagonal. We'll use that as a radius for a bit of
# overkill.
MAP_RADIUS = nautical_miles(1000)

# Aircraft like the B-1 have a combat range closer to 3000 nmi, but we don't have
# maps big enough for that to matter. 600 nmi is still a *very* distant target for
# our campaigns.
MAX_TARGET_DISTANCE = nautical_miles(500)

# 200 nmi is roughly the max range of the SA-5, which has the greatest range of
# anything in DCS.
MAX_THREAT_RANGE = nautical_miles(200)

MAX_THREAT_DISTANCE = MAX_TARGET_DISTANCE + MAX_THREAT_RANGE


THIS_DIR = Path(__file__).parent
TEST_CASE_DIRECTORY = THIS_DIR / "testcases"


def fuzz_threat() -> Polygon:
    threat_range_m = random.triangular(
        feet(500).meters, MAX_THREAT_RANGE.meters, nautical_miles(40).meters
    )
    threat_distance = meters(
        random.triangular(0, MAX_THREAT_DISTANCE.meters, nautical_miles(100).meters)
    )
    threat_position = point_at_heading(Point(0, 0), Heading.random(), threat_distance)
    return threat_position.buffer(threat_range_m)


@pytest.fixture(name="fuzzed_target_distance")
def fuzzed_target_distance_fixture() -> Distance:
    return meters(
        random.triangular(0, MAX_TARGET_DISTANCE.meters, nautical_miles(100).meters)
    )


@pytest.fixture(name="fuzzed_threat_poly")
def fuzzed_threat_poly_fixture() -> MultiPolygon:
    number_of_threats = random.randint(0, 100)
    polys = unary_union([fuzz_threat() for _ in range(number_of_threats)])
    if isinstance(polys, MultiPolygon):
        return polys
    return MultiPolygon([polys])


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


@contextmanager
def capture_fuzz_failures(solver: IpSolver) -> Iterator[None]:
    try:
        yield
    except NoSolutionsError as ex:
        test_case_directory = TEST_CASE_DIRECTORY / str(uuid.uuid4())
        assert solver.debug_output_directory
        WaypointSolverTestCaseReducer(
            solver.debug_output_directory, test_case_directory
        ).reduce()
        ex.add_note(f"Reduced test case was written to {test_case_directory}")
        raise


@pytest.mark.fuzztest
@pytest.mark.parametrize("run_number", range(500))
def test_fuzz_ipsolver(fuzzed_solver: IpSolver, run_number: int) -> None:
    with capture_fuzz_failures(fuzzed_solver):
        fuzzed_solver.solve()


def test_can_construct_solver_with_empty_threat() -> None:
    IpSolver(Point(0, 0), Point(0, 0), ALL_DOCTRINES[0], MultiPolygon([]))
