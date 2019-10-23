from enum import Enum
from typing import List

from dcs.mission import StartType
from dcs.unittype import UnitType

from game import db


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


class FlightWaypoint():

    def __init__(self, x: float, y: float, alt=0):
        self.x = x
        self.y = y
        self.alt = alt
        self.name = ""
        self.description = ""
        self.targets = []


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
    from dcs.planes import A_10C
    from theater import ControlPoint, Point, List

    from_cp = ControlPoint(0, "AA", Point(0, 0), None, [], 0, 0)
    f = Flight(A_10C, 4, from_cp, FlightType.CAS)
    f.scheduled_in = 50
    print(f)
