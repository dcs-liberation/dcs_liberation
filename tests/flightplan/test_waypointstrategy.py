from __future__ import annotations

from pathlib import Path

import pytest
from pytest import approx
from shapely.geometry import Point, MultiPolygon

from game.flightplan.waypointstrategy import WaypointStrategy, angle_between_points
from game.utils import meters, Heading


def test_safe_prerequisite_safe_point() -> None:
    strategy = WaypointStrategy(MultiPolygon([]))
    strategy.prerequisite(Point(0, 0)).is_safe()
    assert strategy.prerequisites_are_satisfied()


def test_safe_prerequisite_unsafe_point() -> None:
    strategy = WaypointStrategy(MultiPolygon([Point(0, 0).buffer(1)]))
    strategy.prerequisite(Point(0, 0)).is_safe()
    assert not strategy.prerequisites_are_satisfied()


def test_no_solution_if_prerequisites_failed() -> None:
    """Verify that no solution is found if prerequisites are not satisfied.

    This test has a 1-meter radius threat zone about the center of the plane. It has a
    prerequisite for a safe center, which will fail. The test verifies that even if
    there are no .require() constraints that would prevent finding a solution, failed
    prerequisites still prevent it (prerequisites differ from constraints in that they
    will prevent any of the other operations from happening without needing to location
    constraints, which is important because it allows strategies to avoid defending
    against invalid cases).
    """
    strategy = WaypointStrategy(MultiPolygon([Point(0, 0).buffer(1)]))
    strategy.prerequisite(Point(0, 0)).is_safe()
    # This constraint won't actually apply, but it's required before calling find() so
    # we need to set it even though it's not actually relevant to the test.
    strategy.nearest(Point(0, 0))
    assert strategy.find() is None


def test_has_solution_if_prerequisites_satisfied() -> None:
    strategy = WaypointStrategy(MultiPolygon([]))
    strategy.prerequisite(Point(0, 0)).is_safe()
    strategy.nearest(Point(0, 0))
    assert strategy.find() is not None


def test_require_nearest() -> None:
    strategy = WaypointStrategy(MultiPolygon([]))
    center = Point(0, 0)
    strategy.nearest(center)
    assert strategy.find() == center


def test_find_without_nearest_raises() -> None:
    with pytest.raises(RuntimeError):
        WaypointStrategy(MultiPolygon([])).find()


def test_multiple_nearest_raises() -> None:
    strategy = WaypointStrategy(MultiPolygon([]))
    strategy.nearest(Point(0, 0))
    with pytest.raises(RuntimeError):
        strategy.nearest(Point(0, 0))


def test_require_at_least() -> None:
    strategy = WaypointStrategy(MultiPolygon([]))
    center = Point(0, 0)
    strategy.require().at_least(meters(10)).away_from(center)
    strategy.nearest(center)
    solution = strategy.find()
    assert solution is not None
    assert solution.distance(center) == approx(10, 0.1)


def test_require_at_most() -> None:
    strategy = WaypointStrategy(MultiPolygon([]))
    center = Point(0, 0)
    strategy.require().at_most(meters(1)).away_from(center)
    strategy.nearest(Point(10, 0))
    solution = strategy.find()
    assert solution is not None
    assert solution.distance(center) <= 1


def test_require_safe() -> None:
    threat = MultiPolygon([Point(0, 0).buffer(10)])
    strategy = WaypointStrategy(threat)
    strategy.require().safe()
    strategy.nearest(Point(0, 0))
    solution = strategy.find()
    assert solution is not None
    assert not solution.intersects(threat)


def test_require_maximum_turn_to() -> None:
    strategy = WaypointStrategy(MultiPolygon([]))
    turn_point = Point(1, 0)
    turn_target = Point(0, 0)
    strategy.require().maximum_turn_to(turn_point, turn_target, Heading(90))
    strategy.nearest(Point(0, 1))
    pre_turn_heading = Heading.from_degrees(
        angle_between_points(strategy.find(), turn_point)
    )
    post_turn_heading = Heading.from_degrees(
        angle_between_points(turn_point, turn_target)
    )
    assert pre_turn_heading.angle_between(post_turn_heading) <= Heading(90)


def test_combined_constraints() -> None:
    strategy = WaypointStrategy(MultiPolygon([]))
    center = Point(0, 0)
    offset = Point(1, 0)
    midpoint = Point(0.5, 0)
    strategy.require().at_least(meters(1)).away_from(center)
    strategy.require().at_least(meters(1)).away_from(offset)
    strategy.nearest(midpoint)
    solution = strategy.find()
    assert solution is not None
    assert solution.distance(center) == approx(1, rel=0.1, abs=0.1)
    assert solution.distance(offset) == approx(1, rel=0.1, abs=0.1)
    assert solution.distance(midpoint) < 1


def test_threat_tolerance(tmp_path: Path) -> None:
    home = Point(20, 0)
    target = Point(-1, 0)
    max_distance = meters(5)
    threat = MultiPolygon([Point(0, 0).buffer(10)])
    strategy = WaypointStrategy(threat)
    strategy.require().at_most(max_distance).away_from(target)
    strategy.threat_tolerance(target, max_distance, meters(1))
    strategy.require().safe()
    strategy.nearest(home)
    solution = strategy.find()
    assert solution is not None
    # Max distance of 5 from -1, so the point should be at 4. Home is at 20.
    assert solution.distance(home) == 16


def test_threat_tolerance_does_nothing_if_no_threats(tmp_path: Path) -> None:
    strategy = WaypointStrategy(MultiPolygon([]))
    strategy.threat_tolerance(Point(0, 0), meters(1), meters(1))
    assert strategy._threat_tolerance is None


def test_no_solutions() -> None:
    strategy = WaypointStrategy(MultiPolygon([]))
    strategy.require().at_most(meters(1)).away_from(Point(0, 0))
    strategy.require().at_least(meters(2)).away_from(Point(0, 0))
    strategy.nearest(Point(0, 0))
    assert strategy.find() is None


def test_debug() -> None:
    center = Point(0, 0)
    threat = MultiPolygon([center.buffer(5)])
    strategy = WaypointStrategy(threat)
    strategy.require().at_most(meters(10)).away_from(center, "center")
    strategy.require().at_least(meters(2)).away_from(center)
    strategy.require().safe()
    strategy.nearest(center)
    solution = strategy.find()
    assert solution is not None
    debug_info = list(strategy.iter_debug_info())
    assert len(debug_info) == 4
    max_distance_debug, min_distance_debug, safe_debug, solution_debug = debug_info
    assert max_distance_debug.description == "at most 10 meters away from center"
    assert max_distance_debug.geometry.distance(center) == approx(10, 0.1)
    assert min_distance_debug.description == "at least 2 meters away from POINT (0 0)"
    assert max_distance_debug.geometry.boundary.distance(center) == approx(10, 0.1)
    assert safe_debug.description == "safe"
    assert safe_debug.geometry == threat
    assert solution_debug.description == "solution"
    assert solution_debug.geometry == solution


def test_debug_info_omits_solution_if_none() -> None:
    center = Point(0, 0)
    strategy = WaypointStrategy(MultiPolygon([]))
    strategy.require().at_most(meters(1)).away_from(center)
    strategy.require().at_least(meters(2)).away_from(center)
    strategy.nearest(center)
    debug_infos = list(strategy.iter_debug_info())
    assert len(debug_infos) == 2
