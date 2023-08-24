import pytest
from dcs import Point
from dcs.terrain import Terrain, Caucasus

from game.ato import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.dcs.aircrafttype import FuelConsumption
from game.missiongenerator.aircraft.bingoestimator import BingoEstimator
from game.utils import nautical_miles


@pytest.fixture(name="terrain")
def terrain_fixture() -> Terrain:
    return Caucasus()


@pytest.fixture(name="waypoints")
def waypoints_fixture(terrain: Terrain) -> list[FlightWaypoint]:
    return [
        FlightWaypoint(
            "", FlightWaypointType.NAV, Point(0, nautical_miles(d).meters, terrain)
        )
        for d in range(101)
    ]


def test_legacy_bingo_estimator(
    waypoints: list[FlightWaypoint], terrain: Terrain
) -> None:
    estimator = BingoEstimator(None, Point(0, 0, terrain), None, waypoints)
    assert estimator.estimate_bingo() == 3000
    assert estimator.estimate_joker() == estimator.estimate_bingo() + 1000
    estimator = BingoEstimator(
        None, Point(0, 0, terrain), Point(0, 5, terrain), waypoints
    )
    assert estimator.estimate_bingo() == 4000
    assert estimator.estimate_joker() == estimator.estimate_bingo() + 1000


def test_fuel_consumption_based_bingo_estimator(
    waypoints: list[FlightWaypoint], terrain: Terrain
) -> None:
    consumption = FuelConsumption(100, 50, 10, 25, 1000)
    estimator = BingoEstimator(consumption, Point(0, 0, terrain), None, waypoints)
    assert estimator.estimate_bingo() == 2000
    assert estimator.estimate_joker() == estimator.estimate_bingo() + 1000
    estimator = BingoEstimator(
        consumption, Point(0, 0, terrain), Point(0, 5, terrain), waypoints
    )
    assert estimator.estimate_bingo() == 2000
    assert estimator.estimate_joker() == estimator.estimate_bingo() + 1000
