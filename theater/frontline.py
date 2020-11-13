"""Battlefield front lines."""
from __future__ import annotations


import logging
import json
from dataclasses import dataclass
from pathlib import Path
from itertools import tee
from typing import Tuple, List, Union, Dict, Optional, TYPE_CHECKING

from dcs.mapping import Point

from .controlpoint import ControlPoint, MissionTarget

if TYPE_CHECKING:
    from theater.conflicttheater import ConflictTheater

Numeric = Union[int, float]

# TODO: Dedup by moving everything to using this class.
FRONTLINE_MIN_CP_DISTANCE = 5000


def pairwise(iterable):
    """
    itertools recipe
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


@dataclass
class ComplexFrontLine:
    """
    Stores data necessary for building a multi-segment frontline.
    "points" should be ordered from closest to farthest distance originating from start_cp.position
    """

    start_cp: ControlPoint
    points: List[Point]


@dataclass
class FrontLineSegment:
    """
    Describes a line segment of a FrontLine
    """

    point_a: Point
    point_b: Point

    @property
    def attack_heading(self) -> Numeric:
        """The heading of the frontline segment from player to enemy control point"""
        return self.point_a.heading_between_point(self.point_b)

    @property
    def attack_distance(self) -> Numeric:
        """Length of the segment"""
        return self.point_a.distance_to_point(self.point_b)


class FrontLine(MissionTarget):
    """Defines a front line location between two control points.
    Front lines are the area where ground combat happens.
    Overwrites the entirety of MissionTarget __init__ method to allow for
    dynamic position calculation.
    """

    theater: ConflictTheater

    def __init__(
        self,
        control_point_a: ControlPoint,
        control_point_b: ControlPoint,
    ) -> None:
        self.control_point_a = control_point_a
        self.control_point_b = control_point_b
        self.segments: List[FrontLineSegment] = []
        self._build_segments()
        self.name = f"Front line {control_point_a}/{control_point_b}"

    @property
    def position(self):
        """
        The position where the conflict should occur
        according to the current strength of each control point.
        """
        return self.point_from_a(self._position_distance)

    @property
    def control_points(self) -> Tuple[ControlPoint, ControlPoint]:
        """Returns a tuple of the two control points."""
        return self.control_point_a, self.control_point_b

    @property
    def middle_point(self):
        self.point_from_a(self.attack_distance / 2)

    @property
    def attack_distance(self):
        """The total distance of all segments"""
        return sum(i.attack_distance for i in self.segments)

    @property
    def attack_heading(self):
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

    def point_from_a(self, distance: Numeric) -> Point:
        """
        Returns a point {distance} away from control_point_a along the frontline segments.
        """
        if distance < self.segments[0].attack_distance:
            return self.control_point_a.position.point_from_heading(
                self.segments[0].attack_heading, distance
            )
        remaining_dist = distance
        for segment in self.segments:
            if remaining_dist < segment.attack_distance:
                return segment.point_a.point_from_heading(
                    segment.attack_heading, remaining_dist
                )
            else:
                remaining_dist -= segment.attack_distance

    @property
    def _position_distance(self) -> float:
        """
        The distance from point "a" where the conflict should occur
        according to the current strength of each control point
        """
        total_strength = (
            self.control_point_a.base.strength + self.control_point_b.base.strength
        )
        if self.control_point_a.base.strength == 0:
            return self._adjust_for_min_dist(0)
        if self.control_point_b.base.strength == 0:
            return self._adjust_for_min_dist(self.attack_distance)
        strength_pct = self.control_point_a.base.strength / total_strength
        return self._adjust_for_min_dist(strength_pct * self.attack_distance)

    def _adjust_for_min_dist(self, distance: Numeric) -> Numeric:
        """
        Ensures the frontline conflict is never located within the minimum distance
        constant of either end control point.
        """
        if (distance > self.attack_distance / 2) and (
            distance + FRONTLINE_MIN_CP_DISTANCE > self.attack_distance
        ):
            distance = self.attack_distance - FRONTLINE_MIN_CP_DISTANCE
        elif (distance < self.attack_distance / 2) and (
            distance < FRONTLINE_MIN_CP_DISTANCE
        ):
            distance = FRONTLINE_MIN_CP_DISTANCE
        return distance

    def _build_segments(self) -> None:
        """Create line segments for the frontline"""
        control_point_ids = "|".join(
            [str(self.control_point_a.id), str(self.control_point_b.id)]
        )  # from_cp.id|to_cp.id
        reversed_cp_ids = "|".join(
            [str(self.control_point_b.id), str(self.control_point_a.id)]
        )
        complex_frontlines = self.theater.frontline_data
        if (complex_frontlines) and (
            (control_point_ids in complex_frontlines)
            or (reversed_cp_ids in complex_frontlines)
        ):
            # The frontline segments must be stored in the correct order for the distance algorithms to work.
            # The points in the frontline are ordered from the id before the | to the id after.
            # First, check if control point id pair matches in order, and create segments if a match is found.
            if control_point_ids in complex_frontlines:
                point_pairs = pairwise(complex_frontlines[control_point_ids].points)
                for i in point_pairs:
                    self.segments.append(FrontLineSegment(i[0], i[1]))
            # Check the reverse order and build in reverse if found.
            elif reversed_cp_ids in complex_frontlines:
                point_pairs = pairwise(
                    reversed(complex_frontlines[reversed_cp_ids].points)
                )
                for i in point_pairs:
                    self.segments.append(FrontLineSegment(i[0], i[1]))
        # If no complex frontline has been configured, fall back to the old straight line method.
        else:
            self.segments.append(
                FrontLineSegment(
                    self.control_point_a.position, self.control_point_b.position
                )
            )

    @classmethod
    def load_json_frontlines(
        cls, theater: ConflictTheater
    ) -> Optional[Dict[str, ComplexFrontLine]]:
        """Load complex frontlines from json and set the theater class variable to current theater instance"""
        cls.theater = theater
        try:
            path = Path(f"resources/frontlines/{theater.terrain.name.lower()}.json")
            with open(path, "r") as file:
                logging.debug(f"Loading frontline from {path}...")
                data = json.load(file)
            return {
                frontline: ComplexFrontLine(
                    data[frontline]["start_cp"],
                    [Point(i[0], i[1]) for i in data[frontline]["points"]],
                )
                for frontline in data
            }
        except OSError:
            logging.warning(
                f"Unable to load preset frontlines for {theater.terrain.name}"
            )
            return None
