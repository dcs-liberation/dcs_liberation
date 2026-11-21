import random
from pathlib import Path
from typing import cast, Self

import pytest
from dcs.mapping import Point as DcsPoint
from dcs.terrain import Caucasus
from shapely import Point, MultiPolygon

from game.coalition import Coalition
from game.data.doctrine import ALL_DOCTRINES, Doctrine
from game.flightplan import JoinZoneGeometry
from game.flightplan.holdpointsolver import HoldPointSolver
from game.flightplan.ipsolver import IpSolver
from game.flightplan.waypointstrategy import point_at_heading
from game.utils import Heading, Distance
from tests.flightplan.conftest import capture_fuzz_failures


class MockCoalition:
    def __init__(self, doctrine: Doctrine, threat_zone: MultiPolygon) -> None:
        self.doctrine = doctrine
        self._threat_zone = threat_zone

    @property
    def opponent(self) -> Self:
        return self

    @property
    def threat_zone(self) -> Self:
        return self

    @property
    def all(self) -> MultiPolygon:
        return self._threat_zone


@pytest.fixture(name="fuzzed_solver")
def fuzzed_solver_fixture(
    fuzzed_target_distance: Distance, fuzzed_threat_poly: MultiPolygon, tmp_path: Path
) -> HoldPointSolver:
    terrain = Caucasus()
    doctrine = random.choice(ALL_DOCTRINES)
    target_heading = Heading.from_degrees(random.uniform(0, 360))
    departure = Point(0, 0)
    target = point_at_heading(departure, target_heading, fuzzed_target_distance)
    ip = IpSolver(departure, target, doctrine, fuzzed_threat_poly).solve()
    join = JoinZoneGeometry(
        DcsPoint(target.x, target.y, terrain),
        DcsPoint(departure.x, departure.y, terrain),
        DcsPoint(ip.x, ip.y, terrain),
        cast(Coalition, MockCoalition(doctrine, fuzzed_threat_poly)),
    ).find_best_join_point()
    solver = HoldPointSolver(
        departure, target, ip, Point(join.x, join.y), doctrine, fuzzed_threat_poly
    )
    solver.set_debug_properties(tmp_path, terrain)
    return solver


@pytest.mark.fuzztest
@pytest.mark.parametrize("run_number", range(500))
def test_fuzz_holdpointsolver(fuzzed_solver: HoldPointSolver, run_number: int) -> None:
    with capture_fuzz_failures(fuzzed_solver):
        fuzzed_solver.solve()
