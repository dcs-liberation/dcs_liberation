import random
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pytest
from shapely import Polygon, Point, MultiPolygon, unary_union

from game.flightplan.waypointsolver import NoSolutionsError, WaypointSolver
from game.flightplan.waypointstrategy import point_at_heading
from game.utils import feet, nautical_miles, Heading, meters, Distance
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


@contextmanager
def capture_fuzz_failures(solver: WaypointSolver) -> Iterator[None]:
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
