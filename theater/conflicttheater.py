from __future__ import annotations

import logging
import json
from dataclasses import dataclass
from itertools import tee
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

from dcs.mapping import Point
from dcs.terrain import (
    caucasus,
    nevada,
    normandy,
    persiangulf,
    syria,
    thechannel,
)
from dcs.terrain.terrain import Terrain

from .controlpoint import ControlPoint, MissionTarget
from .landmap import Landmap, load_landmap, poly_contains

Numeric = Union[int, float]

SIZE_TINY = 150
SIZE_SMALL = 600
SIZE_REGULAR = 1000
SIZE_BIG = 2000
SIZE_LARGE = 3000

IMPORTANCE_LOW = 1
IMPORTANCE_MEDIUM = 1.2
IMPORTANCE_HIGH = 1.4

"""
ALL_RADIALS = [0, 45, 90, 135, 180, 225, 270, 315, ]
COAST_NS_E = [45, 90, 135, ]
COAST_EW_N = [315, 0, 45, ]
COAST_NSEW_E = [225, 270, 315, ]
COAST_NSEW_W = [45, 90, 135, ]

COAST_NS_W = [225, 270, 315, ]
COAST_EW_S = [135, 180, 225, ]
"""

LAND = [0, 45, 90, 135, 180, 225, 270, 315, ]

COAST_V_E = [0, 45, 90, 135, 180]
COAST_V_W = [180, 225, 270, 315, 0]

COAST_A_W = [315, 0, 45, 135, 180, 225, 270]
COAST_A_E = [0, 45, 90, 135, 180, 225, 315]

COAST_H_N = [270, 315, 0, 45, 90]
COAST_H_S = [90, 135, 180, 225, 270]

COAST_DL_E = [45, 90, 135, 180, 225]
COAST_DL_W = [225, 270, 315, 0, 45]
COAST_DR_E = [315, 0, 45, 90, 135]
COAST_DR_W = [135, 180, 225, 315]

FRONTLINE_MIN_CP_DISTANCE = 5000

def pairwise(iterable):
    """
    itertools recipe
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class ConflictTheater:
    terrain: Terrain

    reference_points: Dict[Tuple[float, float], Tuple[float, float]]
    overview_image: str
    landmap: Optional[Landmap]
    """
    land_poly = None  # type: Polygon
    """
    daytime_map: Dict[str, Tuple[int, int]]
    frontline_data: Optional[Dict[str, ComplexFrontLine]] = None

    def __init__(self):
        self.controlpoints: List[ControlPoint] = []
        self.frontline_data = FrontLine.load_json_frontlines(self)
        """
        self.land_poly = geometry.Polygon(self.landmap[0][0])
        for x in self.landmap[1]:
            self.land_poly = self.land_poly.difference(geometry.Polygon(x))
        """

    def add_controlpoint(self, point: ControlPoint,
                         connected_to: Optional[List[ControlPoint]] = None):
        if connected_to is None:
            connected_to = []
        for connected_point in connected_to:
            point.connect(to=connected_point)

        self.controlpoints.append(point)

    def find_ground_objects_by_obj_name(self, obj_name):
        found = []
        for cp in self.controlpoints:
            for g in cp.ground_objects:
                if g.obj_name == obj_name:
                    found.append(g)
        return found

    def is_in_sea(self, point: Point) -> bool:
        if not self.landmap:
            return False

        if self.is_on_land(point):
            return False

        for sea in self.landmap[2]:
            if poly_contains(point.x, point.y, sea):
                return True

        return False

    def is_on_land(self, point: Point) -> bool:
        if not self.landmap:
            return True

        is_point_included = False
        for inclusion_zone in self.landmap[0]:
            if poly_contains(point.x, point.y, inclusion_zone):
                is_point_included = True

        if not is_point_included:
            return False

        for exclusion_zone in self.landmap[1]:
            if poly_contains(point.x, point.y, exclusion_zone):
                return False

        return True

    def player_points(self) -> List[ControlPoint]:
        return [point for point in self.controlpoints if point.captured]

    def conflicts(self, from_player=True) -> Iterator[FrontLine]:
        for cp in [x for x in self.controlpoints if x.captured == from_player]:
            for connected_point in [x for x in cp.connected_points if x.captured != from_player]:
                yield FrontLine(cp, connected_point, self)

    def enemy_points(self) -> List[ControlPoint]:
        return [point for point in self.controlpoints if not point.captured]

    def add_json_cp(self, theater, p: dict) -> ControlPoint:

        if p["type"] == "airbase":

            airbase = theater.terrain.airports[p["id"]].__class__

            if "radials" in p.keys():
                radials = p["radials"]
            else:
                radials = LAND

            if "size" in p.keys():
                size = p["size"]
            else:
                size = SIZE_REGULAR

            if "importance" in p.keys():
                importance = p["importance"]
            else:
                importance = IMPORTANCE_MEDIUM

            cp = ControlPoint.from_airport(airbase, radials, size, importance)
        elif p["type"] == "carrier":
            cp = ControlPoint.carrier("carrier", Point(p["x"], p["y"]), p["id"])
        else:
            cp = ControlPoint.lha("lha", Point(p["x"], p["y"]), p["id"])

        if "captured_invert" in p.keys():
            cp.captured_invert = p["captured_invert"]
        else:
            cp.captured_invert = False

        return cp
        
    @staticmethod
    def from_json(data: Dict[str, Any]) -> ConflictTheater:
        theaters = {
            "Caucasus": CaucasusTheater,
            "Nevada": NevadaTheater,
            "Persian Gulf": PersianGulfTheater,
            "Normandy": NormandyTheater,
            "The Channel": TheChannelTheater,
            "Syria": SyriaTheater,
        }
        theater = theaters[data["theater"]]
        t = theater()
        cps = {}
        for p in data["player_points"]:
            cp = t.add_json_cp(theater, p)
            cp.captured = True
            cps[p["id"]] = cp
            t.add_controlpoint(cp)

        for p in data["enemy_points"]:
            cp = t.add_json_cp(theater, p)
            cps[p["id"]] = cp
            t.add_controlpoint(cp)

        for l in data["links"]:
            cps[l[0]].connect(cps[l[1]])
            cps[l[1]].connect(cps[l[0]])

        return t
    

class CaucasusTheater(ConflictTheater):
    terrain = caucasus.Caucasus()
    overview_image = "caumap.gif"
    reference_points = {(-317948.32727306, 635639.37385346): (278.5 * 4, 319 * 4),
                        (-355692.3067714, 617269.96285781): (263 * 4, 352 * 4), }

    landmap = load_landmap("resources\\caulandmap.p")
    daytime_map = {
        "dawn": (6, 9),
        "day": (9, 18),
        "dusk": (18, 20),
        "night": (0, 5),
    }


class PersianGulfTheater(ConflictTheater):
    terrain = persiangulf.PersianGulf()
    overview_image = "persiangulf.gif"
    reference_points = {
        (persiangulf.Shiraz_International_Airport.position.x, persiangulf.Shiraz_International_Airport.position.y): (
        772, -1970),
        (persiangulf.Liwa_Airbase.position.x, persiangulf.Liwa_Airbase.position.y): (1188, 78), }
    landmap = load_landmap("resources\\gulflandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }

class NevadaTheater(ConflictTheater):
    terrain = nevada.Nevada()
    overview_image = "nevada.gif"
    reference_points = {(nevada.Mina_Airport_3Q0.position.x, nevada.Mina_Airport_3Q0.position.y): (45 * 2, -360 * 2),
                        (nevada.Laughlin_Airport.position.x, nevada.Laughlin_Airport.position.y): (440 * 2, 80 * 2), }
    landmap = load_landmap("resources\\nevlandmap.p")
    daytime_map = {
        "dawn": (4, 6),
        "day": (6, 17),
        "dusk": (17, 18),
        "night": (0, 5),
    }

class NormandyTheater(ConflictTheater):
    terrain = normandy.Normandy()
    overview_image = "normandy.gif"
    reference_points = {(normandy.Needs_Oar_Point.position.x, normandy.Needs_Oar_Point.position.y): (-170, -1000),
                        (normandy.Evreux.position.x, normandy.Evreux.position.y): (2020, 500)}
    landmap = load_landmap("resources\\normandylandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (10, 17),
        "dusk": (17, 18),
        "night": (0, 5),
    }

class TheChannelTheater(ConflictTheater):
    terrain = thechannel.TheChannel()
    overview_image = "thechannel.gif"
    reference_points = {(thechannel.Abbeville_Drucat.position.x, thechannel.Abbeville_Drucat.position.y): (2400, 4100),
                        (thechannel.Detling.position.x, thechannel.Detling.position.y): (1100, 2000)}
    landmap = load_landmap("resources\\channellandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (10, 17),
        "dusk": (17, 18),
        "night": (0, 5),
    }

class SyriaTheater(ConflictTheater):
    terrain = syria.Syria()
    overview_image = "syria.gif"
    reference_points = {(syria.Eyn_Shemer.position.x, syria.Eyn_Shemer.position.y): (1300, 1380),
                        (syria.Tabqa.position.x, syria.Tabqa.position.y): (2060, 570)}
    landmap = load_landmap("resources\\syrialandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }

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

    def __init__(
        self,
        control_point_a: ControlPoint,
        control_point_b: ControlPoint,
        theater: ConflictTheater
    ) -> None:
        self.control_point_a = control_point_a
        self.control_point_b = control_point_b
        self.segments: List[FrontLineSegment] = []
        self.theater = theater
        self._build_segments()
        self.name = f"Front line {control_point_a}/{control_point_b}"

    def is_friendly(self, to_player: bool) -> bool:
        """Returns True if the objective is in friendly territory."""
        return False

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


    @staticmethod
    def load_json_frontlines(
        theater: ConflictTheater
    ) -> Optional[Dict[str, ComplexFrontLine]]:
        """Load complex frontlines from json"""
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
