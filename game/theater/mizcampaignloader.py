from __future__ import annotations

import itertools
from functools import cached_property
from pathlib import Path
from typing import Iterator, List, Dict, Tuple, TYPE_CHECKING

from dcs import Mission
from dcs.countries import CombinedJointTaskForcesBlue, CombinedJointTaskForcesRed
from dcs.country import Country
from dcs.planes import F_15C
from dcs.ships import Stennis, LHA_Tarawa, HandyWind, USS_Arleigh_Burke_IIa
from dcs.statics import Fortification, Warehouse
from dcs.terrain import Airport
from dcs.unitgroup import PlaneGroup, ShipGroup, VehicleGroup, StaticGroup
from dcs.vehicles import Armor, Unarmed, MissilesSS, AirDefence

from game.point_with_heading import PointWithHeading
from game.positioned import Positioned
from game.profiling import logged_duration
from game.scenery_group import SceneryGroup
from game.utils import Distance, meters, Heading
from .controlpoint import (
    Airfield,
    Carrier,
    ControlPoint,
    Fob,
    Lha,
    OffMapSpawn,
)

if TYPE_CHECKING:
    from .conflicttheater import ConflictTheater


class MizCampaignLoader:
    BLUE_COUNTRY = CombinedJointTaskForcesBlue()
    RED_COUNTRY = CombinedJointTaskForcesRed()

    OFF_MAP_UNIT_TYPE = F_15C.id

    CV_UNIT_TYPE = Stennis.id
    LHA_UNIT_TYPE = LHA_Tarawa.id
    FRONT_LINE_UNIT_TYPE = Armor.M_113.id
    SHIPPING_LANE_UNIT_TYPE = HandyWind.id

    FOB_UNIT_TYPE = Unarmed.SKP_11.id
    FARP_HELIPAD = "SINGLE_HELIPAD"

    OFFSHORE_STRIKE_TARGET_UNIT_TYPE = Fortification.Oil_platform.id
    SHIP_UNIT_TYPE = USS_Arleigh_Burke_IIa.id
    MISSILE_SITE_UNIT_TYPE = MissilesSS.Scud_B.id
    COASTAL_DEFENSE_UNIT_TYPE = MissilesSS.Hy_launcher.id

    # Multiple options for air defenses so campaign designers can more accurately see
    # the coverage of their IADS for the expected type.
    LONG_RANGE_SAM_UNIT_TYPES = {
        AirDefence.Patriot_ln.id,
        AirDefence.S_300PS_5P85C_ln.id,
        AirDefence.S_300PS_5P85D_ln.id,
    }

    MEDIUM_RANGE_SAM_UNIT_TYPES = {
        AirDefence.Hawk_ln.id,
        AirDefence.S_75M_Volhov.id,
        AirDefence._5p73_s_125_ln.id,
    }

    SHORT_RANGE_SAM_UNIT_TYPES = {
        AirDefence.M1097_Avenger.id,
        AirDefence.Rapier_fsa_launcher.id,
        AirDefence._2S6_Tunguska.id,
        AirDefence.Strela_1_9P31.id,
    }

    AAA_UNIT_TYPES = {
        AirDefence.Flak18.id,
        AirDefence.Vulcan.id,
        AirDefence.ZSU_23_4_Shilka.id,
    }

    EWR_UNIT_TYPE = AirDefence._1L13_EWR.id

    ARMOR_GROUP_UNIT_TYPE = Armor.M_1_Abrams.id

    FACTORY_UNIT_TYPE = Fortification.Workshop_A.id

    AMMUNITION_DEPOT_UNIT_TYPE = Warehouse._Ammunition_depot.id

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
        cp = Airfield(airport)
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

    def off_map_spawns(self, blue: bool) -> Iterator[PlaneGroup]:
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
            for ship in self.carriers(blue):
                # TODO: Name the carrier.
                control_point = Carrier(
                    "carrier", ship.position, next(self.control_point_id)
                )
                control_point.captured = blue
                control_point.captured_invert = ship.late_activation
                control_points[control_point.id] = control_point
            for ship in self.lhas(blue):
                # TODO: Name the LHA.db
                control_point = Lha("lha", ship.position, next(self.control_point_id))
                control_point.captured = blue
                control_point.captured_invert = ship.late_activation
                control_points[control_point.id] = control_point
            for fob in self.fobs(blue):
                control_point = Fob(
                    str(fob.name), fob.position, next(self.control_point_id)
                )
                control_point.captured = blue
                control_point.captured_invert = fob.late_activation
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

    def objective_info(
        self, near: Positioned, allow_naval: bool = False
    ) -> Tuple[ControlPoint, Distance]:
        closest = self.theater.closest_control_point(near.position, allow_naval)
        distance = meters(closest.position.distance_to_point(near.position))
        return closest, distance

    def add_preset_locations(self) -> None:
        for static in self.offshore_strike_targets:
            closest, distance = self.objective_info(static)
            closest.preset_locations.offshore_strike_locations.append(
                PointWithHeading.from_point(
                    static.position, Heading.from_degrees(static.units[0].heading)
                )
            )

        for ship in self.ships:
            closest, distance = self.objective_info(ship, allow_naval=True)
            closest.preset_locations.ships.append(
                PointWithHeading.from_point(
                    ship.position, Heading.from_degrees(ship.units[0].heading)
                )
            )

        for group in self.missile_sites:
            closest, distance = self.objective_info(group)
            closest.preset_locations.missile_sites.append(
                PointWithHeading.from_point(
                    group.position, Heading.from_degrees(group.units[0].heading)
                )
            )

        for group in self.coastal_defenses:
            closest, distance = self.objective_info(group)
            closest.preset_locations.coastal_defenses.append(
                PointWithHeading.from_point(
                    group.position, Heading.from_degrees(group.units[0].heading)
                )
            )

        for group in self.long_range_sams:
            closest, distance = self.objective_info(group)
            closest.preset_locations.long_range_sams.append(
                PointWithHeading.from_point(
                    group.position, Heading.from_degrees(group.units[0].heading)
                )
            )

        for group in self.medium_range_sams:
            closest, distance = self.objective_info(group)
            closest.preset_locations.medium_range_sams.append(
                PointWithHeading.from_point(
                    group.position, Heading.from_degrees(group.units[0].heading)
                )
            )

        for group in self.short_range_sams:
            closest, distance = self.objective_info(group)
            closest.preset_locations.short_range_sams.append(
                PointWithHeading.from_point(
                    group.position, Heading.from_degrees(group.units[0].heading)
                )
            )

        for group in self.aaa:
            closest, distance = self.objective_info(group)
            closest.preset_locations.aaa.append(
                PointWithHeading.from_point(
                    group.position, Heading.from_degrees(group.units[0].heading)
                )
            )

        for group in self.ewrs:
            closest, distance = self.objective_info(group)
            closest.preset_locations.ewrs.append(
                PointWithHeading.from_point(
                    group.position, Heading.from_degrees(group.units[0].heading)
                )
            )

        for group in self.armor_groups:
            closest, distance = self.objective_info(group)
            closest.preset_locations.armor_groups.append(
                PointWithHeading.from_point(
                    group.position, Heading.from_degrees(group.units[0].heading)
                )
            )

        for static in self.helipads:
            closest, distance = self.objective_info(static)
            closest.helipads.append(
                PointWithHeading.from_point(
                    static.position, Heading.from_degrees(static.units[0].heading)
                )
            )

        for static in self.factories:
            closest, distance = self.objective_info(static)
            closest.preset_locations.factories.append(
                PointWithHeading.from_point(
                    static.position, Heading.from_degrees(static.units[0].heading)
                )
            )

        for static in self.ammunition_depots:
            closest, distance = self.objective_info(static)
            closest.preset_locations.ammunition_depots.append(
                PointWithHeading.from_point(
                    static.position, Heading.from_degrees(static.units[0].heading)
                )
            )

        for static in self.strike_targets:
            closest, distance = self.objective_info(static)
            closest.preset_locations.strike_locations.append(
                PointWithHeading.from_point(
                    static.position, Heading.from_degrees(static.units[0].heading)
                )
            )

        for scenery_group in self.scenery:
            closest, distance = self.objective_info(scenery_group)
            closest.preset_locations.scenery.append(scenery_group)

    def populate_theater(self) -> None:
        for control_point in self.control_points.values():
            self.theater.add_controlpoint(control_point)
        self.add_preset_locations()
        self.add_supply_routes()
        self.add_shipping_lanes()
