from __future__ import annotations

import random
from dataclasses import dataclass
from typing import (
    Iterable,
    Iterator,
    List,
    Optional,
    TYPE_CHECKING,
    Tuple,
    Union,
)

from dcs.mapping import Point
from dcs.unit import Unit
from dcs.unitgroup import Group, VehicleGroup

if TYPE_CHECKING:
    from game import Game
    from game.transfers import MultiGroupTransport

from game.theater import (
    ControlPoint,
    MissionTarget,
    OffMapSpawn,
    TheaterGroundObject,
)
from game.utils import Distance, meters, nautical_miles
from .flight import Flight, FlightWaypoint, FlightWaypointType


@dataclass(frozen=True)
class StrikeTarget:
    name: str
    target: Union[VehicleGroup, TheaterGroundObject, Unit, Group, MultiGroupTransport]


class WaypointBuilder:
    def __init__(
        self,
        flight: Flight,
        game: Game,
        player: bool,
        targets: Optional[List[StrikeTarget]] = None,
    ) -> None:
        self.flight = flight
        self.conditions = game.conditions
        self.doctrine = game.faction_for(player).doctrine
        self.threat_zones = game.threat_zone_for(not player)
        self.navmesh = game.navmesh_for(player)
        self.targets = targets
        self._bullseye = game.bullseye_for(player)

    @property
    def is_helo(self) -> bool:
        return getattr(self.flight.unit_type, "helicopter", False)

    def takeoff(self, departure: ControlPoint) -> FlightWaypoint:
        """Create takeoff waypoint for the given arrival airfield or carrier.

        Note that the takeoff waypoint will automatically be created by pydcs
        when we create the group, but creating our own before generation makes
        the planning code simpler.

        Args:
            departure: Departure airfield or carrier.
        """
        position = departure.position
        if isinstance(departure, OffMapSpawn):
            waypoint = FlightWaypoint(
                FlightWaypointType.NAV,
                position.x,
                position.y,
                meters(500) if self.is_helo else self.doctrine.rendezvous_altitude,
            )
            waypoint.name = "NAV"
            waypoint.alt_type = "BARO"
            waypoint.description = "Enter theater"
            waypoint.pretty_name = "Enter theater"
        else:
            waypoint = FlightWaypoint(
                FlightWaypointType.TAKEOFF, position.x, position.y, meters(0)
            )
            waypoint.name = "TAKEOFF"
            waypoint.alt_type = "RADIO"
            waypoint.description = "Takeoff"
            waypoint.pretty_name = "Takeoff"
        return waypoint

    def land(self, arrival: ControlPoint) -> FlightWaypoint:
        """Create descent waypoint for the given arrival airfield or carrier.

        Args:
            arrival: Arrival airfield or carrier.
        """
        position = arrival.position
        if isinstance(arrival, OffMapSpawn):
            waypoint = FlightWaypoint(
                FlightWaypointType.NAV,
                position.x,
                position.y,
                meters(500) if self.is_helo else self.doctrine.rendezvous_altitude,
            )
            waypoint.name = "NAV"
            waypoint.alt_type = "BARO"
            waypoint.description = "Exit theater"
            waypoint.pretty_name = "Exit theater"
        else:
            waypoint = FlightWaypoint(
                FlightWaypointType.LANDING_POINT, position.x, position.y, meters(0)
            )
            waypoint.name = "LANDING"
            waypoint.alt_type = "RADIO"
            waypoint.description = "Land"
            waypoint.pretty_name = "Land"
        return waypoint

    def divert(self, divert: Optional[ControlPoint]) -> Optional[FlightWaypoint]:
        """Create divert waypoint for the given arrival airfield or carrier.

        Args:
            divert: Divert airfield or carrier.
        """
        if divert is None:
            return None

        position = divert.position
        if isinstance(divert, OffMapSpawn):
            if self.is_helo:
                altitude = meters(500)
            else:
                altitude = self.doctrine.rendezvous_altitude
            altitude_type = "BARO"
        else:
            altitude = meters(0)
            altitude_type = "RADIO"

        waypoint = FlightWaypoint(
            FlightWaypointType.DIVERT, position.x, position.y, altitude
        )
        waypoint.alt_type = altitude_type
        waypoint.name = "DIVERT"
        waypoint.description = "Divert"
        waypoint.pretty_name = "Divert"
        waypoint.only_for_player = True
        return waypoint

    def bullseye(self) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.BULLSEYE,
            self._bullseye.position.x,
            self._bullseye.position.y,
            meters(0),
        )
        waypoint.pretty_name = "Bullseye"
        waypoint.description = "Bullseye"
        waypoint.name = "BULLSEYE"
        waypoint.only_for_player = True
        return waypoint

    def hold(self, position: Point) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.LOITER,
            position.x,
            position.y,
            meters(500) if self.is_helo else self.doctrine.rendezvous_altitude,
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
            meters(80) if self.is_helo else self.doctrine.ingress_altitude,
        )
        if self.is_helo:
            waypoint.alt_type = "RADIO"
        waypoint.pretty_name = "Join"
        waypoint.description = "Rendezvous with package"
        waypoint.name = "JOIN"
        return waypoint

    def split(self, position: Point) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.SPLIT,
            position.x,
            position.y,
            meters(80) if self.is_helo else self.doctrine.ingress_altitude,
        )
        if self.is_helo:
            waypoint.alt_type = "RADIO"
        waypoint.pretty_name = "Split"
        waypoint.description = "Depart from package"
        waypoint.name = "SPLIT"
        return waypoint

    def ingress(
        self,
        ingress_type: FlightWaypointType,
        position: Point,
        objective: MissionTarget,
    ) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            ingress_type,
            position.x,
            position.y,
            meters(50) if self.is_helo else self.doctrine.ingress_altitude,
        )
        if self.is_helo:
            waypoint.alt_type = "RADIO"
        waypoint.pretty_name = "INGRESS on " + objective.name
        waypoint.description = "INGRESS on " + objective.name
        waypoint.name = "INGRESS"
        waypoint.targets = objective.strike_targets
        return waypoint

    def egress(self, position: Point, target: MissionTarget) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.EGRESS,
            position.x,
            position.y,
            meters(50) if self.is_helo else self.doctrine.ingress_altitude,
        )
        if self.is_helo:
            waypoint.alt_type = "RADIO"
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
            meters(0),
        )
        waypoint.description = description
        waypoint.pretty_name = description
        waypoint.name = target.name
        waypoint.alt_type = "RADIO"
        # The target waypoints are only for the player's benefit. AI tasks for
        # the target are set on the ingress point so they begin their attack
        # *before* reaching the target.
        waypoint.only_for_player = True
        return waypoint

    def strike_area(self, target: MissionTarget) -> FlightWaypoint:
        return self._target_area(f"STRIKE {target.name}", target)

    def sead_area(self, target: MissionTarget) -> FlightWaypoint:
        return self._target_area(f"SEAD on {target.name}", target, flyover=True)

    def dead_area(self, target: MissionTarget) -> FlightWaypoint:
        return self._target_area(f"DEAD on {target.name}", target)

    def oca_strike_area(self, target: MissionTarget) -> FlightWaypoint:
        return self._target_area(f"ATTACK {target.name}", target, flyover=True)

    @staticmethod
    def _target_area(
        name: str, location: MissionTarget, flyover: bool = False
    ) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.TARGET_GROUP_LOC,
            location.position.x,
            location.position.y,
            meters(0),
        )
        waypoint.description = name
        waypoint.pretty_name = name
        waypoint.name = name
        waypoint.alt_type = "RADIO"

        # Most target waypoints are only for the player's benefit. AI tasks for
        # the target are set on the ingress point so they begin their attack
        # *before* reaching the target.
        #
        # The exception is for flight plans that require passing over the
        # target. For example, OCA strikes need to get close enough to detect
        # the targets in their engagement zone or they will RTB immediately.
        if flyover:
            waypoint.flyover = True
        else:
            waypoint.only_for_player = True
        return waypoint

    def cas(self, position: Point) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            FlightWaypointType.CAS,
            position.x,
            position.y,
            meters(50) if self.is_helo else meters(1000),
        )
        waypoint.alt_type = "RADIO"
        waypoint.description = "Provide CAS"
        waypoint.name = "CAS"
        waypoint.pretty_name = "CAS"
        return waypoint

    @staticmethod
    def race_track_start(position: Point, altitude: Distance) -> FlightWaypoint:
        """Creates a racetrack start waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the racetrack.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.PATROL_TRACK, position.x, position.y, altitude
        )
        waypoint.name = "RACETRACK START"
        waypoint.description = "Orbit between this point and the next point"
        waypoint.pretty_name = "Race-track start"
        return waypoint

    @staticmethod
    def race_track_end(position: Point, altitude: Distance) -> FlightWaypoint:
        """Creates a racetrack end waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the racetrack.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.PATROL, position.x, position.y, altitude
        )
        waypoint.name = "RACETRACK END"
        waypoint.description = "Orbit between this point and the previous point"
        waypoint.pretty_name = "Race-track end"
        return waypoint

    def race_track(
        self, start: Point, end: Point, altitude: Distance
    ) -> Tuple[FlightWaypoint, FlightWaypoint]:
        """Creates two waypoint for a racetrack orbit.

        Args:
            start: The beginning racetrack waypoint.
            end: The ending racetrack waypoint.
            altitude: The racetrack altitude.
        """
        return (
            self.race_track_start(start, altitude),
            self.race_track_end(end, altitude),
        )

    @staticmethod
    def tanker_race_track_start(position: Point, altitude: Distance) -> FlightWaypoint:
        """Creates a racetrack start waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the racetrack.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.TANKER_RACETRACK_START, position.x, position.y, altitude
        )
        waypoint.name = "RACETRACK START"
        waypoint.description = "Tanker orbit between this point and the next point"
        waypoint.pretty_name = "Race-track start"
        return waypoint

    @staticmethod
    def tanker_race_track_end(position: Point, altitude: Distance) -> FlightWaypoint:
        """Creates a racetrack end waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the racetrack.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.TANKER_RACETRACK_STOP, position.x, position.y, altitude
        )
        waypoint.name = "RACETRACK END"
        waypoint.description = "Tanker orbit between this point and the previous point"
        waypoint.pretty_name = "Race-track end"
        return waypoint

    def tanker_race_track(
        self, start: Point, end: Point, altitude: Distance
    ) -> Tuple[FlightWaypoint, FlightWaypoint]:
        """Creates two waypoint for a racetrack orbit.

        Args:
            start: The beginning racetrack waypoint.
            end: The ending racetrack waypoint.
            altitude: The racetrack altitude.
        """
        return (
            self.tanker_race_track_start(start, altitude),
            self.tanker_race_track_end(end, altitude),
        )

    @staticmethod
    def orbit(start: Point, altitude: Distance) -> FlightWaypoint:
        """Creates an circular orbit point.

        Args:
            start: Position of the waypoint.
            altitude: Altitude of the racetrack.
        """

        waypoint = FlightWaypoint(FlightWaypointType.LOITER, start.x, start.y, altitude)
        waypoint.name = "ORBIT"
        waypoint.description = "Anchor and hold at this point"
        waypoint.pretty_name = "Orbit"
        return waypoint

    @staticmethod
    def sweep_start(position: Point, altitude: Distance) -> FlightWaypoint:
        """Creates a sweep start waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the sweep in meters.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.INGRESS_SWEEP, position.x, position.y, altitude
        )
        waypoint.name = "SWEEP START"
        waypoint.description = "Proceed to the target and engage enemy aircraft"
        waypoint.pretty_name = "Sweep start"
        return waypoint

    @staticmethod
    def sweep_end(position: Point, altitude: Distance) -> FlightWaypoint:
        """Creates a sweep end waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the sweep in meters.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.EGRESS, position.x, position.y, altitude
        )
        waypoint.name = "SWEEP END"
        waypoint.description = "End of sweep"
        waypoint.pretty_name = "Sweep end"
        return waypoint

    def sweep(
        self, start: Point, end: Point, altitude: Distance
    ) -> Tuple[FlightWaypoint, FlightWaypoint]:
        """Creates two waypoint for a racetrack orbit.

        Args:
            start: The beginning of the sweep.
            end: The end of the sweep.
            altitude: The sweep altitude.
        """
        return self.sweep_start(start, altitude), self.sweep_end(end, altitude)

    def escort(
        self,
        ingress: Point,
        target: MissionTarget,
        egress: Point,
    ) -> Tuple[FlightWaypoint, FlightWaypoint, FlightWaypoint]:
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
        ingress = self.ingress(FlightWaypointType.INGRESS_ESCORT, ingress, target)

        waypoint = FlightWaypoint(
            FlightWaypointType.TARGET_GROUP_LOC,
            target.position.x,
            target.position.y,
            meters(50) if self.is_helo else self.doctrine.ingress_altitude,
        )
        if self.is_helo:
            waypoint.alt_type = "RADIO"
        waypoint.name = "TARGET"
        waypoint.description = "Escort the package"
        waypoint.pretty_name = "Target area"

        egress = self.egress(egress, target)
        return ingress, waypoint, egress

    @staticmethod
    def pickup(control_point: ControlPoint) -> FlightWaypoint:
        """Creates a cargo pickup waypoint.

        Args:
            control_point: Pick up location.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.PICKUP,
            control_point.position.x,
            control_point.position.y,
            meters(0),
        )
        waypoint.alt_type = "RADIO"
        waypoint.name = "PICKUP"
        waypoint.description = f"Pick up cargo from {control_point}"
        waypoint.pretty_name = "Pick up location"
        return waypoint

    @staticmethod
    def drop_off(control_point: ControlPoint) -> FlightWaypoint:
        """Creates a cargo drop-off waypoint.

        Args:
            control_point: Drop-off location.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.PICKUP,
            control_point.position.x,
            control_point.position.y,
            meters(0),
        )
        waypoint.alt_type = "RADIO"
        waypoint.name = "DROP OFF"
        waypoint.description = f"Drop off cargo at {control_point}"
        waypoint.pretty_name = "Drop off location"
        return waypoint

    @staticmethod
    def nav(
        position: Point, altitude: Distance, altitude_is_agl: bool = False
    ) -> FlightWaypoint:
        """Creates a navigation point.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the waypoint.
            altitude_is_agl: True for altitude is AGL. False if altitude is MSL.
        """
        waypoint = FlightWaypoint(
            FlightWaypointType.NAV, position.x, position.y, altitude
        )
        if altitude_is_agl:
            waypoint.alt_type = "RADIO"
        waypoint.name = "NAV"
        waypoint.description = "NAV"
        waypoint.pretty_name = "Nav"
        return waypoint

    def nav_path(
        self, a: Point, b: Point, altitude: Distance, altitude_is_agl: bool = False
    ) -> List[FlightWaypoint]:
        path = self.clean_nav_points(self.navmesh.shortest_path(a, b))
        return [self.nav(self.perturb(p), altitude, altitude_is_agl) for p in path]

    def clean_nav_points(self, points: Iterable[Point]) -> Iterator[Point]:
        # Examine a sliding window of three waypoints. `current` is the waypoint
        # being checked for prunability. `previous` is the last emitted waypoint
        # before `current`. `nxt` is the waypoint after `current`.
        previous: Optional[Point] = None
        current: Optional[Point] = None
        for nxt in points:
            if current is None:
                current = nxt
                continue
            if previous is None:
                previous = current
                current = nxt
                continue

            if self.nav_point_prunable(previous, current, nxt):
                current = nxt
                continue

            yield current
            previous = current
            current = nxt

    def nav_point_prunable(self, previous: Point, current: Point, nxt: Point) -> bool:
        previous_threatened = self.threat_zones.path_threatened(previous, current)
        next_threatened = self.threat_zones.path_threatened(current, nxt)
        pruned_threatened = self.threat_zones.path_threatened(previous, nxt)
        previous_distance = meters(previous.distance_to_point(current))
        distance = meters(current.distance_to_point(nxt))
        distance_without = previous_distance + distance
        if distance > distance_without:
            # Don't prune paths to make them longer.
            return False

        # We could shorten the path by removing the intermediate
        # waypoint. Do so if the new path isn't higher threat.
        if not pruned_threatened:
            # The new path is not threatened, so safe to prune.
            return True

        # The new path is threatened. Only allow if both paths were
        # threatened anyway.
        return previous_threatened and next_threatened

    @staticmethod
    def perturb(point: Point) -> Point:
        deviation = nautical_miles(1)
        x_adj = random.randint(int(-deviation.meters), int(deviation.meters))
        y_adj = random.randint(int(-deviation.meters), int(deviation.meters))
        return Point(point.x + x_adj, point.y + y_adj)
