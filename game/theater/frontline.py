from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from typing import Any, Iterator, List, TYPE_CHECKING, Tuple

from dcs.mapping import Point

from .missiontarget import MissionTarget
from ..utils import Heading, pairwise

if TYPE_CHECKING:
    from game.ato import FlightType
    from .controlpoint import ControlPoint


FRONTLINE_MIN_CP_DISTANCE = 5000


@dataclass
class FrontLineSegment:
    """
    Describes a line segment of a FrontLine
    """

    point_a: Point
    point_b: Point

    @property
    def blue_forward_heading(self) -> Heading:
        """The heading toward the start of the next red segment or red base."""
        return Heading.from_degrees(self.point_a.heading_between_point(self.point_b))

    @property
    def length(self) -> float:
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
        self.id = uuid.uuid4()
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
            f"Front line {blue_point}/{red_point}", self._compute_position()
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FrontLine):
            return False
        return (self.blue_cp, self.red_cp) == (other.blue_cp, other.red_cp)

    def __hash__(self) -> int:
        return hash(id(self))

    def _compute_position(self) -> Point:
        return self.point_along_route_from_blue(self._blue_route_progress)

    def update_position(self) -> None:
        self.position = self._compute_position()

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
    def route_length(self) -> float:
        """The total distance of all segments"""
        return sum(i.length for i in self.segments)

    @property
    def blue_forward_heading(self) -> Heading:
        """The heading toward the start of the next red segment or red base."""
        return self.active_segment.blue_forward_heading

    @property
    def active_segment(self) -> FrontLineSegment:
        """The FrontLine segment where there can be an active conflict"""
        if self._blue_route_progress <= self.segments[0].length:
            return self.segments[0]

        distance_to_segment = self._blue_route_progress
        for segment in self.segments:
            if distance_to_segment <= segment.length:
                return segment
            else:
                distance_to_segment -= segment.length
        logging.error(
            "Frontline attack distance is greater than the sum of its segments"
        )
        return self.segments[0]

    def point_along_route_from_blue(self, distance: float) -> Point:
        """Returns a point {distance} away from control_point_a along the route."""
        if distance < self.segments[0].length:
            return self.blue_cp.position.point_from_heading(
                self.segments[0].blue_forward_heading.degrees, distance
            )
        remaining_dist = distance
        for segment in self.segments:
            if remaining_dist < segment.length:
                return segment.point_a.point_from_heading(
                    segment.blue_forward_heading.degrees, remaining_dist
                )
            else:
                remaining_dist -= segment.length
        raise RuntimeError(
            f"Could not find front line point {distance} from {self.blue_cp}"
        )

    @property
    def _blue_route_progress(self) -> float:
        """
        The distance from point "a" where the conflict should occur
        according to the current strength of each control point
        """
        total_strength = self.blue_cp.base.strength + self.red_cp.base.strength
        if self.blue_cp.base.strength == 0:
            return self._adjust_for_min_dist(0)
        if self.red_cp.base.strength == 0:
            return self._adjust_for_min_dist(self.route_length)
        strength_pct = self.blue_cp.base.strength / total_strength
        return self._adjust_for_min_dist(strength_pct * self.route_length)

    def _adjust_for_min_dist(self, distance: float) -> float:
        """
        Ensures the frontline conflict is never located within the minimum distance
        constant of either end control point.
        """
        if (distance > self.route_length / 2) and (
            distance + FRONTLINE_MIN_CP_DISTANCE > self.route_length
        ):
            distance = self.route_length - FRONTLINE_MIN_CP_DISTANCE
        elif (distance < self.route_length / 2) and (
            distance < FRONTLINE_MIN_CP_DISTANCE
        ):
            distance = FRONTLINE_MIN_CP_DISTANCE
        return distance

    @staticmethod
    def sort_control_points(
        a: ControlPoint, b: ControlPoint
    ) -> tuple[ControlPoint, ControlPoint]:
        if a.is_friendly_to(b):
            raise ValueError(
                "Cannot sort control points that are friendly to each other"
            )
        if a.captured:
            return a, b
        return b, a
