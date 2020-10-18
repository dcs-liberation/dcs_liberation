from __future__ import annotations

from typing import List, Optional, Union

from dcs.mapping import Point
from dcs.unit import Unit

from game.data.doctrine import Doctrine
from game.utils import nm_to_meter
from theater import ControlPoint, MissionTarget, TheaterGroundObject
from .flight import Flight, FlightWaypoint, FlightWaypointType


class WaypointBuilder:
    def __init__(self, flight: Flight, doctrine: Doctrine) -> None:
        self.flight = flight
        self.doctrine = doctrine
        self.waypoints: List[FlightWaypoint] = []
        self.ingress_point: Optional[FlightWaypoint] = None

    def build(self) -> List[FlightWaypoint]:
        return self.waypoints

    def ascent(self, departure: ControlPoint, is_helo: bool = False) -> None:
        """Create ascent waypoint for the given departure airfield or carrier.

        Args:
            departure: Departure airfield or carrier.
            is_helo: True if the flight is a helicopter.
        """
        # TODO: Pick runway based on wind direction.
        heading = departure.heading
        position = departure.position.point_from_heading(
            heading, nm_to_meter(5)
        )
        waypoint = FlightWaypoint(
            FlightWaypointType.ASCEND_POINT,
            position.x,
            position.y,
            500 if is_helo else self.doctrine.pattern_altitude
        )
        waypoint.name = "ASCEND"
        waypoint.alt_type = "RADIO"
        waypoint.description = "Ascend"
        waypoint.pretty_name = "Ascend"
        self.waypoints.append(waypoint)

    def descent(self, arrival: ControlPoint, is_helo: bool = False) -> None:
        """Create descent waypoint for the given arrival airfield or carrier.

        Args:
            arrival: Arrival airfield or carrier.
            is_helo: True if the flight is a helicopter.
        """
        # TODO: Pick runway based on wind direction.
        # ControlPoint.heading is the departure heading.
        heading = (arrival.heading + 180) % 360
        position = arrival.position.point_from_heading(
            heading, nm_to_meter(5)
        )
        waypoint = FlightWaypoint(
            FlightWaypointType.DESCENT_POINT,
            position.x,
            position.y,
            300 if is_helo else self.doctrine.pattern_altitude
        )
        waypoint.name = "DESCEND"
        waypoint.alt_type = "RADIO"
        waypoint.description = "Descend to pattern altitude"
        waypoint.pretty_name = "Descend"
        self.waypoints.append(waypoint)

    def land(self, arrival: ControlPoint) -> None:
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
        self.waypoints.append(waypoint)

    def hold(self, position: Point) -> None:
        waypoint = FlightWaypoint(
            FlightWaypointType.LOITER,
            position.x,
            position.y,
            self.doctrine.rendezvous_altitude
        )
        waypoint.pretty_name = "Hold"
        waypoint.description = "Wait until push time"
        waypoint.name = "HOLD"
        self.waypoints.append(waypoint)

    def join(self, position: Point) -> None:
        waypoint = FlightWaypoint(
            FlightWaypointType.JOIN,
            position.x,
            position.y,
            self.doctrine.ingress_altitude
        )
        waypoint.pretty_name = "Join"
        waypoint.description = "Rendezvous with package"
        waypoint.name = "JOIN"
        self.waypoints.append(waypoint)

    def split(self, position: Point) -> None:
        waypoint = FlightWaypoint(
            FlightWaypointType.SPLIT,
            position.x,
            position.y,
            self.doctrine.ingress_altitude
        )
        waypoint.pretty_name = "Split"
        waypoint.description = "Depart from package"
        waypoint.name = "SPLIT"
        self.waypoints.append(waypoint)

    def ingress_cas(self, position: Point, objective: MissionTarget) -> None:
        self._ingress(FlightWaypointType.INGRESS_CAS, position, objective)

    def ingress_escort(self, position: Point, objective: MissionTarget) -> None:
        self._ingress(FlightWaypointType.INGRESS_ESCORT, position, objective)

    def ingress_sead(self, position: Point, objective: MissionTarget) -> None:
        self._ingress(FlightWaypointType.INGRESS_SEAD, position, objective)

    def ingress_strike(self, position: Point, objective: MissionTarget) -> None:
        self._ingress(FlightWaypointType.INGRESS_STRIKE, position, objective)

    def _ingress(self, ingress_type: FlightWaypointType, position: Point,
                 objective: MissionTarget) -> None:
        if self.ingress_point is not None:
            raise RuntimeError("A flight plan can have only one ingress point.")

        waypoint = FlightWaypoint(
            ingress_type,
            position.x,
            position.y,
            self.doctrine.ingress_altitude
        )
        waypoint.pretty_name = "INGRESS on " + objective.name
        waypoint.description = "INGRESS on " + objective.name
        waypoint.name = "INGRESS"
        self.waypoints.append(waypoint)
        self.ingress_point = waypoint

    def egress(self, position: Point, target: MissionTarget) -> None:
        waypoint = FlightWaypoint(
            FlightWaypointType.EGRESS,
            position.x,
            position.y,
            self.doctrine.ingress_altitude
        )
        waypoint.pretty_name = "EGRESS from " + target.name
        waypoint.description = "EGRESS from " + target.name
        waypoint.name = "EGRESS"
        self.waypoints.append(waypoint)

    def dead_point(self, target: Union[TheaterGroundObject, Unit], name: str,
                   location: MissionTarget) -> None:
        self._target_point(target, name, f"STRIKE [{location.name}]: {name}",
                           location)
        # TODO: Seems fishy.
        if self.ingress_point is not None:
            self.ingress_point.targetGroup = location

    def sead_point(self, target: Union[TheaterGroundObject, Unit], name: str,
                   location: MissionTarget) -> None:
        self._target_point(target, name, f"STRIKE [{location.name}]: {name}",
                           location)
        # TODO: Seems fishy.
        if self.ingress_point is not None:
            self.ingress_point.targetGroup = location

    def strike_point(self, target: Union[TheaterGroundObject, Unit], name: str,
                     location: MissionTarget) -> None:
        self._target_point(target, name, f"STRIKE [{location.name}]: {name}",
                           location)

    def _target_point(self, target: Union[TheaterGroundObject, Unit], name: str,
                      description: str, location: MissionTarget) -> None:
        if self.ingress_point is None:
            raise RuntimeError(
                "An ingress point must be added before target points."
            )

        waypoint = FlightWaypoint(
            FlightWaypointType.TARGET_POINT,
            target.position.x,
            target.position.y,
            0
        )
        waypoint.description = description
        waypoint.pretty_name = description
        waypoint.name = name
        # The target waypoints are only for the player's benefit. AI tasks for
        # the target are set on the ingress point so they begin their attack
        # *before* reaching the target.
        waypoint.only_for_player = True
        self.waypoints.append(waypoint)
        # TODO: This seems wrong, but it's what was there before.
        self.ingress_point.targets.append(location)

    def sead_area(self, target: MissionTarget) -> None:
        self._target_area(f"SEAD on {target.name}", target)
        # TODO: Seems fishy.
        if self.ingress_point is not None:
            self.ingress_point.targetGroup = target

    def dead_area(self, target: MissionTarget) -> None:
        self._target_area(f"DEAD on {target.name}", target)
        # TODO: Seems fishy.
        if self.ingress_point is not None:
            self.ingress_point.targetGroup = target

    def _target_area(self, name: str, location: MissionTarget) -> None:
        if self.ingress_point is None:
            raise RuntimeError(
                "An ingress point must be added before target points."
            )

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
        self.waypoints.append(waypoint)
        # TODO: This seems wrong, but it's what was there before.
        self.ingress_point.targets.append(location)

    def cas(self, position: Point, altitude: int) -> None:
        waypoint = FlightWaypoint(
            FlightWaypointType.CAS,
            position.x,
            position.y,
            altitude
        )
        waypoint.alt_type = "RADIO"
        waypoint.description = "Provide CAS"
        waypoint.name = "CAS"
        waypoint.pretty_name = "CAS"
        self.waypoints.append(waypoint)

    def race_track_start(self, position: Point, altitude: int) -> None:
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
        self.waypoints.append(waypoint)

    def race_track_end(self, position: Point, altitude: int) -> None:
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
        self.waypoints.append(waypoint)

    def race_track(self, start: Point, end: Point, altitude: int) -> None:
        """Creates two waypoint for a racetrack orbit.

        Args:
            start: The beginning racetrack waypoint.
            end: The ending racetrack waypoint.
            altitude: The racetrack altitude.
        """
        self.race_track_start(start, altitude)
        self.race_track_end(end, altitude)

    def rtb(self, arrival: ControlPoint, is_helo: bool = False) -> None:
        """Creates descent ant landing waypoints for the given control point.

        Args:
            arrival: Arrival airfield or carrier.
            is_helo: True if the flight is a helicopter.
        """
        self.descent(arrival, is_helo)
        self.land(arrival)

    def escort(self, ingress: Point, target: MissionTarget,
               egress: Point) -> None:
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
        self._ingress(FlightWaypointType.INGRESS_ESCORT, ingress, target)

        waypoint = FlightWaypoint(
            FlightWaypointType.TARGET_GROUP_LOC,
            target.position.x,
            target.position.y,
            self.doctrine.ingress_altitude
        )
        waypoint.name = "TARGET"
        waypoint.description = "Escort the package"
        waypoint.pretty_name = "Target area"
        self.waypoints.append(waypoint)

        self.egress(egress, target)
