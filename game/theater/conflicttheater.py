from __future__ import annotations

import itertools
import json
import logging
from dataclasses import dataclass
from functools import cached_property
from itertools import tee
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union, cast

from dcs import Mission
from dcs.countries import (
    CombinedJointTaskForcesBlue,
    CombinedJointTaskForcesRed,
)
from dcs.country import Country
from dcs.mapping import Point
from dcs.planes import F_15C
from dcs.ships import (
    CVN_74_John_C__Stennis,
    LHA_1_Tarawa,
    USS_Arleigh_Burke_IIa,
)
from dcs.statics import Fortification
from dcs.terrain import (
    caucasus,
    nevada,
    normandy,
    persiangulf,
    syria,
    thechannel,
)
from dcs.terrain.terrain import Airport, Terrain
from dcs.unitgroup import (
    FlyingGroup,
    Group,
    ShipGroup,
    StaticGroup,
    VehicleGroup,
)
from dcs.vehicles import AirDefence, Armor, MissilesSS

from gen.flights.flight import FlightType
from .controlpoint import (
    Airfield,
    Carrier,
    ControlPoint,
    Lha,
    MissionTarget,
    OffMapSpawn,
)
from .landmap import Landmap, load_landmap, poly_contains
from ..utils import nm_to_meter

Numeric = Union[int, float]

SIZE_TINY = 150
SIZE_SMALL = 600
SIZE_REGULAR = 1000
SIZE_BIG = 2000
SIZE_LARGE = 3000

IMPORTANCE_LOW = 1
IMPORTANCE_MEDIUM = 1.2
IMPORTANCE_HIGH = 1.4

FRONTLINE_MIN_CP_DISTANCE = 5000

def pairwise(iterable):
    """
    itertools recipe
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class MizCampaignLoader:
    BLUE_COUNTRY = CombinedJointTaskForcesBlue()
    RED_COUNTRY = CombinedJointTaskForcesRed()

    OFF_MAP_UNIT_TYPE = F_15C.id

    CV_UNIT_TYPE = CVN_74_John_C__Stennis.id
    LHA_UNIT_TYPE = LHA_1_Tarawa.id
    FRONT_LINE_UNIT_TYPE = Armor.APC_M113.id

    EWR_UNIT_TYPE = AirDefence.EWR_55G6.id
    SAM_UNIT_TYPE = AirDefence.SAM_SA_10_S_300PS_SR_64H6E.id
    GARRISON_UNIT_TYPE = AirDefence.SAM_SA_19_Tunguska_2S6.id
    OFFSHORE_STRIKE_TARGET_UNIT_TYPE = Fortification.Oil_platform.id
    SHIP_UNIT_TYPE = USS_Arleigh_Burke_IIa.id
    MISSILE_SITE_UNIT_TYPE = MissilesSS.SRBM_SS_1C_Scud_B_9K72_LN_9P117M.id
    COASTAL_DEFENSE_UNIT_TYPE = MissilesSS.SS_N_2_Silkworm.id

    # Multiple options for the required SAMs so campaign designers can more
    # easily see the coverage of their IADS. Designers focused on campaigns that
    # will primarily use SA-2s can place SA-2 launchers to ensure that they will
    # have adequate coverage, and designers focused on campaigns that will
    # primarily use SA-10s can do the same.
    REQUIRED_SAM_UNIT_TYPES = {
        AirDefence.SAM_Hawk_LN_M192,
        AirDefence.SAM_Patriot_LN_M901,
        AirDefence.SAM_SA_10_S_300PS_LN_5P85C,
        AirDefence.SAM_SA_10_S_300PS_LN_5P85D,
        AirDefence.SAM_SA_2_LN_SM_90,
        AirDefence.SAM_SA_3_S_125_LN_5P73,
    }

    BASE_DEFENSE_RADIUS = nm_to_meter(2)

    def __init__(self, miz: Path, theater: ConflictTheater) -> None:
        self.theater = theater
        self.mission = Mission()
        self.mission.load_file(str(miz))
        self.control_point_id = itertools.count(1000)

        # If there are no red carriers there usually aren't red units. Make sure
        # both countries are initialized so we don't have to deal with None.
        if self.mission.country(self.BLUE_COUNTRY.name) is None:
            self.mission.coalition["blue"].add_country(self.BLUE_COUNTRY)
        if self.mission.country(self.RED_COUNTRY.name) is None:
            self.mission.coalition["red"].add_country(self.RED_COUNTRY)

    @staticmethod
    def control_point_from_airport(airport: Airport) -> ControlPoint:

        # The wiki says this is a legacy property and to just use regular.
        size = SIZE_REGULAR

        # The importance is taken from the periodicity of the airport's
        # warehouse divided by 10. 30 is the default, and out of range (valid
        # values are between 1.0 and 1.4). If it is used, pick the default
        # importance.
        if airport.periodicity == 30:
            importance = IMPORTANCE_MEDIUM
        else:
            importance = airport.periodicity / 10

        cp = Airfield(airport, size, importance)
        cp.captured = airport.is_blue()

        # Use the unlimited aircraft option to determine if an airfield should
        # be owned by the player when the campaign is "inverted".
        cp.captured_invert = airport.unlimited_aircrafts

        return cp

    def country(self, blue: bool) -> Country:
        country = self.mission.country(
            self.BLUE_COUNTRY.name if blue else self.RED_COUNTRY.name)
        # Should be guaranteed because we initialized them.
        assert country
        return country

    @property
    def blue(self) -> Country:
        return self.country(blue=True)

    @property
    def red(self) -> Country:
        return self.country(blue=False)

    def off_map_spawns(self, blue: bool) -> Iterator[FlyingGroup]:
        for group in self.country(blue).plane_group:
            if group.units[0].type == self.OFF_MAP_UNIT_TYPE:
                yield group

    def carriers(self, blue: bool) -> Iterator[ShipGroup]:
        for group in self.country(blue).ship_group:
            if group.units[0].type == self.CV_UNIT_TYPE:
                yield group

    def lhas(self, blue: bool) -> Iterator[ShipGroup]:
        for group in self.country(blue).ship_group:
            if group.units[0].type == self.LHA_UNIT_TYPE:
                yield group

    @property
    def ships(self) -> Iterator[ShipGroup]:
        for group in self.blue.ship_group:
            if group.units[0].type == self.SHIP_UNIT_TYPE:
                yield group

    @property
    def ewrs(self) -> Iterator[VehicleGroup]:
        for group in self.blue.vehicle_group:
            if group.units[0].type == self.EWR_UNIT_TYPE:
                yield group

    @property
    def sams(self) -> Iterator[VehicleGroup]:
        for group in self.blue.vehicle_group:
            if group.units[0].type == self.SAM_UNIT_TYPE:
                yield group

    @property
    def garrisons(self) -> Iterator[VehicleGroup]:
        for group in self.blue.vehicle_group:
            if group.units[0].type == self.GARRISON_UNIT_TYPE:
                yield group

    @property
    def offshore_strike_targets(self) -> Iterator[StaticGroup]:
        for group in self.blue.static_group:
            if group.units[0].type == self.OFFSHORE_STRIKE_TARGET_UNIT_TYPE:
                yield group

    @property
    def missile_sites(self) -> Iterator[VehicleGroup]:
        for group in self.blue.vehicle_group:
            if group.units[0].type == self.MISSILE_SITE_UNIT_TYPE:
                yield group

    @property
    def coastal_defenses(self) -> Iterator[VehicleGroup]:
        for group in self.blue.vehicle_group:
            if group.units[0].type == self.COASTAL_DEFENSE_UNIT_TYPE:
                yield group

    @property
    def required_sams(self) -> Iterator[VehicleGroup]:
        for group in self.red.vehicle_group:
            if group.units[0].type == self.REQUIRED_SAM_UNIT_TYPES:
                yield group

    @cached_property
    def control_points(self) -> Dict[int, ControlPoint]:
        control_points = {}
        for airport in self.mission.terrain.airport_list():
            if airport.is_blue() or airport.is_red():
                control_point = self.control_point_from_airport(airport)
                control_points[control_point.id] = control_point

        for blue in (False, True):
            for group in self.off_map_spawns(blue):
                control_point = OffMapSpawn(next(self.control_point_id),
                                            str(group.name), group.position)
                control_point.captured = blue
                control_point.captured_invert = group.late_activation
                control_points[control_point.id] = control_point
            for group in self.carriers(blue):
                # TODO: Name the carrier.
                control_point = Carrier(
                    "carrier", group.position, next(self.control_point_id))
                control_point.captured = blue
                control_point.captured_invert = group.late_activation
                control_points[control_point.id] = control_point
            for group in self.lhas(blue):
                # TODO: Name the LHA.
                control_point = Lha(
                    "lha", group.position, next(self.control_point_id))
                control_point.captured = blue
                control_point.captured_invert = group.late_activation
                control_points[control_point.id] = control_point

        return control_points

    @property
    def front_line_path_groups(self) -> Iterator[VehicleGroup]:
        for group in self.country(blue=True).vehicle_group:
            if group.units[0].type == self.FRONT_LINE_UNIT_TYPE:
                yield group

    @cached_property
    def front_lines(self) -> Dict[str, ComplexFrontLine]:
        # Dict of front line ID to a front line.
        front_lines = {}
        for group in self.front_line_path_groups:
            # The unit will have its first waypoint at the source CP and the
            # final waypoint at the destination CP. Intermediate waypoints
            # define the curve of the front line.
            waypoints = [p.position for p in group.points]
            origin = self.mission.terrain.nearest_airport(waypoints[0])
            if origin is None:
                raise RuntimeError(
                    f"No airport near the first waypoint of {group.name}")
            destination = self.mission.terrain.nearest_airport(waypoints[-1])
            if destination is None:
                raise RuntimeError(
                    f"No airport near the final waypoint of {group.name}")

            # Snap the begin and end points to the control points.
            waypoints[0] = origin.position
            waypoints[-1] = destination.position
            front_line_id = f"{origin.id}|{destination.id}"
            front_lines[front_line_id] = ComplexFrontLine(origin, waypoints)
            self.control_points[origin.id].connect(
                self.control_points[destination.id])
            self.control_points[destination.id].connect(
                self.control_points[origin.id])
        return front_lines

    def objective_info(self, group: Group) -> Tuple[ControlPoint, int]:
        closest = self.theater.closest_control_point(group.position)
        distance = closest.position.distance_to_point(group.position)
        return closest, distance

    def add_preset_locations(self) -> None:
        for group in self.garrisons:
            closest, distance = self.objective_info(group)
            if distance < self.BASE_DEFENSE_RADIUS:
                closest.preset_locations.base_garrisons.append(group.position)
            else:
                logging.warning(
                    f"Found garrison unit too far from base: {group.name}")

        for group in self.sams:
            closest, distance = self.objective_info(group)
            if distance < self.BASE_DEFENSE_RADIUS:
                closest.preset_locations.base_air_defense.append(group.position)
            else:
                closest.preset_locations.strike_locations.append(group.position)

        for group in self.ewrs:
            closest, distance = self.objective_info(group)
            closest.preset_locations.ewrs.append(group.position)

        for group in self.offshore_strike_targets:
            closest, distance = self.objective_info(group)
            closest.preset_locations.offshore_strike_locations.append(
                group.position)

        for group in self.ships:
            closest, distance = self.objective_info(group)
            closest.preset_locations.ships.append(group.position)

        for group in self.missile_sites:
            closest, distance = self.objective_info(group)
            closest.preset_locations.missile_sites.append(group.position)

        for group in self.coastal_defenses:
            closest, distance = self.objective_info(group)
            closest.preset_locations.coastal_defenses.append(group.position)

        for group in self.required_sams:
            closest, distance = self.objective_info(group)
            closest.preset_locations.required_sams.append(group.position)

    def populate_theater(self) -> None:
        for control_point in self.control_points.values():
            self.theater.add_controlpoint(control_point)
        self.add_preset_locations()
        self.theater.set_frontline_data(self.front_lines)


class ConflictTheater:
    terrain: Terrain

    reference_points: Dict[Tuple[float, float], Tuple[float, float]]
    overview_image: str
    landmap: Optional[Landmap]
    """
    land_poly = None  # type: Polygon
    """
    daytime_map: Dict[str, Tuple[int, int]]
    _frontline_data: Optional[Dict[str, ComplexFrontLine]] = None

    def __init__(self):
        self.controlpoints: List[ControlPoint] = []
        self._frontline_data: Optional[Dict[str, ComplexFrontLine]] = None
        """
        self.land_poly = geometry.Polygon(self.landmap[0][0])
        for x in self.landmap[1]:
            self.land_poly = self.land_poly.difference(geometry.Polygon(x))
        """

    @property
    def frontline_data(self) -> Optional[Dict[str, ComplexFrontLine]]:
        if self._frontline_data is None:
            self.load_frontline_data_from_file()
        return self._frontline_data

    def load_frontline_data_from_file(self) -> None:
        if self._frontline_data is not None:
            logging.warning("Replacing existing frontline data from file")
        self._frontline_data = FrontLine.load_json_frontlines(self)
        if self._frontline_data is None:
            self._frontline_data = {}

    def set_frontline_data(self, data: Dict[str, ComplexFrontLine]) -> None:
        if self._frontline_data is not None:
            logging.warning("Replacing existing frontline data")
        self._frontline_data = data

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

    def closest_control_point(self, point: Point) -> ControlPoint:
        closest = self.controlpoints[0]
        closest_distance = point.distance_to_point(closest.position)
        for control_point in self.controlpoints[1:]:
            distance = point.distance_to_point(control_point.position)
            if distance < closest_distance:
                closest = control_point
                closest_distance = distance
        return closest
    
    def closest_opposing_control_points(self) -> Tuple[ControlPoint, ControlPoint]:
        """
        Returns a tuple of the two nearest opposing ControlPoints in theater.
        (player_cp, enemy_cp)
        """
        all_cp_min_distances = {}
        for idx, control_point in enumerate(self.controlpoints):
            distances = {}
            closest_distance = None
            for i, cp in enumerate(self.controlpoints):
                if i != idx and cp.captured is not control_point.captured:
                    dist = cp.position.distance_to_point(control_point.position)
                    if not closest_distance:
                        closest_distance = dist
                        distances[cp.id] = dist
                    if dist < closest_distance:
                        distances[cp.id] = dist
            closest_cp_id = min(distances, key=distances.get)

            all_cp_min_distances[(control_point.id, closest_cp_id)] = distances[closest_cp_id]
        closest_opposing_cps = [
            self.find_control_point_by_id(i)
            for i
            in min(all_cp_min_distances, key=all_cp_min_distances.get)
          ]  # type: List[ControlPoint]
        assert len(closest_opposing_cps) == 2
        if closest_opposing_cps[0].captured:
            return cast(Tuple[ControlPoint, ControlPoint], tuple(closest_opposing_cps))
        else:
            return cast(Tuple[ControlPoint, ControlPoint], tuple(reversed(closest_opposing_cps)))

    def find_control_point_by_id(self, id: int) -> ControlPoint:
        for i in self.controlpoints:
            if i.id == id:
                return i
        raise RuntimeError(f"Cannot find ControlPoint with ID {id}")

    def add_json_cp(self, theater, p: dict) -> ControlPoint:
        cp: ControlPoint
        if p["type"] == "airbase":

            airbase = theater.terrain.airports[p["id"]]

            if "size" in p.keys():
                size = p["size"]
            else:
                size = SIZE_REGULAR

            if "importance" in p.keys():
                importance = p["importance"]
            else:
                importance = IMPORTANCE_MEDIUM

            cp = Airfield(airbase, size, importance)
        elif p["type"] == "carrier":
            cp = Carrier("carrier", Point(p["x"], p["y"]), p["id"])
        else:
            cp = Lha("lha", Point(p["x"], p["y"]), p["id"])

        if "captured_invert" in p.keys():
            cp.captured_invert = p["captured_invert"]
        else:
            cp.captured_invert = False

        return cp
        
    @staticmethod
    def from_json(directory: Path, data: Dict[str, Any]) -> ConflictTheater:
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

        miz = data.get("miz", None)
        if miz is not None:
            MizCampaignLoader(directory / miz, t).populate_theater()
            return t

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

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        yield from [
            FlightType.CAS,
            # TODO: FlightType.TROOP_TRANSPORT
            # TODO: FlightType.EVAC
        ]
        yield from super().mission_types(for_player)

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
