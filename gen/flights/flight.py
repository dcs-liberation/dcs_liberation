from enum import Enum
from typing import List

from game import db
from dcs.unittype import UnitType
from dcs.point import MovingPoint, PointAction
from theater.controlpoint import ControlPoint


class FlightType(Enum):
    CAP = 0
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
        self.waypoint_type = waypoint_type
        self.x = x
        self.y = y
        self.alt = alt
        self.alt_type = "BARO"
        self.name = ""
        self.description = ""
        self.targets = []
        self.targetGroup = None
        self.obj_name = ""
        self.pretty_name = ""
        self.category: PredefinedWaypointCategory = PredefinedWaypointCategory.NOT_PREDEFINED
        self.only_for_player = False
        self.data = None


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
    unit_type: UnitType = None
    from_cp = None
    points: List[FlightWaypoint] = []
    flight_type: FlightType = None
    count: int = 0
    client_count: int = 0
    targets = []
    use_custom_loadout = False
    loadout = {}
    preset_loadout_name = ""
    start_type = "Runway"
    group = False # Contains DCS Mission group data after mission has been generated

    # How long before this flight should take off
    scheduled_in = 0

    def __init__(self, unit_type: UnitType, count: int, from_cp, flight_type: FlightType):
        self.unit_type = unit_type
        self.count = count
        self.from_cp = from_cp
        self.flight_type = flight_type
        self.points = []
        self.targets = []
        self.loadout = {}
        self.start_type = "Runway"

    def __repr__(self):
        return self.flight_type.name + " | " + str(self.count) + "x" + db.unit_type_name(self.unit_type) \
               + " in " + str(self.scheduled_in) + " minutes (" + str(len(self.points)) + " wpt)"


# Test
if __name__ == '__main__':
    from pydcs.dcs.planes import A_10C
    from theater import ControlPoint, Point, List

    from_cp = ControlPoint(0, "AA", Point(0, 0), None, [], 0, 0)
    f = Flight(A_10C(), 4, from_cp, FlightType.CAS)
    f.scheduled_in = 50
    print(f)
