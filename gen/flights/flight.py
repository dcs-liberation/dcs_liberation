from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import List, Optional, TYPE_CHECKING, Union, Sequence

from dcs.mapping import Point
from dcs.point import MovingPoint, PointAction
from dcs.unit import Unit

from game.dcs.aircrafttype import AircraftType
from game.theater.controlpoint import ControlPoint, MissionTarget
from game.utils import Distance, meters
from gen.flights.loadouts import Loadout

if TYPE_CHECKING:
    from game.squadrons import Pilot, Squadron
    from game.transfers import TransferOrder
    from gen.ato import Package
    from gen.flights.flightplan import FlightPlan


class FlightType(Enum):
    """Enumeration of mission types.

    The value of each enumeration is the name that will be shown in the UI.

    These values are persisted to the save game as well since they are a part of
    each flight and thus a part of the ATO, so changing these values will break
    save compat.

    When adding new mission types to this list, you will also need to update:

    * flightplan.py: Add waypoint population in generate_flight_plan. Add a new flight
      plan type if necessary, though most are a subclass of StrikeFlightPlan.
    * aircraft.py: Add a configuration method and call it in setup_flight_group. This is
      responsible for configuring waypoint 0 actions like setting ROE, threat reaction,
      and mission abort parameters (winchester, bingo, etc).
    * Implementations of MissionTarget.mission_types: A mission type can only be planned
      against compatible targets. The mission_types method of each target class defines
      which missions may target it.
    * ai_flight_planner_db.py: Add the new mission type to aircraft_for_task that
      returns the list of compatible aircraft in order of preference.

    You may also need to update:

    * flight.py: Add a new waypoint type if necessary. Most mission types will need
      these, as aircraft.py uses the ingress point type to specialize AI tasks, and non-
      strike-like missions will need more specialized control.
    * ai_flight_planner.py: Use the new mission type in propose_missions so the AI will
      plan the new mission type.
    * FlightType.is_air_to_air and FlightType.is_air_to_ground: If the new mission type
      fits either of these categories, update those methods accordingly.
    """

    TARCAP = "TARCAP"
    BARCAP = "BARCAP"
    CAS = "CAS"
    INTERCEPTION = "Intercept"
    STRIKE = "Strike"
    ANTISHIP = "Anti-ship"
    SEAD = "SEAD"
    DEAD = "DEAD"
    ESCORT = "Escort"
    BAI = "BAI"
    SWEEP = "Fighter sweep"
    OCA_RUNWAY = "OCA/Runway"
    OCA_AIRCRAFT = "OCA/Aircraft"
    AEWC = "AEW&C"
    TRANSPORT = "Transport"
    SEAD_ESCORT = "SEAD Escort"
    REFUELING = "Refueling"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_name(cls, name: str) -> FlightType:
        for entry in cls:
            if name == entry.value:
                return entry
        raise KeyError(f"No FlightType with name {name}")

    @property
    def is_air_to_air(self) -> bool:
        return self in {
            FlightType.TARCAP,
            FlightType.BARCAP,
            FlightType.INTERCEPTION,
            FlightType.ESCORT,
            FlightType.SWEEP,
        }

    @property
    def is_air_to_ground(self) -> bool:
        return self in {
            FlightType.CAS,
            FlightType.STRIKE,
            FlightType.ANTISHIP,
            FlightType.SEAD,
            FlightType.DEAD,
            FlightType.BAI,
            FlightType.OCA_RUNWAY,
            FlightType.OCA_AIRCRAFT,
            FlightType.SEAD_ESCORT,
        }


class FlightWaypointType(Enum):
    """Enumeration of waypoint types.

    The value of the enum has no meaning but should remain stable to prevent breaking
    save game compatibility.

    When adding a new waypoint type, you will also need to update:

    * waypointbuilder.py: Add a builder to simplify construction of the new waypoint
      type unless the new waypoint type will be a parameter to an existing builder
      method (such as how escort ingress waypoints work).
    * aircraft.py: Associate AI actions with the new waypoint type by subclassing
      PydcsWaypointBuilder and using it in PydcsWaypointBuilder.for_waypoint.
    """

    TAKEOFF = 0  # Take off point
    ASCEND_POINT = 1  # Ascension point after take off
    PATROL = 2  # Patrol point
    PATROL_TRACK = 3  # Patrol race track
    NAV = 4  # Nav point
    INGRESS_STRIKE = 5  # Ingress strike (For generator, means that this should have bombing on next TARGET_POINT points)
    INGRESS_SEAD = 6  # Ingress sead (For generator, means that this should attack groups on TARGET_GROUP_LOC points)
    INGRESS_CAS = 7  # Ingress cas (should start CAS task)
    CAS = 8  # Should do CAS there
    EGRESS = 9  # Should stop attack
    DESCENT_POINT = 10  # Should start descending to pattern alt
    LANDING_POINT = 11  # Should land there
    TARGET_POINT = 12  # A target building or static object, position
    TARGET_GROUP_LOC = 13  # A target group approximate location
    TARGET_SHIP = 14  # Unused.
    CUSTOM = 15  # User waypoint (no specific behaviour)
    JOIN = 16
    SPLIT = 17
    LOITER = 18
    INGRESS_ESCORT = 19
    INGRESS_DEAD = 20
    INGRESS_SWEEP = 21
    INGRESS_BAI = 22
    DIVERT = 23
    INGRESS_OCA_RUNWAY = 24
    INGRESS_OCA_AIRCRAFT = 25
    PICKUP = 26
    DROP_OFF = 27
    BULLSEYE = 28


class FlightWaypoint:
    def __init__(
        self,
        waypoint_type: FlightWaypointType,
        x: float,
        y: float,
        alt: Distance = meters(0),
    ) -> None:
        """Creates a flight waypoint.

        Args:
            waypoint_type: The waypoint type.
            x: X coordinate of the waypoint.
            y: Y coordinate of the waypoint.
            alt: Altitude of the waypoint. By default this is MSL, but it can be
            changed to AGL by setting alt_type to "RADIO"
        """
        self.waypoint_type = waypoint_type
        self.x = x
        self.y = y
        self.alt = alt
        self.alt_type = "BARO"
        self.name = ""
        # TODO: Merge with pretty_name.
        # Only used in the waypoint list in the flight edit page. No sense
        # having three names. A short and long form is enough.
        self.description = ""
        self.targets: Sequence[Union[MissionTarget, Unit]] = []
        self.obj_name = ""
        self.pretty_name = ""
        self.only_for_player = False
        self.flyover = False
        # The minimum amount of fuel remaining at this waypoint in pounds.
        self.min_fuel: Optional[float] = None

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
    def from_pydcs(cls, point: MovingPoint, from_cp: ControlPoint) -> "FlightWaypoint":
        waypoint = FlightWaypoint(
            FlightWaypointType.NAV,
            point.position.x,
            point.position.y,
            meters(point.alt),
        )
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


class FlightRoster:
    def __init__(self, squadron: Squadron, initial_size: int = 0) -> None:
        self.squadron = squadron
        self.pilots: list[Optional[Pilot]] = []
        self.resize(initial_size)

    @property
    def max_size(self) -> int:
        return len(self.pilots)

    @property
    def player_count(self) -> int:
        return len([p for p in self.pilots if p is not None and p.player])

    @property
    def missing_pilots(self) -> int:
        return len([p for p in self.pilots if p is None])

    def resize(self, new_size: int) -> None:
        if self.max_size > new_size:
            self.squadron.return_pilots(
                [p for p in self.pilots[new_size:] if p is not None]
            )
            self.pilots = self.pilots[:new_size]
            return
        self.pilots.extend(
            [
                self.squadron.claim_available_pilot()
                for _ in range(new_size - self.max_size)
            ]
        )

    def set_pilot(self, index: int, pilot: Optional[Pilot]) -> None:
        if pilot is not None:
            self.squadron.claim_pilot(pilot)
        if (current_pilot := self.pilots[index]) is not None:
            self.squadron.return_pilot(current_pilot)
        self.pilots[index] = pilot

    def clear(self) -> None:
        self.squadron.return_pilots([p for p in self.pilots if p is not None])


class Flight:
    def __init__(
        self,
        package: Package,
        country: str,
        squadron: Squadron,
        count: int,
        flight_type: FlightType,
        start_type: str,
        departure: ControlPoint,
        arrival: ControlPoint,
        divert: Optional[ControlPoint],
        custom_name: Optional[str] = None,
        cargo: Optional[TransferOrder] = None,
        roster: Optional[FlightRoster] = None,
    ) -> None:
        self.package = package
        self.country = country
        self.squadron = squadron
        if roster is None:
            self.roster = FlightRoster(self.squadron, initial_size=count)
        else:
            self.roster = roster
        self.departure = departure
        self.arrival = arrival
        self.divert = divert
        self.flight_type = flight_type
        # TODO: Replace with FlightPlan.
        self.targets: List[MissionTarget] = []
        self.loadout = Loadout.default_for(self)
        self.start_type = start_type
        self.use_custom_loadout = False
        self.custom_name = custom_name

        # Only used by transport missions.
        self.cargo = cargo

        # Will be replaced with a more appropriate FlightPlan by
        # FlightPlanBuilder, but an empty flight plan the flight begins with an
        # empty flight plan.
        from gen.flights.flightplan import CustomFlightPlan

        self.flight_plan: FlightPlan = CustomFlightPlan(
            package=package, flight=self, custom_waypoints=[]
        )

    @property
    def count(self) -> int:
        return self.roster.max_size

    @property
    def client_count(self) -> int:
        return self.roster.player_count

    @property
    def unit_type(self) -> AircraftType:
        return self.squadron.aircraft

    @property
    def from_cp(self) -> ControlPoint:
        return self.departure

    @property
    def points(self) -> List[FlightWaypoint]:
        return self.flight_plan.waypoints[1:]

    def resize(self, new_size: int) -> None:
        self.roster.resize(new_size)

    def set_pilot(self, index: int, pilot: Optional[Pilot]) -> None:
        self.roster.set_pilot(index, pilot)

    @property
    def missing_pilots(self) -> int:
        return self.roster.missing_pilots

    def clear_roster(self) -> None:
        self.roster.clear()

    def __repr__(self) -> str:
        if self.custom_name:
            return f"{self.custom_name} {self.count} x {self.unit_type}"
        return f"[{self.flight_type}] {self.count} x {self.unit_type}"

    def __str__(self) -> str:
        if self.custom_name:
            return f"{self.custom_name} {self.count} x {self.unit_type}"
        return f"[{self.flight_type}] {self.count} x {self.unit_type}"
