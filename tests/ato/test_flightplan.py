from typing import cast, Any

import pytest
from dcs import Point
from dcs.terrain import Caucasus

from game.ato import Flight, FlightWaypoint
from game.ato.flightplans.custom import CustomFlightPlan, CustomLayout
from game.ato.flightplans.flightplan import FlightPlan
from game.ato.flightwaypointtype import FlightWaypointType


@pytest.fixture(name="unescorted_flight_plan")
def unescorted_flight_plan_fixture() -> FlightPlan[Any]:
    point = Point(0, 0, Caucasus())
    departure = FlightWaypoint("", FlightWaypointType.TAKEOFF, point)

    waypoints = [
        FlightWaypoint(f"{i}", FlightWaypointType.NAV, point) for i in range(10)
    ]
    return CustomFlightPlan(cast(Flight, object()), CustomLayout(departure, waypoints))


@pytest.fixture(name="escorted_flight_plan")
def escorted_flight_plan_fixture() -> FlightPlan[Any]:
    point = Point(0, 0, Caucasus())
    departure = FlightWaypoint("", FlightWaypointType.TAKEOFF, point)

    waypoints = [
        FlightWaypoint(f"{i}", FlightWaypointType.NAV, point) for i in range(10)
    ]
    waypoints[1].wants_escort = True
    waypoints[2].wants_escort = True
    waypoints[3].wants_escort = True
    waypoints[5].wants_escort = True
    waypoints[7].wants_escort = True
    waypoints[8].wants_escort = True
    return CustomFlightPlan(cast(Flight, object()), CustomLayout(departure, waypoints))


def test_escorted_flight_plan_escorted_waypoints(
    escorted_flight_plan: FlightPlan[Any],
) -> None:
    assert [w.name for w in escorted_flight_plan.escorted_waypoints()] == [
        "1",
        "2",
        "3",
        "5",
        "7",
        "8",
    ]


def test_escorted_flight_plan_request_escort_at(
    escorted_flight_plan: FlightPlan[Any],
) -> None:
    wp = escorted_flight_plan.request_escort_at()
    assert wp is not None
    assert wp.name == "1"


def test_escorted_flight_plan_dismiss_escort_at(
    escorted_flight_plan: FlightPlan[Any],
) -> None:
    wp = escorted_flight_plan.dismiss_escort_at()
    assert wp is not None
    assert wp.name == "8"


def test_unescorted_flight_plan_escorted_waypoints(
    unescorted_flight_plan: FlightPlan[Any],
) -> None:
    assert not list(unescorted_flight_plan.escorted_waypoints())


def test_unescorted_flight_plan_request_escort_at(
    unescorted_flight_plan: FlightPlan[Any],
) -> None:
    assert unescorted_flight_plan.request_escort_at() is None


def test_unescorted_flight_plan_dismiss_escort_at(
    unescorted_flight_plan: FlightPlan[Any],
) -> None:
    assert unescorted_flight_plan.dismiss_escort_at() is None
