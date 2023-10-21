from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable, Union

from dcs import Mission
from dcs.planes import AJS37, F_14B, JF_17
from dcs.point import MovingPoint, PointAction
from dcs.unitgroup import FlyingGroup

from game.ato import Flight, FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.traveltime import GroundSpeed
from game.flightplan.waypointactions.taskcontext import TaskContext
from game.missiongenerator.missiondata import MissionData
from game.theater import MissionTarget, TheaterUnit
from game.unitmap import UnitMap

TARGET_WAYPOINTS = (
    FlightWaypointType.TARGET_GROUP_LOC,
    FlightWaypointType.TARGET_POINT,
    FlightWaypointType.TARGET_SHIP,
)


class PydcsWaypointBuilder:
    def __init__(
        self,
        waypoint: FlightWaypoint,
        group: FlyingGroup[Any],
        flight: Flight,
        mission: Mission,
        now: datetime,
        mission_data: MissionData,
        unit_map: UnitMap,
        generated_waypoint_idx: int,
    ) -> None:
        self.waypoint = waypoint
        self.group = group
        self.package = flight.package
        self.flight = flight
        self.mission = mission
        self.now = now
        self.mission_data = mission_data
        self.unit_map = unit_map
        self.generated_waypoint_idx = generated_waypoint_idx

    def dcs_name_for_waypoint(self) -> str:
        return self.waypoint.name

    def build(self) -> MovingPoint:
        waypoint = self.group.add_waypoint(
            self.waypoint.position,
            self.waypoint.alt.meters,
            # The speed we pass will be overridden for most waypoints because we'll set
            # a TOT and leave the speed up to the AI, but for the few types of waypoints
            # that don't have TOTs (e.g. nav points), we set a reasonable cruise speed
            # to pydcs doesn't assign the default of 600kph ground speed (which is very
            # slow at most altitudes).
            #
            # Calling GroundSpeed.for_flight isn't really a correct fix here. We ought
            # to be using FlightPlan.speed_between_waypoints, but the way the waypoint
            # builder is called makes it difficult to track the previous waypoint. This
            # is probably good enough for a stop gap, and most of the flight planning
            # code is hopefully being rewritten soon anyway.
            #
            # https://github.com/dcs-liberation/dcs_liberation/issues/3113
            speed=GroundSpeed.for_flight(self.flight, self.waypoint.alt).kph,
            name=self.dcs_name_for_waypoint(),
        )

        if self.waypoint.flyover:
            waypoint.action = PointAction.FlyOverPoint
            # It seems we need to leave waypoint.type exactly as it is even
            # though it's set to "Turning Point". If I set this to "Fly Over
            # Point" and then save the mission in the ME DCS resets it.
            if self.flight.client_count > 0:
                # Set Altitute to 0 AGL for player flights so that they can slave target pods or weapons to the waypoint
                waypoint.alt = 0
                waypoint.alt_type = "RADIO"

        waypoint.alt_type = self.waypoint.alt_type
        tot = self.flight.flight_plan.tot_for_waypoint(self.waypoint)
        if tot is not None:
            self.set_waypoint_tot(waypoint, tot, self.generated_waypoint_idx)
        self.add_tasks(waypoint)
        return waypoint

    def add_tasks(self, waypoint: MovingPoint) -> None:
        ctx = TaskContext(self.now)
        for action in self.waypoint.actions:
            for task in action.iter_tasks(ctx):
                waypoint.add_task(task)
        for option in self.waypoint.options.values():
            for task in option.iter_tasks(ctx):
                waypoint.add_task(task)

    def set_waypoint_tot(
        self, waypoint: MovingPoint, tot: datetime, waypoint_index: int
    ) -> None:
        self.waypoint.tot = tot
        if not self._viggen_client_tot():
            waypoint.ETA = int((tot - self.now).total_seconds())
            waypoint.ETA_locked = True
            # The first waypoint must always have a locked speed (see the bug). Other
            # waypoints cannot lock both a speed and an ETA, so we need to clear the
            # speed lock when setting a TOT.
            # https://github.com/dcs-liberation/dcs_liberation/issues/3195
            waypoint.speed_locked = waypoint_index == 0

    def _viggen_client_tot(self) -> bool:
        """Viggen player aircraft consider any waypoint with a TOT set to be a target ("M") waypoint.
        If the flight is a player controlled Viggen flight, no TOT should be set on any waypoint except actual target waypoints.
        """
        if (
            self.flight.client_count > 0
            and self.flight.unit_type.dcs_unit_type == AJS37
        ) and (self.waypoint.waypoint_type not in TARGET_WAYPOINTS):
            return True
        else:
            return False

    def register_special_waypoints(
        self, targets: Iterable[Union[MissionTarget, TheaterUnit]]
    ) -> None:
        """Create special target waypoints for various aircraft"""
        for i, t in enumerate(targets):
            if self.group.units[0].unit_type == JF_17 and i < 4:
                self.group.add_nav_target_point(t.position, "PP" + str(i + 1))
            if self.group.units[0].unit_type == F_14B and i == 0:
                self.group.add_nav_target_point(t.position, "ST")
