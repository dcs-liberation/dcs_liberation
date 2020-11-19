from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from dcs.mapping import Point
from dcs.unit import Unit
from dcs.unitgroup import VehicleGroup

from game.data.doctrine import Doctrine
from game.utils import nm_to_meter
from game.weather import Conditions
from theater import ControlPoint, MissionTarget, TheaterGroundObject
from .flight import Flight, FlightWaypoint, FlightWaypointType
from ..runways import RunwayAssigner


@dataclass(frozen=True)
class StrikeTarget:
    name: str
    target: Union[VehicleGroup, TheaterGroundObject, Unit]


class WaypointBuilder:
    def __init__(self, conditions: Conditions, flight: Flight,
                 doctrine: Doctrine,
                 targets: Optional[List[StrikeTarget]] = None) -> None:
        self.conditions = conditions
        self.flight = flight
        self.doctrine = doctrine
        self.targets = targets

    @property
    def is_helo(self) -> bool:
        return getattr(self.flight.unit_type, "helicopter", False)

    @staticmethod
    def takeoff(departure: ControlPoint) -> FlightWaypoint:
        """Create takeoff waypoint for the given arrival airfield or carrier.

        Note that the takeoff waypoint will automatically be created by pydcs
        when we create the group, but creating our own before generation makes
        the planning code simpler.

        Args:
            departure: Departure airfield or carrier.
        """
        position = departure.position
        waypoint = FlightWaypoint(
            FlightWaypointType.TAKEOFF,
            position.x,
            position.y,
            0
        )
        waypoint.name = "TAKEOFF"
        waypoint.alt_type = "RADIO"
        waypoint.description = "Takeoff"
        waypoint.pretty_name = "Takeoff"
        return waypoint

    @staticmethod
    def land(arrival: ControlPoint) -> FlightWaypoint:
        """Create descent waypoint for the given arrival airfield or carrier.

        Args:
            arrival: Arrival airfield or carrier.
        """
        position = arrival.position
        waypoint = FlightWaypoint(
            FlightWaypointType.LANDING_POINT,
            position.x,
            position.y,
            0
        )
        waypoint.name = "LANDING"
        waypoint.alt_type = "RADIO"
        waypoint.description = "Land"
        waypoint.pretty_name = "Land"
        return waypoint

    def hold(self, position: Point) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.LOITER,
            position.x,
            position.y,
            500 if self.is_helo else self.doctrine.rendezvous_altitude
        )
        waypoint.pretty_name = "Hold"
        waypoint.description = "Wait until push time"
        waypoint.name = "HOLD"
        return waypoint

    def join(self, position: Point) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.JOIN,
            position.x,
            position.y,
            500 if self.is_helo else self.doctrine.ingress_altitude
        )
        waypoint.pretty_name = "Join"
        waypoint.description = "Rendezvous with package"
        waypoint.name = "JOIN"
        return waypoint

    def split(self, position: Point) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.SPLIT,
            position.x,
            position.y,
            500 if self.is_helo else self.doctrine.ingress_altitude
        )
        waypoint.pretty_name = "Split"
        waypoint.description = "Depart from package"
        waypoint.name = "SPLIT"
        return waypoint

    def ingress_cas(self, position: Point,
                    objective: MissionTarget) -> FlightWaypoint:
        return self._ingress(FlightWaypointType.INGRESS_CAS, position,
                             objective)

    def ingress_escort(self, position: Point,
                       objective: MissionTarget) -> FlightWaypoint:
        return self._ingress(FlightWaypointType.INGRESS_ESCORT, position,
                             objective)

    def ingress_bai(self, position: Point,
                    objective: MissionTarget) -> FlightWaypoint:
        return self._ingress(FlightWaypointType.INGRESS_BAI, position,
                             objective)
    
    def ingress_dead(self, position:Point,
                     objective: MissionTarget) -> FlightWaypoint:
        return self._ingress(FlightWaypointType.INGRESS_DEAD, position,
                             objective)

    def ingress_sead(self, position: Point,
                     objective: MissionTarget) -> FlightWaypoint:
        return self._ingress(FlightWaypointType.INGRESS_SEAD, position,
                             objective)

    def ingress_strike(self, position: Point,
                       objective: MissionTarget) -> FlightWaypoint:
        return self._ingress(FlightWaypointType.INGRESS_STRIKE, position,
                             objective)

    def _ingress(self, ingress_type: FlightWaypointType, position: Point,
                 objective: MissionTarget) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            ingress_type,
            position.x,
            position.y,
            500 if self.is_helo else self.doctrine.ingress_altitude
        )
        waypoint.pretty_name = "INGRESS on " + objective.name
        waypoint.description = "INGRESS on " + objective.name
        waypoint.name = "INGRESS"
        # TODO: This seems wrong, but it's what was there before.
        waypoint.targets.append(objective)
        return waypoint

    def egress(self, position: Point, target: MissionTarget) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.EGRESS,
            position.x,
            position.y,
            500 if self.is_helo else self.doctrine.ingress_altitude
        )
        waypoint.pretty_name = "EGRESS from " + target.name
        waypoint.description = "EGRESS from " + target.name
        waypoint.name = "EGRESS"
        return waypoint

    def bai_group(self, target: StrikeTarget) -> FlightWaypoint:
        return self._target_point(target, f"ATTACK {target.name}")

    def dead_point(self, target: StrikeTarget) -> FlightWaypoint:
        return self._target_point(target, f"STRIKE {target.name}")

    def sead_point(self, target: StrikeTarget) -> FlightWaypoint:
        return self._target_point(target, f"STRIKE {target.name}")

    def strike_point(self, target: StrikeTarget) -> FlightWaypoint:
        return self._target_point(target, f"STRIKE {target.name}")

    @staticmethod
    def _target_point(target: StrikeTarget, description: str) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.TARGET_POINT,
            target.target.position.x,
            target.target.position.y,
            0
        )
        waypoint.description = description
        waypoint.pretty_name = description
        waypoint.name = target.name
        # The target waypoints are only for the player's benefit. AI tasks for
        # the target are set on the ingress point so they begin their attack
        # *before* reaching the target.
        waypoint.only_for_player = True
        return waypoint

    def strike_area(self, target: MissionTarget) -> FlightWaypoint:
        return self._target_area(f"STRIKE {target.name}", target)

    def sead_area(self, target: MissionTarget) -> FlightWaypoint:
        return self._target_area(f"SEAD on {target.name}", target)

    def dead_area(self, target: MissionTarget) -> FlightWaypoint:
        return self._target_area(f"DEAD on {target.name}", target)

    @staticmethod
    def _target_area(name: str, location: MissionTarget) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.TARGET_GROUP_LOC,
            location.position.x,
            location.position.y,
            0
        )
        waypoint.description = name
        waypoint.pretty_name = name
        waypoint.name = name
        # The target waypoints are only for the player's benefit. AI tasks for
        # the target are set on the ingress point so they begin their attack
        # *before* reaching the target.
        waypoint.only_for_player = True
        return waypoint

    def cas(self, position: Point) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.CAS,
            position.x,
            position.y,
            500 if self.is_helo else 1000
        )
        waypoint.alt_type = "RADIO"
        waypoint.description = "Provide CAS"
        waypoint.name = "CAS"
        waypoint.pretty_name = "CAS"
        return waypoint

    @staticmethod
    def race_track_start(position: Point, altitude: int) -> FlightWaypoint:
        """Creates a racetrack start waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the racetrack in meters.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.PATROL_TRACK,
            position.x,
            position.y,
            altitude
        )
        waypoint.name = "RACETRACK START"
        waypoint.description = "Orbit between this point and the next point"
        waypoint.pretty_name = "Race-track start"
        return waypoint

    @staticmethod
    def race_track_end(position: Point, altitude: int) -> FlightWaypoint:
        """Creates a racetrack end waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the racetrack in meters.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.PATROL,
            position.x,
            position.y,
            altitude
        )
        waypoint.name = "RACETRACK END"
        waypoint.description = "Orbit between this point and the previous point"
        waypoint.pretty_name = "Race-track end"
        return waypoint

    def race_track(self, start: Point, end: Point,
                   altitude: int) -> Tuple[FlightWaypoint, FlightWaypoint]:
        """Creates two waypoint for a racetrack orbit.

        Args:
            start: The beginning racetrack waypoint.
            end: The ending racetrack waypoint.
            altitude: The racetrack altitude.
        """
        return (self.race_track_start(start, altitude),
                self.race_track_end(end, altitude))

    @staticmethod
    def sweep_start(position: Point, altitude: int) -> FlightWaypoint:
        """Creates a sweep start waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the sweep in meters.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.INGRESS_SWEEP,
            position.x,
            position.y,
            altitude
        )
        waypoint.name = "SWEEP START"
        waypoint.description = "Proceed to the target and engage enemy aircraft"
        waypoint.pretty_name = "Sweep start"
        return waypoint

    @staticmethod
    def sweep_end(position: Point, altitude: int) -> FlightWaypoint:
        """Creates a sweep end waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the sweep in meters.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.EGRESS,
            position.x,
            position.y,
            altitude
        )
        waypoint.name = "SWEEP END"
        waypoint.description = "End of sweep"
        waypoint.pretty_name = "Sweep end"
        return waypoint

    def sweep(self, start: Point, end: Point,
              altitude: int) -> Tuple[FlightWaypoint, FlightWaypoint]:
        """Creates two waypoint for a racetrack orbit.

        Args:
            start: The beginning of the sweep.
            end: The end of the sweep.
            altitude: The sweep altitude.
        """
        return (self.sweep_start(start, altitude),
                self.sweep_end(end, altitude))

    def escort(self, ingress: Point, target: MissionTarget, egress: Point) -> \
            Tuple[FlightWaypoint, FlightWaypoint, FlightWaypoint]:
        """Creates the waypoints needed to escort the package.

        Args:
            ingress: The package ingress point.
            target: The mission target.
            egress: The package egress point.
        """
        # This would preferably be no points at all, and instead the Escort task
        # would begin on the join point and end on the split point, however the
        # escort task does not appear to work properly (see the longer
        # description in gen.aircraft.JoinPointBuilder), so instead we give
        # the escort flights a flight plan including the ingress point, target
        # area, and egress point.
        ingress = self._ingress(FlightWaypointType.INGRESS_ESCORT, ingress,
                                target)

        waypoint = FlightWaypoint(
            FlightWaypointType.TARGET_GROUP_LOC,
            target.position.x,
            target.position.y,
            500 if self.is_helo else self.doctrine.ingress_altitude
        )
        waypoint.name = "TARGET"
        waypoint.description = "Escort the package"
        waypoint.pretty_name = "Target area"

        egress = self.egress(egress, target)
        return ingress, waypoint, egress
