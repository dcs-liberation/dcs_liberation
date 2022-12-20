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

from dcs.mapping import Point, Vector2

from game.ato.flightwaypoint import AltitudeReference, FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.theater import (
    ControlPoint,
    MissionTarget,
    OffMapSpawn,
    TheaterGroundObject,
    TheaterUnit,
)
from game.utils import Distance, feet, meters, nautical_miles

if TYPE_CHECKING:
    from game.coalition import Coalition
    from game.transfers import MultiGroupTransport
    from game.theater.theatergroup import TheaterGroup
    from game.ato.flight import Flight


@dataclass(frozen=True)
class StrikeTarget:
    name: str
    target: Union[TheaterGroundObject, TheaterGroup, TheaterUnit, MultiGroupTransport]


class WaypointBuilder:
    def __init__(
        self,
        flight: Flight,
        coalition: Coalition,
        targets: Optional[List[StrikeTarget]] = None,
    ) -> None:
        self.flight = flight
        self.doctrine = coalition.doctrine
        self.threat_zones = coalition.opponent.threat_zone
        self.navmesh = coalition.nav_mesh
        self.targets = targets
        self._bullseye = coalition.bullseye

    @property
    def is_helo(self) -> bool:
        return self.flight.is_helo

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
            return FlightWaypoint(
                "NAV",
                FlightWaypointType.NAV,
                position,
                meters(500) if self.is_helo else self.doctrine.rendezvous_altitude,
                description="Enter theater",
                pretty_name="Enter theater",
            )

        return FlightWaypoint(
            "TAKEOFF",
            FlightWaypointType.TAKEOFF,
            position,
            meters(0),
            alt_type="RADIO",
            description="Takeoff",
            pretty_name="Takeoff",
        )

    def land(self, arrival: ControlPoint) -> FlightWaypoint:
        """Create descent waypoint for the given arrival airfield or carrier.

        Args:
            arrival: Arrival airfield or carrier.
        """
        position = arrival.position
        if isinstance(arrival, OffMapSpawn):
            return FlightWaypoint(
                "NAV",
                FlightWaypointType.NAV,
                position,
                meters(500) if self.is_helo else self.doctrine.rendezvous_altitude,
                description="Exit theater",
                pretty_name="Exit theater",
            )

        return FlightWaypoint(
            "LANDING",
            FlightWaypointType.LANDING_POINT,
            position,
            meters(0),
            alt_type="RADIO",
            description="Land",
            pretty_name="Land",
            control_point=arrival,
        )

    def divert(self, divert: Optional[ControlPoint]) -> Optional[FlightWaypoint]:
        """Create divert waypoint for the given arrival airfield or carrier.

        Args:
            divert: Divert airfield or carrier.
        """
        if divert is None:
            return None

        position = divert.position
        altitude_type: AltitudeReference
        if isinstance(divert, OffMapSpawn):
            if self.is_helo:
                altitude = meters(500)
            else:
                altitude = self.doctrine.rendezvous_altitude
            altitude_type = "BARO"
        else:
            altitude = meters(0)
            altitude_type = "RADIO"

        return FlightWaypoint(
            "DIVERT",
            FlightWaypointType.DIVERT,
            position,
            altitude,
            alt_type=altitude_type,
            description="Divert",
            pretty_name="Divert",
            only_for_player=True,
            control_point=divert,
        )

    def bullseye(self) -> FlightWaypoint:
        return FlightWaypoint(
            "BULLSEYE",
            FlightWaypointType.BULLSEYE,
            self._bullseye.position,
            meters(0),
            description="Bullseye",
            pretty_name="Bullseye",
            only_for_player=True,
        )

    def hold(self, position: Point) -> FlightWaypoint:
        alt_type: AltitudeReference = "BARO"
        if self.is_helo:
            alt_type = "RADIO"

        return FlightWaypoint(
            "HOLD",
            FlightWaypointType.LOITER,
            position,
            meters(500) if self.is_helo else self.doctrine.rendezvous_altitude,
            alt_type,
            description="Wait until push time",
            pretty_name="Hold",
        )

    def join(self, position: Point) -> FlightWaypoint:
        alt_type: AltitudeReference = "BARO"
        if self.is_helo:
            alt_type = "RADIO"

        return FlightWaypoint(
            "JOIN",
            FlightWaypointType.JOIN,
            position,
            meters(80) if self.is_helo else self.doctrine.ingress_altitude,
            alt_type,
            description="Rendezvous with package",
            pretty_name="Join",
        )

    def refuel(self, position: Point) -> FlightWaypoint:
        alt_type: AltitudeReference = "BARO"
        if self.is_helo:
            alt_type = "RADIO"

        return FlightWaypoint(
            "REFUEL",
            FlightWaypointType.REFUEL,
            position,
            meters(80) if self.is_helo else self.doctrine.ingress_altitude,
            alt_type,
            description="Refuel from tanker",
            pretty_name="Refuel",
        )

    def recovery_tanker(self, position: Point) -> FlightWaypoint:
        alt_type: AltitudeReference = "BARO"

        return FlightWaypoint(
            "RECOVERY",
            FlightWaypointType.RECOVERY_TANKER,
            position,
            feet(6000),
            alt_type,
            description="Recovery tanker for aircraft carriers",
            pretty_name="Recovery",
        )

    def split(self, position: Point) -> FlightWaypoint:
        alt_type: AltitudeReference = "BARO"
        if self.is_helo:
            alt_type = "RADIO"

        return FlightWaypoint(
            "SPLIT",
            FlightWaypointType.SPLIT,
            position,
            meters(80) if self.is_helo else self.doctrine.ingress_altitude,
            alt_type,
            description="Depart from package",
            pretty_name="Split",
        )

    def ingress(
        self,
        ingress_type: FlightWaypointType,
        position: Point,
        objective: MissionTarget,
    ) -> FlightWaypoint:
        alt_type: AltitudeReference = "BARO"
        if self.is_helo:
            alt_type = "RADIO"

        return FlightWaypoint(
            "INGRESS",
            ingress_type,
            position,
            meters(60) if self.is_helo else self.doctrine.ingress_altitude,
            alt_type,
            description=f"INGRESS on {objective.name}",
            pretty_name=f"INGRESS on {objective.name}",
            targets=objective.strike_targets,
        )

    def egress(self, position: Point, target: MissionTarget) -> FlightWaypoint:
        alt_type: AltitudeReference = "BARO"
        if self.is_helo:
            alt_type = "RADIO"

        return FlightWaypoint(
            "EGRESS",
            FlightWaypointType.EGRESS,
            position,
            meters(60) if self.is_helo else self.doctrine.ingress_altitude,
            alt_type,
            description=f"EGRESS from {target.name}",
            pretty_name=f"EGRESS from {target.name}",
        )

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
        return FlightWaypoint(
            target.name,
            FlightWaypointType.TARGET_POINT,
            target.target.position,
            meters(0),
            "RADIO",
            description=description,
            pretty_name=description,
            # The target waypoints are only for the player's benefit. AI tasks for
            # the target are set on the ingress point so that they begin their attack
            # *before* reaching the target.
            only_for_player=True,
        )

    def strike_area(self, target: MissionTarget) -> FlightWaypoint:
        return self._target_area(f"STRIKE {target.name}", target)

    def sead_area(self, target: MissionTarget) -> FlightWaypoint:
        # Set flyover with ingress altitude to allow the flight to search and engage
        # the target group at the ingress alt without suicide dive
        return self._target_area(
            f"SEAD on {target.name}",
            target,
            flyover=True,
            altitude=self.doctrine.ingress_altitude,
            alt_type="BARO",
        )

    def dead_area(self, target: MissionTarget) -> FlightWaypoint:
        return self._target_area(f"DEAD on {target.name}", target)

    def oca_strike_area(self, target: MissionTarget) -> FlightWaypoint:
        return self._target_area(f"ATTACK {target.name}", target, flyover=True)

    def assault_area(self, target: MissionTarget) -> FlightWaypoint:
        """A destination waypoint used by air-assault ground troops.

        This waypoint is an implementation detail for CTLD and should not be followed by
        aircraft.
        """
        # TODO: Add a property that can hide this waypoint from the player's flight
        # plan.
        return self._target_area(f"ASSAULT {target.name}", target)

    @staticmethod
    def _target_area(
        name: str,
        location: MissionTarget,
        flyover: bool = False,
        altitude: Distance = meters(0),
        alt_type: AltitudeReference = "RADIO",
    ) -> FlightWaypoint:
        waypoint = FlightWaypoint(
            name,
            FlightWaypointType.TARGET_GROUP_LOC,
            location.position,
            altitude,
            alt_type,
            description=name,
            pretty_name=name,
        )

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
        return FlightWaypoint(
            "CAS",
            FlightWaypointType.CAS,
            position,
            meters(60) if self.is_helo else meters(1000),
            "RADIO",
            description="Provide CAS",
            pretty_name="CAS",
        )

    @staticmethod
    def race_track_start(position: Point, altitude: Distance) -> FlightWaypoint:
        """Creates a racetrack start waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the racetrack.
        """
        return FlightWaypoint(
            "RACETRACK START",
            FlightWaypointType.PATROL_TRACK,
            position,
            altitude,
            description="Orbit between this point and the next point",
            pretty_name="Race-track start",
        )

    @staticmethod
    def race_track_end(position: Point, altitude: Distance) -> FlightWaypoint:
        """Creates a racetrack end waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the racetrack.
        """
        return FlightWaypoint(
            "RACETRACK END",
            FlightWaypointType.PATROL,
            position,
            altitude,
            description="Orbit between this point and the previous point",
            pretty_name="Race-track end",
        )

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
    def orbit(start: Point, altitude: Distance) -> FlightWaypoint:
        """Creates an circular orbit point.

        Args:
            start: Position of the waypoint.
            altitude: Altitude of the racetrack.
        """

        return FlightWaypoint(
            "ORBIT",
            FlightWaypointType.LOITER,
            start,
            altitude,
            description="Anchor and hold at this point",
            pretty_name="Orbit",
        )

    @staticmethod
    def sweep_start(position: Point, altitude: Distance) -> FlightWaypoint:
        """Creates a sweep start waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the sweep in meters.
        """
        return FlightWaypoint(
            "SWEEP START",
            FlightWaypointType.INGRESS_SWEEP,
            position,
            altitude,
            description="Proceed to the target and engage enemy aircraft",
            pretty_name="Sweep start",
        )

    @staticmethod
    def sweep_end(position: Point, altitude: Distance) -> FlightWaypoint:
        """Creates a sweep end waypoint.

        Args:
            position: Position of the waypoint.
            altitude: Altitude of the sweep in meters.
        """
        return FlightWaypoint(
            "SWEEP END",
            FlightWaypointType.EGRESS,
            position,
            altitude,
            description="End of sweep",
            pretty_name="Sweep end",
        )

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
    ) -> Tuple[FlightWaypoint, FlightWaypoint]:
        """Creates the waypoints needed to escort the package.

        Args:
            ingress: The package ingress point.
            target: The mission target.
        """
        alt_type: AltitudeReference = "BARO"
        if self.is_helo:
            alt_type = "RADIO"

        # This would preferably be no points at all, and instead the Escort task
        # would begin on the join point and end on the split point, however the
        # escort task does not appear to work properly (see the longer
        # description in gen.aircraft.JoinPointBuilder), so instead we give
        # the escort flights a flight plan including the ingress point and target area.
        ingress_wp = self.ingress(FlightWaypointType.INGRESS_ESCORT, ingress, target)

        return ingress_wp, FlightWaypoint(
            "TARGET",
            FlightWaypointType.TARGET_GROUP_LOC,
            target.position,
            meters(60) if self.is_helo else self.doctrine.ingress_altitude,
            alt_type,
            description="Escort the package",
            pretty_name="Target area",
        )

    @staticmethod
    def pickup_zone(pick_up: MissionTarget) -> FlightWaypoint:
        """Creates a pickup landing zone waypoint
        This waypoint is used to generate the Trigger Zone used for AirAssault and
        AirLift using the CTLD plugin (see LogisticsGenerator)
        """
        return FlightWaypoint(
            "PICKUPZONE",
            FlightWaypointType.PICKUP_ZONE,
            pick_up.position,
            meters(0),
            "RADIO",
            description=f"Pick up cargo from {pick_up.name}",
            pretty_name="Pick-up zone",
        )

    @staticmethod
    def dropoff_zone(drop_off: MissionTarget) -> FlightWaypoint:
        """Creates a dropoff landing zone waypoint
        This waypoint is used to generate the Trigger Zone used for AirAssault and
        AirLift using the CTLD plugin (see LogisticsGenerator)
        """
        return FlightWaypoint(
            "DROPOFFZONE",
            FlightWaypointType.DROPOFF_ZONE,
            drop_off.position,
            meters(0),
            "RADIO",
            description=f"Drop off cargo at {drop_off.name}",
            pretty_name="Drop-off zone",
        )

    @staticmethod
    def cargo_stop(control_point: ControlPoint) -> FlightWaypoint:
        """Creates a cargo stop waypoint.
        This waypoint is used by AirLift as a landing and stopover waypoint
        """
        return FlightWaypoint(
            "CARGOSTOP",
            FlightWaypointType.CARGO_STOP,
            control_point.position,
            meters(0),
            "RADIO",
            description=f"Stop for cargo at {control_point.name}",
            pretty_name="Cargo stop",
            control_point=control_point,
        )

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
        alt_type: AltitudeReference = "BARO"
        if altitude_is_agl:
            alt_type = "RADIO"

        return FlightWaypoint(
            "NAV",
            FlightWaypointType.NAV,
            position,
            altitude,
            alt_type,
            description="NAV",
            pretty_name="Nav",
        )

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
        return point + Vector2(x_adj, y_adj)
