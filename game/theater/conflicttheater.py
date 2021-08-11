from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, TYPE_CHECKING

from dcs.mapping import Point
from dcs.terrain import (
    caucasus,
    nevada,
    normandy,
    persiangulf,
    syria,
    thechannel,
    marianaislands,
)
from dcs.terrain.terrain import Terrain
from pyproj import CRS, Transformer
from shapely import geometry, ops

from .controlpoint import (
    ControlPoint,
    MissionTarget,
)
from .mizcampaignloader import MizCampaignLoader
from .seasonalconditions import SeasonalConditions
from .frontline import FrontLine
from .landmap import Landmap, load_landmap, poly_contains
from .latlon import LatLon
from .projections import TransverseMercator
from ..profiling import logged_duration

if TYPE_CHECKING:
    from . import TheaterGroundObject


@dataclass
class ReferencePoint:
    world_coordinates: Point
    image_coordinates: Point


class ConflictTheater:
    terrain: Terrain

    reference_points: Tuple[ReferencePoint, ReferencePoint]
    overview_image: str
    landmap: Optional[Landmap]
    """
    land_poly = None  # type: Polygon
    """
    daytime_map: Dict[str, Tuple[int, int]]

    def __init__(self) -> None:
        self.controlpoints: List[ControlPoint] = []
        self.point_to_ll_transformer = Transformer.from_crs(
            self.projection_parameters.to_crs(), CRS("WGS84")
        )
        self.ll_to_point_transformer = Transformer.from_crs(
            CRS("WGS84"), self.projection_parameters.to_crs()
        )
        """
        self.land_poly = geometry.Polygon(self.landmap[0][0])
        for x in self.landmap[1]:
            self.land_poly = self.land_poly.difference(geometry.Polygon(x))
        """

    def __getstate__(self) -> Dict[str, Any]:
        state = self.__dict__.copy()
        # Avoid persisting any volatile types that can be deterministically
        # recomputed on load for the sake of save compatibility.
        del state["point_to_ll_transformer"]
        del state["ll_to_point_transformer"]
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__.update(state)
        # Regenerate any state that was not persisted.
        self.point_to_ll_transformer = Transformer.from_crs(
            self.projection_parameters.to_crs(), CRS("WGS84")
        )
        self.ll_to_point_transformer = Transformer.from_crs(
            CRS("WGS84"), self.projection_parameters.to_crs()
        )

    def add_controlpoint(self, point: ControlPoint) -> None:
        self.controlpoints.append(point)

    def find_ground_objects_by_obj_name(
        self, obj_name: str
    ) -> list[TheaterGroundObject[Any]]:
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

        for exclusion_zone in self.landmap.exclusion_zones:
            if poly_contains(point.x, point.y, exclusion_zone):
                return False

        for sea in self.landmap.sea_zones:
            if poly_contains(point.x, point.y, sea):
                return True

        return False

    def is_on_land(self, point: Point) -> bool:
        if not self.landmap:
            return True

        is_point_included = False
        if poly_contains(point.x, point.y, self.landmap.inclusion_zones):
            is_point_included = True

        if not is_point_included:
            return False

        for exclusion_zone in self.landmap.exclusion_zones:
            if poly_contains(point.x, point.y, exclusion_zone):
                return False

        return True

    def nearest_land_pos(self, near: Point, extend_dist: int = 50) -> Point:
        """Returns the nearest point inside a land exclusion zone from point
        `extend_dist` determines how far inside the zone the point should be placed"""
        if self.is_on_land(near):
            return near
        point = geometry.Point(near.x, near.y)
        nearest_points = []
        if not self.landmap:
            raise RuntimeError("Landmap not initialized")
        for inclusion_zone in self.landmap.inclusion_zones:
            nearest_pair = ops.nearest_points(point, inclusion_zone)
            nearest_points.append(nearest_pair[1])
        min_distance = point.distance(nearest_points[0])  # type: geometry.Point
        nearest_point = nearest_points[0]  # type: geometry.Point
        for pt in nearest_points[1:]:
            distance = point.distance(pt)
            if distance < min_distance:
                min_distance = distance
                nearest_point = pt
        assert isinstance(nearest_point, geometry.Point)
        point = Point(point.x, point.y)
        nearest_point = Point(nearest_point.x, nearest_point.y)
        new_point = point.point_from_heading(
            point.heading_between_point(nearest_point),
            point.distance_to_point(nearest_point) + extend_dist,
        )
        return new_point

    def control_points_for(self, player: bool) -> Iterator[ControlPoint]:
        for point in self.controlpoints:
            if point.captured == player:
                yield point

    def player_points(self) -> List[ControlPoint]:
        return list(self.control_points_for(player=True))

    def conflicts(self) -> Iterator[FrontLine]:
        for player_cp in [x for x in self.controlpoints if x.captured]:
            for enemy_cp in [
                x for x in player_cp.connected_points if not x.is_friendly_to(player_cp)
            ]:
                yield FrontLine(player_cp, enemy_cp)

    def enemy_points(self) -> List[ControlPoint]:
        return list(self.control_points_for(player=False))

    def closest_control_point(
        self, point: Point, allow_naval: bool = False
    ) -> ControlPoint:
        closest = self.controlpoints[0]
        closest_distance = point.distance_to_point(closest.position)
        for control_point in self.controlpoints[1:]:
            if control_point.is_fleet and not allow_naval:
                continue
            distance = point.distance_to_point(control_point.position)
            if distance < closest_distance:
                closest = control_point
                closest_distance = distance
        return closest

    def closest_target(self, point: Point) -> MissionTarget:
        closest: MissionTarget = self.controlpoints[0]
        closest_distance = point.distance_to_point(closest.position)
        for control_point in self.controlpoints[1:]:
            distance = point.distance_to_point(control_point.position)
            if distance < closest_distance:
                closest = control_point
                closest_distance = distance
            for tgo in control_point.ground_objects:
                distance = point.distance_to_point(tgo.position)
                if distance < closest_distance:
                    closest = tgo
                    closest_distance = distance
        for conflict in self.conflicts():
            distance = conflict.position.distance_to_point(point)
            if distance < closest_distance:
                closest = conflict
                closest_distance = distance
        return closest

    def closest_opposing_control_points(self) -> Tuple[ControlPoint, ControlPoint]:
        """
        Returns a tuple of the two nearest opposing ControlPoints in theater.
        (player_cp, enemy_cp)
        """
        seen = set()
        min_distance = math.inf
        closest_blue = None
        closest_red = None
        for blue_cp in self.player_points():
            for red_cp in self.enemy_points():
                if (blue_cp, red_cp) in seen:
                    continue
                seen.add((blue_cp, red_cp))
                seen.add((red_cp, blue_cp))

                dist = red_cp.position.distance_to_point(blue_cp.position)
                if dist < min_distance:
                    closest_red = red_cp
                    closest_blue = blue_cp
                    min_distance = dist

        assert closest_blue is not None
        assert closest_red is not None
        return closest_blue, closest_red

    def find_control_point_by_id(self, id: int) -> ControlPoint:
        for i in self.controlpoints:
            if i.id == id:
                return i
        raise KeyError(f"Cannot find ControlPoint with ID {id}")

    @staticmethod
    def from_file_data(directory: Path, data: Dict[str, Any]) -> ConflictTheater:
        theaters = {
            "Caucasus": CaucasusTheater,
            "Nevada": NevadaTheater,
            "Persian Gulf": PersianGulfTheater,
            "Normandy": NormandyTheater,
            "The Channel": TheChannelTheater,
            "Syria": SyriaTheater,
            "MarianaIslands": MarianaIslandsTheater,
        }
        theater = theaters[data["theater"]]
        t = theater()

        miz = data.get("miz", None)
        if miz is None:
            raise RuntimeError(
                "Old format (non-miz) campaigns are no longer supported."
            )

        with logged_duration("Importing miz data"):
            MizCampaignLoader(directory / miz, t).populate_theater()
        return t

    @property
    def seasonal_conditions(self) -> SeasonalConditions:
        raise NotImplementedError

    @property
    def projection_parameters(self) -> TransverseMercator:
        raise NotImplementedError

    def point_to_ll(self, point: Point) -> LatLon:
        lat, lon = self.point_to_ll_transformer.transform(point.x, point.y)
        return LatLon(lat, lon)

    def ll_to_point(self, ll: LatLon) -> Point:
        x, y = self.ll_to_point_transformer.transform(ll.latitude, ll.longitude)
        return Point(x, y)


class CaucasusTheater(ConflictTheater):
    terrain = caucasus.Caucasus()
    overview_image = "caumap.gif"
    reference_points = (
        ReferencePoint(caucasus.Gelendzhik.position, Point(176, 298)),
        ReferencePoint(caucasus.Batumi.position, Point(1307, 1205)),
    )

    landmap = load_landmap("resources\\caulandmap.p")
    daytime_map = {
        "dawn": (6, 9),
        "day": (9, 18),
        "dusk": (18, 20),
        "night": (0, 5),
    }

    @property
    def seasonal_conditions(self) -> SeasonalConditions:
        from .seasonalconditions.caucasus import CONDITIONS

        return CONDITIONS

    @property
    def projection_parameters(self) -> TransverseMercator:
        from .caucasus import PARAMETERS

        return PARAMETERS


class PersianGulfTheater(ConflictTheater):
    terrain = persiangulf.PersianGulf()
    overview_image = "persiangulf.gif"
    reference_points = (
        ReferencePoint(persiangulf.Jiroft.position, Point(1692, 1343)),
        ReferencePoint(persiangulf.Liwa_AFB.position, Point(358, 3238)),
    )
    landmap = load_landmap("resources\\gulflandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }

    @property
    def seasonal_conditions(self) -> SeasonalConditions:
        from .seasonalconditions.persiangulf import CONDITIONS

        return CONDITIONS

    @property
    def projection_parameters(self) -> TransverseMercator:
        from .persiangulf import PARAMETERS

        return PARAMETERS


class NevadaTheater(ConflictTheater):
    terrain = nevada.Nevada()
    overview_image = "nevada.gif"
    reference_points = (
        ReferencePoint(nevada.Mina_Airport_3Q0.position, Point(252, 295)),
        ReferencePoint(nevada.Laughlin_Airport.position, Point(844, 909)),
    )
    landmap = load_landmap("resources\\nevlandmap.p")
    daytime_map = {
        "dawn": (4, 6),
        "day": (6, 17),
        "dusk": (17, 18),
        "night": (0, 5),
    }

    @property
    def seasonal_conditions(self) -> SeasonalConditions:
        from .seasonalconditions.nevada import CONDITIONS

        return CONDITIONS

    @property
    def projection_parameters(self) -> TransverseMercator:
        from .nevada import PARAMETERS

        return PARAMETERS


class NormandyTheater(ConflictTheater):
    terrain = normandy.Normandy()
    overview_image = "normandy.gif"
    reference_points = (
        ReferencePoint(normandy.Needs_Oar_Point.position, Point(515, 329)),
        ReferencePoint(normandy.Evreux.position, Point(2029, 1709)),
    )
    landmap = load_landmap("resources\\normandylandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (10, 17),
        "dusk": (17, 18),
        "night": (0, 5),
    }

    @property
    def seasonal_conditions(self) -> SeasonalConditions:
        from .seasonalconditions.normandy import CONDITIONS

        return CONDITIONS

    @property
    def projection_parameters(self) -> TransverseMercator:
        from .normandy import PARAMETERS

        return PARAMETERS


class TheChannelTheater(ConflictTheater):
    terrain = thechannel.TheChannel()
    overview_image = "thechannel.gif"
    reference_points = (
        ReferencePoint(thechannel.Abbeville_Drucat.position, Point(2005, 2390)),
        ReferencePoint(thechannel.Detling.position, Point(706, 382)),
    )
    landmap = load_landmap("resources\\channellandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (10, 17),
        "dusk": (17, 18),
        "night": (0, 5),
    }

    @property
    def seasonal_conditions(self) -> SeasonalConditions:
        from .seasonalconditions.thechannel import CONDITIONS

        return CONDITIONS

    @property
    def projection_parameters(self) -> TransverseMercator:
        from .thechannel import PARAMETERS

        return PARAMETERS


class SyriaTheater(ConflictTheater):
    terrain = syria.Syria()
    overview_image = "syria.gif"
    reference_points = (
        ReferencePoint(syria.Eyn_Shemer.position, Point(564, 1289)),
        ReferencePoint(syria.Tabqa.position, Point(1329, 491)),
    )
    landmap = load_landmap("resources\\syrialandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }

    @property
    def seasonal_conditions(self) -> SeasonalConditions:
        from .seasonalconditions.syria import CONDITIONS

        return CONDITIONS

    @property
    def projection_parameters(self) -> TransverseMercator:
        from .syria import PARAMETERS

        return PARAMETERS


class MarianaIslandsTheater(ConflictTheater):
    terrain = marianaislands.MarianaIslands()
    overview_image = "marianaislands.gif"

    landmap = load_landmap("resources\\marianaislandslandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }

    @property
    def seasonal_conditions(self) -> SeasonalConditions:
        from .seasonalconditions.marianaislands import CONDITIONS

        return CONDITIONS

    @property
    def projection_parameters(self) -> TransverseMercator:
        from .marianaislands import PARAMETERS

        return PARAMETERS
