from __future__ import annotations

from datetime import timedelta

from pydantic import BaseModel

from game.ato import Flight, FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.server.leaflet import LeafletPoint


def timing_info(flight: Flight, waypoint_idx: int) -> str:
    if waypoint_idx == 0:
        return f"Depart T+{flight.flight_plan.takeoff_time()}"

    waypoint = flight.flight_plan.waypoints[waypoint_idx - 1]
    prefix = "TOT"
    time = flight.flight_plan.tot_for_waypoint(waypoint)
    if time is None:
        prefix = "Depart"
        time = flight.flight_plan.depart_time_for_waypoint(waypoint)
    if time is None:
        return ""
    return f"{prefix} T+{timedelta(seconds=int(time.total_seconds()))}"


class FlightWaypointJs(BaseModel):
    name: str
    position: LeafletPoint
    altitude_ft: float
    altitude_reference: str
    is_movable: bool
    should_mark: bool
    include_in_path: bool
    timing: str

    class Config:
        title = "Waypoint"

    @staticmethod
    def for_waypoint(
        waypoint: FlightWaypoint, flight: Flight, waypoint_idx: int
    ) -> FlightWaypointJs:
        # Target *points* are the exact location of a unit, whereas the target area is
        # only the center of the objective. Allow moving the latter since its exact
        # location isn't very important.
        #
        # Landing, and divert should be changed in the flight settings UI, takeoff
        # cannot be changed because that's where the plane is.
        #
        # Moving the bullseye reference only makes it wrong.
        is_movable = waypoint.waypoint_type not in {
            FlightWaypointType.BULLSEYE,
            FlightWaypointType.DIVERT,
            FlightWaypointType.LANDING_POINT,
            FlightWaypointType.TAKEOFF,
            FlightWaypointType.TARGET_POINT,
        }

        # We don't need a marker for the departure waypoint (and it's likely
        # coincident with the landing waypoint, so hard to see). We do want to draw
        # the path from it though.
        #
        # We also don't need the landing waypoint since we'll be drawing that path
        # as well, and it's clear what it is, and only obscured the CP icon.
        #
        # The divert waypoint also obscures the CP. We don't draw the path to it,
        # but it can be seen in the flight settings page, so it's not really a
        # problem to exclude it.
        #
        # Bullseye ought to be (but currently isn't) drawn *once* rather than as a
        # flight waypoint.
        should_mark = waypoint.waypoint_type not in {
            FlightWaypointType.BULLSEYE,
            FlightWaypointType.DIVERT,
            FlightWaypointType.LANDING_POINT,
            FlightWaypointType.TAKEOFF,
        }

        include_in_path = waypoint.waypoint_type not in {
            FlightWaypointType.BULLSEYE,
            FlightWaypointType.DIVERT,
        }

        return FlightWaypointJs(
            name=waypoint.name,
            position=waypoint.position.latlng(),
            altitude_ft=waypoint.alt.feet,
            altitude_reference=waypoint.alt_type,
            is_movable=is_movable,
            should_mark=should_mark,
            include_in_path=include_in_path,
            timing=timing_info(flight, waypoint_idx),
        )
