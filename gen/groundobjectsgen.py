"""Generators for creating the groups for ground objectives.

The classes in this file are responsible for creating the vehicle groups, ship
groups, statics, missile sites, and AA sites for the mission. Each of these
objectives is defined in the Theater by a TheaterGroundObject. These classes
create the pydcs groups and statics for those areas and add them to the mission.
"""
from __future__ import annotations

import logging
import random
from typing import Dict, Iterator, Optional, TYPE_CHECKING, Type, List

from dcs import Mission, Point, unitgroup
from dcs.action import SceneryDestructionZone
from dcs.country import Country
from dcs.point import StaticPoint
from dcs.statics import Fortification, fortification_map, warehouse_map, Warehouse
from dcs.task import (
    ActivateBeaconCommand,
    ActivateICLSCommand,
    EPLRS,
    OptAlarmState,
    FireAtPoint,
)
from dcs.triggers import TriggerStart, TriggerZone
from dcs.unit import Ship, Unit, Vehicle, SingleHeliPad, Static
from dcs.unitgroup import Group, ShipGroup, StaticGroup, VehicleGroup
from dcs.unittype import StaticType, UnitType
from dcs.vehicles import vehicle_map

from game import db
from game.data.building_data import FORTIFICATION_UNITS, FORTIFICATION_UNITS_ID
from game.db import unit_type_from_name
from game.theater import ControlPoint, TheaterGroundObject
from game.theater.theatergroundobject import (
    BuildingGroundObject,
    CarrierGroundObject,
    FactoryGroundObject,
    GenericCarrierGroundObject,
    LhaGroundObject,
    ShipGroundObject,
    MissileSiteGroundObject,
    SceneryGroundObject,
)
from game.unitmap import UnitMap
from game.utils import knots, mps
from .radios import RadioFrequency, RadioRegistry
from .runways import RunwayData
from .tacan import TacanBand, TacanChannel, TacanRegistry

if TYPE_CHECKING:
    from game import Game

FARP_FRONTLINE_DISTANCE = 10000
AA_CP_MIN_DISTANCE = 40000


class GenericGroundObjectGenerator:
    """An unspecialized ground object generator.

    Currently used only for SAM
    """

    def __init__(
        self,
        ground_object: TheaterGroundObject,
        country: Country,
        game: Game,
        mission: Mission,
        unit_map: UnitMap,
    ) -> None:
        self.ground_object = ground_object
        self.country = country
        self.game = game
        self.m = mission
        self.unit_map = unit_map

    def generate(self) -> None:
        if self.game.position_culled(self.ground_object.position):
            return

        for group in self.ground_object.groups:
            if not group.units:
                logging.warning(f"Found empty group in {self.ground_object}")
                continue

            unit_type = unit_type_from_name(group.units[0].type)
            if unit_type is None:
                raise RuntimeError(f"Unrecognized unit type: {group.units[0].type}")

            vg = self.m.vehicle_group(
                self.country,
                group.name,
                unit_type,
                position=group.position,
                heading=group.units[0].heading,
            )
            vg.units[0].name = self.m.string(group.units[0].name)
            vg.units[0].player_can_drive = True
            for i, u in enumerate(group.units):
                if i > 0:
                    vehicle = Vehicle(
                        self.m.next_unit_id(), self.m.string(u.name), u.type
                    )
                    vehicle.position.x = u.position.x
                    vehicle.position.y = u.position.y
                    vehicle.heading = u.heading
                    vehicle.player_can_drive = True
                    vg.add_unit(vehicle)

            self.enable_eplrs(vg, unit_type)
            self.set_alarm_state(vg)
            self._register_unit_group(group, vg)

    @staticmethod
    def enable_eplrs(group: Group, unit_type: Type[UnitType]) -> None:
        if hasattr(unit_type, "eplrs"):
            if unit_type.eplrs:
                group.points[0].tasks.append(EPLRS(group.id))

    def set_alarm_state(self, group: Group) -> None:
        if self.game.settings.perf_red_alert_state:
            group.points[0].tasks.append(OptAlarmState(2))
        else:
            group.points[0].tasks.append(OptAlarmState(1))

    def _register_unit_group(self, persistence_group: Group, miz_group: Group) -> None:
        self.unit_map.add_ground_object_units(
            self.ground_object, persistence_group, miz_group
        )


class MissileSiteGenerator(GenericGroundObjectGenerator):
    def generate(self) -> None:
        super(MissileSiteGenerator, self).generate()
        # Note : Only the SCUD missiles group can fire (V1 site cannot fire in game right now)
        # TODO : Should be pre-planned ?
        # TODO : Add delay to task to spread fire task over mission duration ?
        for group in self.ground_object.groups:
            vg = self.m.find_group(group.name)
            if vg is not None:
                targets = self.possible_missile_targets(vg)
                if targets:
                    target = random.choice(targets)
                    real_target = target.point_from_heading(
                        random.randint(0, 360), random.randint(0, 2500)
                    )
                    vg.points[0].add_task(FireAtPoint(real_target))
                    logging.info("Set up fire task for missile group.")
                else:
                    logging.info(
                        "Couldn't setup missile site to fire, no valid target in range."
                    )
            else:
                logging.info(
                    "Couldn't setup missile site to fire, group was not generated."
                )

    def possible_missile_targets(self, vg: Group) -> List[Point]:
        """
        Find enemy control points in range
        :param vg: Vehicle group we are searching a target for (There is always only oe group right now)
        :return: List of possible missile targets
        """
        targets: List[Point] = []
        for cp in self.game.theater.controlpoints:
            if cp.captured != self.ground_object.control_point.captured:
                distance = cp.position.distance_to_point(vg.position)
                if distance < self.missile_site_range:
                    targets.append(cp.position)
        return targets

    @property
    def missile_site_range(self) -> int:
        """
        Get the missile site range
        :return: Missile site range
        """
        site_range = 0
        for group in self.ground_object.groups:
            vg = self.m.find_group(group.name)
            if vg is not None:
                for u in vg.units:
                    if u.type in vehicle_map:
                        if vehicle_map[u.type].threat_range > site_range:
                            site_range = vehicle_map[u.type].threat_range
        return site_range


class BuildingSiteGenerator(GenericGroundObjectGenerator):
    """Generator for building sites.

    Building sites are the primary type of non-airbase objective locations that
    appear on the map. They come in a handful of variants each with different
    types of buildings and ground units.
    """

    def generate(self) -> None:
        if self.game.position_culled(self.ground_object.position):
            return

        if self.ground_object.dcs_identifier in warehouse_map:
            static_type = warehouse_map[self.ground_object.dcs_identifier]
            self.generate_static(static_type)
        elif self.ground_object.dcs_identifier in fortification_map:
            static_type = fortification_map[self.ground_object.dcs_identifier]
            self.generate_static(static_type)
        elif self.ground_object.dcs_identifier in FORTIFICATION_UNITS_ID:
            for f in FORTIFICATION_UNITS:
                if f.id == self.ground_object.dcs_identifier:
                    unit_type = f
                    self.generate_vehicle_group(unit_type)
                    break
        else:
            logging.error(
                f"{self.ground_object.dcs_identifier} not found in static maps"
            )

    def generate_vehicle_group(self, unit_type: Type[UnitType]) -> None:
        if not self.ground_object.is_dead:
            group = self.m.vehicle_group(
                country=self.country,
                name=self.ground_object.group_name,
                _type=unit_type,
                position=self.ground_object.position,
                heading=self.ground_object.heading,
            )
            self._register_fortification(group)

    def generate_static(self, static_type: Type[StaticType]) -> None:
        group = self.m.static_group(
            country=self.country,
            name=self.ground_object.group_name,
            _type=static_type,
            position=self.ground_object.position,
            heading=self.ground_object.heading,
            dead=self.ground_object.is_dead,
        )
        self._register_building(group)

    def _register_fortification(self, fortification: VehicleGroup) -> None:
        assert isinstance(self.ground_object, BuildingGroundObject)
        self.unit_map.add_fortification(self.ground_object, fortification)

    def _register_building(self, building: StaticGroup) -> None:
        assert isinstance(self.ground_object, BuildingGroundObject)
        self.unit_map.add_building(self.ground_object, building)


class FactoryGenerator(BuildingSiteGenerator):
    """Generator for factory sites.

    Factory sites are the buildings that allow the recruitment of ground units.
    Destroying these prevents the owner from recruiting ground units at the connected
    control point.
    """

    def generate(self) -> None:
        if self.game.position_culled(self.ground_object.position):
            return

        # TODO: Faction specific?
        self.generate_static(Fortification.Workshop_A)


class SceneryGenerator(BuildingSiteGenerator):
    def generate(self) -> None:
        if isinstance(self.ground_object, SceneryGroundObject):
            trigger_zone = self.generate_trigger_zone(self.ground_object)

            if self.ground_object.is_dead:
                self.generate_dead_trigger_rule(trigger_zone)

            self.register_scenery()

    def generate_trigger_zone(self, scenery: SceneryGroundObject) -> TriggerZone:
        zone = scenery.zone
        # self.m.triggers._zones.append(scenery.zone)
        return self.m.triggers.add_triggerzone(
            zone.position, zone.radius, zone.hidden, zone.name, zone.properties
        )

    def generate_dead_trigger_rule(self, trigger_zone: TriggerZone) -> None:
        # Add destruction zone trigger
        t = TriggerStart(comment="Destruction")
        t.actions.append(SceneryDestructionZone(100, trigger_zone.id))
        self.m.triggerrules.triggers.append(t)

    def register_scenery(self) -> None:
        scenery = self.ground_object
        self.unit_map.add_scenery(scenery)


class GenericCarrierGenerator(GenericGroundObjectGenerator):
    """Base type for carrier group generation.

    Used by both CV(N) groups and LHA groups.
    """

    def __init__(
        self,
        ground_object: GenericCarrierGroundObject,
        control_point: ControlPoint,
        country: Country,
        game: Game,
        mission: Mission,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        icls_alloc: Iterator[int],
        runways: Dict[str, RunwayData],
        unit_map: UnitMap,
    ) -> None:
        super().__init__(ground_object, country, game, mission, unit_map)
        self.ground_object = ground_object
        self.control_point = control_point
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.icls_alloc = icls_alloc
        self.runways = runways

    def generate(self) -> None:
        # TODO: Require single group?
        for group in self.ground_object.groups:
            if not group.units:
                logging.warning(f"Found empty carrier group in {self.control_point}")
                continue

            atc = self.radio_registry.alloc_uhf()
            ship_group = self.configure_carrier(group, atc)
            for unit in group.units[1:]:
                ship_group.add_unit(self.create_ship(unit, atc))

            tacan = self.tacan_registry.alloc_for_band(TacanBand.X)
            tacan_callsign = self.tacan_callsign()
            icls = next(self.icls_alloc)

            # Always steam into the wind, even if the carrier is being moved.
            # There are multiple unsimulated hours between turns, so we can
            # count those as the time the carrier uses to move and the mission
            # time as the recovery window.
            brc = self.steam_into_wind(ship_group)
            self.activate_beacons(ship_group, tacan, tacan_callsign, icls)
            self.add_runway_data(brc or 0, atc, tacan, tacan_callsign, icls)
            self._register_unit_group(group, ship_group)

    def get_carrier_type(self, group: Group) -> Type[UnitType]:
        unit_type = unit_type_from_name(group.units[0].type)
        if unit_type is None:
            raise RuntimeError(f"Unrecognized carrier name: {group.units[0].type}")
        return unit_type

    def configure_carrier(self, group: Group, atc_channel: RadioFrequency) -> ShipGroup:
        unit_type = self.get_carrier_type(group)

        ship_group = self.m.ship_group(
            self.country,
            group.name,
            unit_type,
            position=group.position,
            heading=group.units[0].heading,
        )
        ship_group.set_frequency(atc_channel.hertz)
        ship_group.units[0].name = self.m.string(group.units[0].name)
        return ship_group

    def create_ship(self, unit: Unit, atc_channel: RadioFrequency) -> Ship:
        ship = Ship(
            self.m.next_unit_id(),
            self.m.string(unit.name),
            unit_type_from_name(unit.type),
        )
        ship.position.x = unit.position.x
        ship.position.y = unit.position.y
        ship.heading = unit.heading
        # TODO: Verify.
        ship.set_frequency(atc_channel.hertz)
        return ship

    def steam_into_wind(self, group: ShipGroup) -> Optional[int]:
        wind = self.game.conditions.weather.wind.at_0m
        brc = wind.direction + 180
        # Aim for 25kts over the deck.
        carrier_speed = knots(25) - mps(wind.speed)
        for attempt in range(5):
            point = group.points[0].position.point_from_heading(
                brc, 100000 - attempt * 20000
            )
            if self.game.theater.is_in_sea(point):
                group.points[0].speed = carrier_speed.meters_per_second
                group.add_waypoint(point, carrier_speed.kph)
                return brc
        return None

    def tacan_callsign(self) -> str:
        raise NotImplementedError

    @staticmethod
    def activate_beacons(
        group: ShipGroup, tacan: TacanChannel, callsign: str, icls: int
    ) -> None:
        group.points[0].tasks.append(
            ActivateBeaconCommand(
                channel=tacan.number,
                modechannel=tacan.band.value,
                callsign=callsign,
                unit_id=group.units[0].id,
                aa=False,
            )
        )
        group.points[0].tasks.append(
            ActivateICLSCommand(icls, unit_id=group.units[0].id)
        )

    def add_runway_data(
        self,
        brc: int,
        atc: RadioFrequency,
        tacan: TacanChannel,
        callsign: str,
        icls: int,
    ) -> None:
        # TODO: Make unit name usable.
        # This relies on one control point mapping exactly
        # to one LHA, carrier, or other usable "runway".
        # This isn't wholly true, since the DD escorts of
        # the carrier group are valid for helicopters, but
        # they aren't exposed as such to the game. Should
        # clean this up so that's possible. We can't use the
        # unit name since it's an arbitrary ID.
        self.runways[self.control_point.name] = RunwayData(
            self.control_point.name,
            brc,
            "N/A",
            atc=atc,
            tacan=tacan,
            tacan_callsign=callsign,
            icls=icls,
        )


class CarrierGenerator(GenericCarrierGenerator):
    """Generator for CV(N) groups."""

    def get_carrier_type(self, group: Group) -> UnitType:
        unit_type = super().get_carrier_type(group)
        if self.game.settings.supercarrier:
            unit_type = db.upgrade_to_supercarrier(unit_type, self.control_point.name)
        return unit_type

    def tacan_callsign(self) -> str:
        # TODO: Assign these properly.
        if self.control_point.name == "Carrier Strike Group 8":
            return "TRU"
        else:
            return random.choice(
                [
                    "STE",
                    "CVN",
                    "CVH",
                    "CCV",
                    "ACC",
                    "ARC",
                    "GER",
                    "ABR",
                    "LIN",
                    "TRU",
                ]
            )


class LhaGenerator(GenericCarrierGenerator):
    """Generator for LHA groups."""

    def tacan_callsign(self) -> str:
        # TODO: Assign these properly.
        return random.choice(
            [
                "LHD",
                "LHA",
                "LHB",
                "LHC",
                "LHD",
                "LDS",
            ]
        )


class ShipObjectGenerator(GenericGroundObjectGenerator):
    """Generator for non-carrier naval groups."""

    def generate(self) -> None:
        if self.game.position_culled(self.ground_object.position):
            return

        for group in self.ground_object.groups:
            if not group.units:
                logging.warning(f"Found empty group in {self.ground_object}")
                continue

            unit_type = unit_type_from_name(group.units[0].type)
            if unit_type is None:
                raise RuntimeError(f"Unrecognized unit type: {group.units[0].type}")

            self.generate_group(group, unit_type)

    def generate_group(self, group_def: Group, first_unit_type: Type[UnitType]) -> None:
        group = self.m.ship_group(
            self.country,
            group_def.name,
            first_unit_type,
            position=group_def.position,
            heading=group_def.units[0].heading,
        )
        group.units[0].name = self.m.string(group_def.units[0].name)
        # TODO: Skipping the first unit looks like copy pasta from the carrier.
        for unit in group_def.units[1:]:
            unit_type = unit_type_from_name(unit.type)
            ship = Ship(self.m.next_unit_id(), self.m.string(unit.name), unit_type)
            ship.position.x = unit.position.x
            ship.position.y = unit.position.y
            ship.heading = unit.heading
            group.add_unit(ship)
        self.set_alarm_state(group)
        self._register_unit_group(group_def, group)


class HelipadGenerator:
    """
    Generates helipads for given control point
    """

    def __init__(
        self,
        mission: Mission,
        cp: ControlPoint,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
    ):
        self.m = mission
        self.cp = cp
        self.game = game
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry

    def generate(self) -> None:

        if self.cp.captured:
            country_name = self.game.player_country
        else:
            country_name = self.game.enemy_country
        country = self.m.country(country_name)

        for i, helipad in enumerate(self.cp.helipads):
            name = self.cp.name + "_helipad_" + str(i)
            logging.info("Generating helipad : " + name)
            pad = SingleHeliPad(name=self.m.string(name + "_unit"))
            pad.position = Point(helipad.x, helipad.y)
            pad.heading = helipad.heading
            # pad.heliport_frequency = self.radio_registry.alloc_uhf() TODO : alloc radio & callsign
            sg = unitgroup.StaticGroup(self.m.next_group_id(), self.m.string(name))
            sg.add_unit(pad)
            sp = StaticPoint()
            sp.position = pad.position
            sg.add_point(sp)
            country.add_static_group(sg)


class GroundObjectsGenerator:
    """Creates DCS groups and statics for the theater during mission generation.

    Most of the work of group/static generation is delegated to the other
    generator classes. This class is responsible for finding each of the
    locations for spawning ground objects, determining their types, and creating
    the appropriate generators.
    """

    def __init__(
        self,
        mission: Mission,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        unit_map: UnitMap,
    ) -> None:
        self.m = mission
        self.game = game
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.unit_map = unit_map
        self.icls_alloc = iter(range(1, 21))
        self.runways: Dict[str, RunwayData] = {}

    def generate(self):
        for cp in self.game.theater.controlpoints:
            if cp.captured:
                country_name = self.game.player_country
            else:
                country_name = self.game.enemy_country
            country = self.m.country(country_name)

            HelipadGenerator(
                self.m, cp, self.game, self.radio_registry, self.tacan_registry
            ).generate()

            for ground_object in cp.ground_objects:
                if isinstance(ground_object, FactoryGroundObject):
                    generator = FactoryGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                elif isinstance(ground_object, SceneryGroundObject):
                    generator = SceneryGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                elif isinstance(ground_object, BuildingGroundObject):
                    generator = BuildingSiteGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                elif isinstance(ground_object, CarrierGroundObject):
                    generator = CarrierGenerator(
                        ground_object,
                        cp,
                        country,
                        self.game,
                        self.m,
                        self.radio_registry,
                        self.tacan_registry,
                        self.icls_alloc,
                        self.runways,
                        self.unit_map,
                    )
                elif isinstance(ground_object, LhaGroundObject):
                    generator = CarrierGenerator(
                        ground_object,
                        cp,
                        country,
                        self.game,
                        self.m,
                        self.radio_registry,
                        self.tacan_registry,
                        self.icls_alloc,
                        self.runways,
                        self.unit_map,
                    )
                elif isinstance(ground_object, ShipGroundObject):
                    generator = ShipObjectGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                elif isinstance(ground_object, MissileSiteGroundObject):
                    generator = MissileSiteGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                else:
                    generator = GenericGroundObjectGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                generator.generate()
