from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterator, List, Tuple, Any, TYPE_CHECKING

from dcs.mapping import Point

from .controlpoint import ControlPoint, MissionTarget
from ..utils import Heading, pairwise

if TYPE_CHECKING:
    from game.ato import FlightType


@dataclass
class FrontLineSegment:
    """
    Describes a line segment of a FrontLine
    """

    point_a: Point
    point_b: Point

    @property
    def attack_heading(self) -> Heading:
        """The heading of the frontline segment from player to enemy control point"""
        return Heading.from_degrees(self.point_a.heading_between_point(self.point_b))

    @property
    def attack_distance(self) -> float:
        """Length of the segment"""
        return self.point_a.distance_to_point(self.point_b)


class FrontLine(MissionTarget):
    """Defines a front line location between two control points.
    Front lines are the area where ground combat happens.
    Overwrites the entirety of MissionTarget __init__ method to allow for
    dynamic position calculation.
    """

    def __init__(
        self,
        blue_point: ControlPoint,
        red_point: ControlPoint,
    ) -> None:
        self.blue_cp = blue_point
        self.red_cp = red_point
        try:
            route = list(blue_point.convoy_route_to(red_point))
        except KeyError:
            # Some campaigns are air only and the mission generator currently relies on
            # *some* "front line" being drawn between these two. In this case there will
            # be no supply route to follow. Just create an arbitrary route between the
            # two points.
            route = [blue_point.position, red_point.position]
        # Snap the beginning and end points to the CPs rather than the convoy waypoints,
        # which are on roads.
        route[0] = blue_point.position
        route[-1] = red_point.position
        self.segments: List[FrontLineSegment] = [
            FrontLineSegment(a, b) for a, b in pairwise(route)
        ]
        super().__init__(
            f"Front line {blue_point}/{red_point}",
            self.point_from_a(self._position_distance),
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FrontLine):
            return False
        return (self.blue_cp, self.red_cp) == (other.blue_cp, other.red_cp)

    def __hash__(self) -> int:
        return hash((self.blue_cp, self.red_cp))

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        if not hasattr(self, "position"):
            self.position = self.point_from_a(self._position_distance)

    def control_point_friendly_to(self, player: bool) -> ControlPoint:
        if player:
            return self.blue_cp
        return self.red_cp

    def control_point_hostile_to(self, player: bool) -> ControlPoint:
        return self.control_point_friendly_to(not player)

    def is_friendly(self, to_player: bool) -> bool:
        """Returns True if the objective is in friendly territory."""
        return False

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from game.ato import FlightType

        yield from [
            FlightType.CAS,
            FlightType.AEWC,
            FlightType.REFUELING
            # TODO: FlightType.TROOP_TRANSPORT
            # TODO: FlightType.EVAC
        ]
        yield from super().mission_types(for_player)

    @property
    def points(self) -> Iterator[Point]:
        yield self.segments[0].point_a
        for segment in self.segments:
            yield segment.point_b

    @property
    def control_points(self) -> Tuple[ControlPoint, ControlPoint]:
        """Returns a tuple of the two control points."""
        return self.blue_cp, self.red_cp

    @property
    def attack_distance(self) -> float:
        """The total distance of all segments"""
        return sum(i.attack_distance for i in self.segments)

    @property
    def attack_heading(self) -> Heading:
        """The heading of the active attack segment from player to enemy control point"""
        return self.active_segment.attack_heading

    @property
    def active_segment(self) -> FrontLineSegment:
        """The FrontLine segment where there can be an active conflict"""
        if self._position_distance <= self.segments[0].attack_distance:
            return self.segments[0]

        remaining_dist = self._position_distance
        for segment in self.segments:
            if remaining_dist <= segment.attack_distance:
                return segment
            else:
                remaining_dist -= segment.attack_distance
        logging.error(
            "Frontline attack distance is greater than the sum of its segments"
        )
        return self.segments[0]

    def point_from_a(self, distance: float) -> Point:
        """
        Returns a point {distance} away from control_point_a along the frontline segments.
        """
        if distance < self.segments[0].attack_distance:
            return self.blue_cp.position.point_from_heading(
                self.segments[0].attack_heading.degrees, distance
            )
        remaining_dist = distance
        for segment in self.segments:
            if remaining_dist < segment.attack_distance:
                return segment.point_a.point_from_heading(
                    segment.attack_heading.degrees, remaining_dist
                )
            else:
                remaining_dist -= segment.attack_distance
        raise RuntimeError(
            f"Could not find front line point {distance} from {self.blue_cp}"
        )

    @property
    def _position_distance(self) -> float:
        """
        The distance from point "a" where the conflict should occur
        according to the current strength of each control point
        """
        total_strength = self.blue_cp.base.strength + self.red_cp.base.strength
        if self.blue_cp.base.strength == 0:
            return self._keep_frontline_within_bounds(0)
        if self.red_cp.base.strength == 0:
            return self._keep_frontline_within_bounds(self.attack_distance)
        strength_pct = self.blue_cp.base.strength / total_strength
        return self._keep_frontline_within_bounds(strength_pct * self.attack_distance)

    def _keep_frontline_within_bounds(self, distance: float) -> float:
        """
        Ensures the frontline conflict is always located between the control points
        and cannot move behind either one, where we couldn't find route segments.
        This is done by making sure the frontline is always placed at least
        one segment away from either control point.
        """
        if distance > self.attack_distance - self.segments[-1].attack_distance:
            distance = self.attack_distance - self.segments[-1].attack_distance
        elif distance < self.segments[0].attack_distance:
            distance = self.segments[0].attack_distance
        return distance
