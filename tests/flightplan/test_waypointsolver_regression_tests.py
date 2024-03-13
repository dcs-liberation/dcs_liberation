from pathlib import Path

import pytest

from game.flightplan.waypointsolverloader import WaypointSolverLoader

THIS_DIR = Path(__file__).parent
TEST_CASES_DIR = THIS_DIR / "testcases"

# Set to True to regenerate the debug files for each test case. After doing this, format
# the test cases with `npx prettier -w tests/flightplan/testcases` for readability.
UPDATE_TEST_CASES = False


@pytest.mark.parametrize("test_case", TEST_CASES_DIR.glob("**/solver.json"))
def test_waypoint_solver_regression_tests(test_case: Path) -> None:
    loader = WaypointSolverLoader(test_case)
    solver = loader.load()
    if UPDATE_TEST_CASES:
        solver.set_debug_properties(test_case.parent, loader.terrain)
    solver.solve()
    if UPDATE_TEST_CASES:
        solver.dump_debug_info()
