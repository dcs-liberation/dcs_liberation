from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple

from dcs import Mission
from dcs.countries import (
    CombinedJointTaskForcesBlue,
    CombinedJointTaskForcesRed,
)
from dcs.country import Country
from dcs.mapping import Point
from dcs.planes import F_15C
from dcs.ships import (
    Bulker_Handy_Wind,
    CVN_74_John_C__Stennis,
    DDG_Arleigh_Burke_IIa,
    LHA_1_Tarawa,
)
from dcs.statics import Fortification, Warehouse
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
from dcs.vehicles import AirDefence, Armor, MissilesSS, Unarmed
from pyproj import CRS, Transformer
from shapely import geometry, ops

from .controlpoint import (
    Airfield,
    Carrier,
    ControlPoint,
    Fob,
    Lha,
    MissionTarget,
    OffMapSpawn,
)
from .frontline import FrontLine
from .landmap import Landmap, load_landmap, poly_contains
from .latlon import LatLon
from .projections import TransverseMercator
from ..helipad import Helipad
from ..point_with_heading import PointWithHeading
from ..profiling import logged_duration
from ..scenery_group import SceneryGroup
from ..utils import Distance, meters

SIZE_TINY = 150
SIZE_SMALL = 600
SIZE_REGULAR = 1000
SIZE_BIG = 2000
SIZE_LARGE = 3000

IMPORTANCE_LOW = 1
IMPORTANCE_MEDIUM = 1.2
IMPORTANCE_HIGH = 1.4


class MizCampaignLoader:
    BLUE_COUNTRY = CombinedJointTaskForcesBlue()
    RED_COUNTRY = CombinedJointTaskForcesRed()

    OFF_MAP_UNIT_TYPE = F_15C.id

    CV_UNIT_TYPE = CVN_74_John_C__Stennis.id
    LHA_UNIT_TYPE = LHA_1_Tarawa.id
    FRONT_LINE_UNIT_TYPE = Armor.APC_M113.id
    SHIPPING_LANE_UNIT_TYPE = Bulker_Handy_Wind.id

    FOB_UNIT_TYPE = Unarmed.Truck_SKP_11_Mobile_ATC.id
    FARP_HELIPAD = "SINGLE_HELIPAD"

    OFFSHORE_STRIKE_TARGET_UNIT_TYPE = Fortification.Oil_platform.id
    SHIP_UNIT_TYPE = DDG_Arleigh_Burke_IIa.id
    MISSILE_SITE_UNIT_TYPE = MissilesSS.SSM_SS_1C_Scud_B.id
    COASTAL_DEFENSE_UNIT_TYPE = MissilesSS.AShM_SS_N_2_Silkworm.id

    # Multiple options for air defenses so campaign designers can more accurately see
    # the coverage of their IADS for the expected type.
    LONG_RANGE_SAM_UNIT_TYPES = {
        AirDefence.SAM_Patriot_LN.id,
        AirDefence.SAM_SA_10_S_300_Grumble_TEL_C.id,
        AirDefence.SAM_SA_10_S_300_Grumble_TEL_D.id,
    }

    MEDIUM_RANGE_SAM_UNIT_TYPES = {
        AirDefence.SAM_Hawk_LN_M192.id,
        AirDefence.SAM_SA_2_S_75_Guideline_LN.id,
        AirDefence.SAM_SA_3_S_125_Goa_LN.id,
    }

    SHORT_RANGE_SAM_UNIT_TYPES = {
        AirDefence.SAM_Avenger__Stinger.id,
        AirDefence.SAM_Rapier_LN.id,
        AirDefence.SAM_SA_19_Tunguska_Grison.id,
        AirDefence.SAM_SA_9_Strela_1_Gaskin_TEL.id,
    }

    AAA_UNIT_TYPES = {
        AirDefence.AAA_8_8cm_Flak_18.id,
        AirDefence.SPAAA_Vulcan_M163.id,
        AirDefence.SPAAA_ZSU_23_4_Shilka_Gun_Dish.id,
    }

    EWR_UNIT_TYPE = AirDefence.EWR_1L13.id

    ARMOR_GROUP_UNIT_TYPE = Armor.MBT_M1A2_Abrams.id

    FACTORY_UNIT_TYPE = Fortification.Workshop_A.id

    AMMUNITION_DEPOT_UNIT_TYPE = Warehouse.Ammunition_depot.id

    STRIKE_TARGET_UNIT_TYPE = Fortification.Tech_combine.id

    def __init__(self, miz: Path, theater: ConflictTheater) -> None:
        self.theater = theater
        self.mission = Mission()
        with logged_duration("Loading miz"):
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
            self.BLUE_COUNTRY.name if blue else self.RED_COUNTRY.name
        )
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

    def fobs(self, blue: bool) -> Iterator[VehicleGroup]:
        for group in self.country(blue).vehicle_group:
            if group.units[0].type == self.FOB_UNIT_TYPE:
                yield group

    @property
    def ships(self) -> Iterator[ShipGroup]:
        for group in self.red.ship_group:
            if group.units[0].type == self.SHIP_UNIT_TYPE:
                yield group

    @property
    def offshore_strike_targets(self) -> Iterator[StaticGroup]:
        for group in self.red.static_group:
            if group.units[0].type == self.OFFSHORE_STRIKE_TARGET_UNIT_TYPE:
                yield group

    @property
    def missile_sites(self) -> Iterator[VehicleGroup]:
        for group in self.red.vehicle_group:
            if group.units[0].type == self.MISSILE_SITE_UNIT_TYPE:
                yield group

    @property
    def coastal_defenses(self) -> Iterator[VehicleGroup]:
        for group in self.red.vehicle_group:
            if group.units[0].type == self.COASTAL_DEFENSE_UNIT_TYPE:
                yield group

    @property
    def long_range_sams(self) -> Iterator[VehicleGroup]:
        for group in self.red.vehicle_group:
            if group.units[0].type in self.LONG_RANGE_SAM_UNIT_TYPES:
                yield group

    @property
    def medium_range_sams(self) -> Iterator[VehicleGroup]:
        for group in self.red.vehicle_group:
            if group.units[0].type in self.MEDIUM_RANGE_SAM_UNIT_TYPES:
                yield group

    @property
    def short_range_sams(self) -> Iterator[VehicleGroup]:
        for group in self.red.vehicle_group:
            if group.units[0].type in self.SHORT_RANGE_SAM_UNIT_TYPES:
                yield group

    @property
    def aaa(self) -> Iterator[VehicleGroup]:
        for group in itertools.chain(self.blue.vehicle_group, self.red.vehicle_group):
            if group.units[0].type in self.AAA_UNIT_TYPES:
                yield group

    @property
    def ewrs(self) -> Iterator[VehicleGroup]:
        for group in self.red.vehicle_group:
            if group.units[0].type in self.EWR_UNIT_TYPE:
                yield group

    @property
    def armor_groups(self) -> Iterator[VehicleGroup]:
        for group in itertools.chain(self.blue.vehicle_group, self.red.vehicle_group):
            if group.units[0].type in self.ARMOR_GROUP_UNIT_TYPE:
                yield group

    @property
    def helipads(self) -> Iterator[StaticGroup]:
        for group in self.blue.static_group:
            if group.units[0].type == self.FARP_HELIPAD:
                yield group

    @property
    def factories(self) -> Iterator[StaticGroup]:
        for group in self.blue.static_group:
            if group.units[0].type in self.FACTORY_UNIT_TYPE:
                yield group

    @property
    def ammunition_depots(self) -> Iterator[StaticGroup]:
        for group in itertools.chain(self.blue.static_group, self.red.static_group):
            if group.units[0].type in self.AMMUNITION_DEPOT_UNIT_TYPE:
                yield group

    @property
    def strike_targets(self) -> Iterator[StaticGroup]:
        for group in itertools.chain(self.blue.static_group, self.red.static_group):
            if group.units[0].type in self.STRIKE_TARGET_UNIT_TYPE:
                yield group

    @property
    def scenery(self) -> List[SceneryGroup]:
        return SceneryGroup.from_trigger_zones(self.mission.triggers._zones)

    @cached_property
    def control_points(self) -> Dict[int, ControlPoint]:
        control_points = {}
        for airport in self.mission.terrain.airport_list():
            if airport.is_blue() or airport.is_red():
                control_point = self.control_point_from_airport(airport)
                control_points[control_point.id] = control_point

        for blue in (False, True):
            for group in self.off_map_spawns(blue):
                control_point = OffMapSpawn(
                    next(self.control_point_id), str(group.name), group.position
                )
                control_point.captured = blue
                control_point.captured_invert = group.late_activation
                control_points[control_point.id] = control_point
            for group in self.carriers(blue):
                # TODO: Name the carrier.
                control_point = Carrier(
                    "carrier", group.position, next(self.control_point_id)
                )
                control_point.captured = blue
                control_point.captured_invert = group.late_activation
                control_points[control_point.id] = control_point
            for group in self.lhas(blue):
                # TODO: Name the LHA.db
                control_point = Lha("lha", group.position, next(self.control_point_id))
                control_point.captured = blue
                control_point.captured_invert = group.late_activation
                control_points[control_point.id] = control_point
            for group in self.fobs(blue):
                control_point = Fob(
                    str(group.name), group.position, next(self.control_point_id)
                )
                control_point.captured = blue
                control_point.captured_invert = group.late_activation
                control_points[control_point.id] = control_point

        return control_points

    @property
    def front_line_path_groups(self) -> Iterator[VehicleGroup]:
        for group in self.country(blue=True).vehicle_group:
            if group.units[0].type == self.FRONT_LINE_UNIT_TYPE:
                yield group

    @property
    def shipping_lane_groups(self) -> Iterator[ShipGroup]:
        for group in self.country(blue=True).ship_group:
            if group.units[0].type == self.SHIPPING_LANE_UNIT_TYPE:
                yield group

    def add_supply_routes(self) -> None:
        for group in self.front_line_path_groups:
            # The unit will have its first waypoint at the source CP and the final
            # waypoint at the destination CP. Each waypoint defines the path of the
            # cargo ship.
            waypoints = [p.position for p in group.points]
            origin = self.theater.closest_control_point(waypoints[0])
            if origin is None:
                raise RuntimeError(
                    f"No control point near the first waypoint of {group.name}"
                )
            destination = self.theater.closest_control_point(waypoints[-1])
            if destination is None:
                raise RuntimeError(
                    f"No control point near the final waypoint of {group.name}"
                )

            self.control_points[origin.id].create_convoy_route(destination, waypoints)
            self.control_points[destination.id].create_convoy_route(
                origin, list(reversed(waypoints))
            )

    def add_shipping_lanes(self) -> None:
        for group in self.shipping_lane_groups:
            # The unit will have its first waypoint at the source CP and the final
            # waypoint at the destination CP. Each waypoint defines the path of the
            # cargo ship.
            waypoints = [p.position for p in group.points]
            origin = self.theater.closest_control_point(waypoints[0])
            if origin is None:
                raise RuntimeError(
                    f"No control point near the first waypoint of {group.name}"
                )
            destination = self.theater.closest_control_point(waypoints[-1])
            if destination is None:
                raise RuntimeError(
                    f"No control point near the final waypoint of {group.name}"
                )

            self.control_points[origin.id].create_shipping_lane(destination, waypoints)
            self.control_points[destination.id].create_shipping_lane(
                origin, list(reversed(waypoints))
            )

    def objective_info(self, group: Group) -> Tuple[ControlPoint, Distance]:
        closest = self.theater.closest_control_point(group.position)
        distance = meters(closest.position.distance_to_point(group.position))
        return closest, distance

    def add_preset_locations(self) -> None:
        for group in self.offshore_strike_targets:
            closest, distance = self.objective_info(group)
            closest.preset_locations.offshore_strike_locations.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.ships:
            closest, distance = self.objective_info(group)
            closest.preset_locations.ships.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.missile_sites:
            closest, distance = self.objective_info(group)
            closest.preset_locations.missile_sites.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.coastal_defenses:
            closest, distance = self.objective_info(group)
            closest.preset_locations.coastal_defenses.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.long_range_sams:
            closest, distance = self.objective_info(group)
            closest.preset_locations.long_range_sams.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.medium_range_sams:
            closest, distance = self.objective_info(group)
            closest.preset_locations.medium_range_sams.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.short_range_sams:
            closest, distance = self.objective_info(group)
            closest.preset_locations.short_range_sams.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.aaa:
            closest, distance = self.objective_info(group)
            closest.preset_locations.aaa.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.ewrs:
            closest, distance = self.objective_info(group)
            closest.preset_locations.ewrs.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.armor_groups:
            closest, distance = self.objective_info(group)
            closest.preset_locations.armor_groups.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.helipads:
            closest, distance = self.objective_info(group)
            closest.helipads.append(
                Helipad.from_point(group.position, group.units[0].heading)
            )

        for group in self.factories:
            closest, distance = self.objective_info(group)
            closest.preset_locations.factories.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.ammunition_depots:
            closest, distance = self.objective_info(group)
            closest.preset_locations.ammunition_depots.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.strike_targets:
            closest, distance = self.objective_info(group)
            closest.preset_locations.strike_locations.append(
                PointWithHeading.from_point(group.position, group.units[0].heading)
            )

        for group in self.scenery:
            closest, distance = self.objective_info(group)
            closest.preset_locations.scenery.append(group)

    def populate_theater(self) -> None:
        for control_point in self.control_points.values():
            self.theater.add_controlpoint(control_point)
        self.add_preset_locations()
        self.add_supply_routes()
        self.add_shipping_lanes()


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

    def __init__(self):
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

    def add_controlpoint(self, point: ControlPoint):
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

    def nearest_land_pos(self, point: Point, extend_dist: int = 50) -> Point:
        """Returns the nearest point inside a land exclusion zone from point
        `extend_dist` determines how far inside the zone the point should be placed"""
        if self.is_on_land(point):
            return point
        point = geometry.Point(point.x, point.y)
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

    def closest_control_point(self, point: Point) -> ControlPoint:
        closest = self.controlpoints[0]
        closest_distance = point.distance_to_point(closest.position)
        for control_point in self.controlpoints[1:]:
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
        if miz is None:
            raise RuntimeError(
                "Old format (non-miz) campaigns are no longer supported."
            )

        with logged_duration("Importing miz data"):
            MizCampaignLoader(directory / miz, t).populate_theater()
        return t

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
    def projection_parameters(self) -> TransverseMercator:
        from .syria import PARAMETERS

        return PARAMETERS
