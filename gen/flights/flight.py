from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING

from dcs.mapping import Point
from dcs.point import MovingPoint, PointAction
from dcs.unittype import UnitType

from game import db
from theater.controlpoint import ControlPoint, MissionTarget

if TYPE_CHECKING:
    from gen.ato import Package
    from gen.flights.flightplan import FlightPlan


class FlightType(Enum):
    CAP = 0  # Do not use. Use BARCAP or TARCAP.
    TARCAP = 1
    BARCAP = 2
    CAS = 3
    INTERCEPTION = 4
    STRIKE = 5
    ANTISHIP = 6
    SEAD = 7
    DEAD = 8
    ESCORT = 9
    BAI = 10

    # Helos
    TROOP_TRANSPORT = 11
    LOGISTICS = 12
    EVAC = 13

    ELINT = 14
    RECON = 15
    EWAR = 16


class FlightWaypointType(Enum):
    TAKEOFF = 0             # Take off point
    ASCEND_POINT = 1        # Ascension point after take off
    PATROL = 2              # Patrol point
    PATROL_TRACK = 3        # Patrol race track
    NAV = 4                 # Nav point
    INGRESS_STRIKE = 5      # Ingress strike (For generator, means that this should have bombing on next TARGET_POINT points)
    INGRESS_SEAD = 6        # Ingress sead (For generator, means that this should attack groups on TARGET_GROUP_LOC points)
    INGRESS_CAS = 7         # Ingress cas (should start CAS task)
    CAS = 8                 # Should do CAS there
    EGRESS = 9              # Should stop attack
    DESCENT_POINT = 10       # Should start descending to pattern alt
    LANDING_POINT = 11      # Should land there
    TARGET_POINT = 12       # A target building or static object, position
    TARGET_GROUP_LOC = 13   # A target group approximate location
    TARGET_SHIP = 14        # A target ship known location
    CUSTOM = 15             # User waypoint (no specific behaviour)
    JOIN = 16
    SPLIT = 17
    LOITER = 18
    INGRESS_ESCORT = 19
    INGRESS_DEAD = 20


class FlightWaypoint:

    def __init__(self, waypoint_type: FlightWaypointType, x: float, y: float,
                 alt: int = 0) -> None:
        """Creates a flight waypoint.

        Args:
            waypoint_type: The waypoint type.
            x: X cooidinate of the waypoint.
            y: Y coordinate of the waypoint.
            alt: Altitude of the waypoint. By default this is AGL, but it can be
            changed to MSL by setting alt_type to "RADIO".
        """
        self.waypoint_type = waypoint_type
        self.x = x
        self.y = y
        self.alt = alt
        self.alt_type = "BARO"
        self.name = ""
        self.description = ""
        self.targets: List[MissionTarget] = []
        self.obj_name = ""
        self.pretty_name = ""
        self.only_for_player = False

        # These are set very late by the air conflict generator (part of mission
        # generation). We do it late so that we don't need to propagate changes
        # to waypoint times whenever the player alters the package TOT or the
        # flight's offset in the UI.
        self.tot: Optional[timedelta] = None
        self.departure_time: Optional[timedelta] = None

    @property
    def position(self) -> Point:
        return Point(self.x, self.y)

    @classmethod
    def from_pydcs(cls, point: MovingPoint,
                   from_cp: ControlPoint) -> "FlightWaypoint":
        waypoint = FlightWaypoint(FlightWaypointType.NAV, point.position.x,
                                  point.position.y, point.alt)
        waypoint.alt_type = point.alt_type
        # Other actions exist... but none of them *should* be the first
        # waypoint for a flight.
        waypoint.waypoint_type = {
            PointAction.TurningPoint: FlightWaypointType.NAV,
            PointAction.FlyOverPoint: FlightWaypointType.NAV,
            PointAction.FromParkingArea: FlightWaypointType.TAKEOFF,
            PointAction.FromParkingAreaHot: FlightWaypointType.TAKEOFF,
            PointAction.FromRunway: FlightWaypointType.TAKEOFF,
        }[point.action]
        if waypoint.waypoint_type == FlightWaypointType.NAV:
            waypoint.name = "NAV"
            waypoint.pretty_name = "Nav"
            waypoint.description = "Nav"
        else:
            waypoint.name = "TAKEOFF"
            waypoint.pretty_name = "Takeoff"
            waypoint.description = "Takeoff"
            waypoint.description = f"Takeoff from {from_cp.name}"
        return waypoint


class Flight:

    def __init__(self, package: Package, unit_type: UnitType, count: int,
                 from_cp: ControlPoint, flight_type: FlightType,
                 start_type: str) -> None:
        self.package = package
        self.unit_type = unit_type
        self.count = count
        self.from_cp = from_cp
        self.flight_type = flight_type
        # TODO: Replace with FlightPlan.
        self.targets: List[MissionTarget] = []
        self.loadout: Dict[str, str] = {}
        self.start_type = start_type
        self.use_custom_loadout = False
        self.client_count = 0

        # Will be replaced with a more appropriate FlightPlan by
        # FlightPlanBuilder, but an empty flight plan the flight begins with an
        # empty flight plan.
        from gen.flights.flightplan import CustomFlightPlan
        self.flight_plan: FlightPlan = CustomFlightPlan(
            package=package,
            flight=self,
            custom_waypoints=[]
        )

    @property
    def points(self) -> List[FlightWaypoint]:
        return self.flight_plan.waypoints[1:]

    def __repr__(self):
        return self.flight_type.name + " | " + str(self.count) + "x" + db.unit_type_name(self.unit_type) \
               + " (" + str(len(self.points)) + " wpt)"
