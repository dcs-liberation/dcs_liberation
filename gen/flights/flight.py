from enum import Enum
from typing import Dict, Iterable, Optional

from game import db
from dcs.unittype import UnitType
from dcs.point import MovingPoint, PointAction
from theater.controlpoint import ControlPoint, MissionTarget


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


class PredefinedWaypointCategory(Enum):
    NOT_PREDEFINED = 0
    ALLY_CP = 1
    ENEMY_CP = 2
    FRONTLINE = 3
    ENEMY_BUILDING = 4
    ENEMY_UNIT = 5
    ALLY_BUILDING = 6
    ALLY_UNIT = 7


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
        self.targetGroup: Optional[MissionTarget] = None
        self.obj_name = ""
        self.pretty_name = ""
        self.category: PredefinedWaypointCategory = PredefinedWaypointCategory.NOT_PREDEFINED
        self.only_for_player = False
        self.data = None

        # These are set very late by the air conflict generator (part of mission
        # generation). We do it late so that we don't need to propagate changes
        # to waypoint times whenever the player alters the package TOT or the
        # flight's offset in the UI.
        self.tot: Optional[int] = None
        self.departure_time: Optional[int] = None

    @classmethod
    def from_pydcs(cls, point: MovingPoint,
                   from_cp: ControlPoint) -> "FlightWaypoint":
        waypoint = FlightWaypoint(point.position.x, point.position.y,
                                  point.alt)
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
    count: int = 0
    client_count: int = 0
    use_custom_loadout = False
    preset_loadout_name = ""
    group = False # Contains DCS Mission group data after mission has been generated

    def __init__(self, unit_type: UnitType, count: int, from_cp: ControlPoint,
                 flight_type: FlightType, start_type: str) -> None:
        self.unit_type = unit_type
        self.count = count
        self.from_cp = from_cp
        self.flight_type = flight_type
        self.points: List[FlightWaypoint] = []
        self.targets: List[MissionTarget] = []
        self.loadout: Dict[str, str] = {}
        self.start_type = start_type
        # Late activation delay in seconds from mission start. This is not
        # the same as the flight's takeoff time. Takeoff time depends on the
        # mission's TOT and the other flights in the package. Takeoff time is
        # determined by AirConflictGenerator.
        self.scheduled_in = 0

    def __repr__(self):
        return self.flight_type.name + " | " + str(self.count) + "x" + db.unit_type_name(self.unit_type) \
               + " (" + str(len(self.points)) + " wpt)"

    def waypoint_with_type(
            self,
            types: Iterable[FlightWaypointType]) -> Optional[FlightWaypoint]:
        for waypoint in self.points:
            if waypoint.waypoint_type in types:
                return waypoint
        return None


# Test
if __name__ == '__main__':
    from dcs.planes import A_10C
    from theater import ControlPoint, Point, List

    from_cp = ControlPoint(0, "AA", Point(0, 0), Point(0, 0), [], 0, 0)
    f = Flight(A_10C(), 4, from_cp, FlightType.CAS, "Cold")
    f.scheduled_in = 50
    print(f)
