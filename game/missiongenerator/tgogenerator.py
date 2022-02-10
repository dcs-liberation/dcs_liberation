"""Generators for creating the groups for ground objectives.

The classes in this file are responsible for creating the vehicle groups, ship
groups, statics, missile sites, and AA sites for the mission. Each of these
objectives is defined in the Theater by a TheaterGroundObject. These classes
create the pydcs groups and statics for those areas and add them to the mission.
"""
from __future__ import annotations

import logging
import random
from collections import defaultdict
from typing import (
    Any,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    TYPE_CHECKING,
    Type,
    TypeVar,
    List,
    Any,
)

from dcs import Mission, Point, unitgroup
from dcs.action import DoScript, SceneryDestructionZone
from dcs.condition import MapObjectIsDead
from dcs.country import Country
from dcs.point import StaticPoint
from dcs.ships import (
    CVN_71,
    CVN_72,
    CVN_73,
    CVN_75,
    CV_1143_5,
    KUZNECOW,
    Stennis,
    ship_map,
)
from dcs.statics import Fortification, fortification_map, warehouse_map
from dcs.task import (
    ActivateBeaconCommand,
    ActivateICLSCommand,
    EPLRS,
    FireAtPoint,
    OptAlarmState,
)
from dcs.translation import String
from dcs.triggers import Event, TriggerOnce, TriggerStart, TriggerZone
from dcs.unit import InvisibleFARP, Ship, Unit, Vehicle
from dcs.unitgroup import ShipGroup, StaticGroup, VehicleGroup, MovingGroup
from dcs.unittype import ShipType, StaticType, VehicleType
from dcs.vehicles import vehicle_map

from game.data.building_data import FORTIFICATION_UNITS, FORTIFICATION_UNITS_ID
from game.dcs.helpers import static_type_from_name, unit_type_from_name
from game.radio.radios import RadioFrequency, RadioRegistry
from game.radio.tacan import TacanBand, TacanChannel, TacanRegistry, TacanUsage
from game.theater import ControlPoint, TheaterGroundObject, TheaterUnit
from game.theater.theatergroundobject import (
    CarrierGroundObject,
    GenericCarrierGroundObject,
    LhaGroundObject,
    MissileSiteGroundObject,
)
from game.theater.theatergroup import SceneryUnit, TheaterGroup
from game.unitmap import UnitMap
from game.utils import Heading, feet, knots, mps
from gen.runways import RunwayData

if TYPE_CHECKING:
    from game import Game

FARP_FRONTLINE_DISTANCE = 10000
AA_CP_MIN_DISTANCE = 40000


class GroundObjectGenerator:
    """generates the DCS groups and units from the TheaterGroundObject"""

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

    @property
    def culled(self) -> bool:
        return self.game.iads_considerate_culling(self.ground_object)

    def generate(self) -> None:
        if self.culled:
            return
        for group in self.ground_object.groups:
            vehicle_units = []
            ship_units = []
            # Split the different unit types to be compliant to dcs limitation
            for unit in group.units:
                if unit.is_static:
                    # A Static unit has to be a single static group
                    self.create_static_group(unit)
                elif unit.is_vehicle and unit.alive:
                    # All alive Vehicles
                    vehicle_units.append(unit)
                elif unit.is_ship and unit.alive:
                    # All alive Ships
                    ship_units.append(unit)
            if vehicle_units:
                self.create_vehicle_group(group.group_name, vehicle_units)
            if ship_units:
                self.create_ship_group(group.group_name, ship_units)

    def create_vehicle_group(
        self, group_name: str, units: list[TheaterUnit]
    ) -> VehicleGroup:
        vehicle_group: Optional[VehicleGroup] = None
        for unit in units:
            assert issubclass(unit.type, VehicleType)
            if vehicle_group is None:
                vehicle_group = self.m.vehicle_group(
                    self.country,
                    group_name,
                    unit.type,
                    position=unit.position,
                    heading=unit.position.heading.degrees,
                )
                vehicle_group.units[0].player_can_drive = True
                self.enable_eplrs(vehicle_group, unit.type)
                vehicle_group.units[0].name = unit.unit_name
                self.set_alarm_state(vehicle_group)
            else:
                vehicle_unit = Vehicle(
                    self.m.next_unit_id(),
                    unit.unit_name,
                    unit.type.id,
                )
                vehicle_unit.player_can_drive = True
                vehicle_unit.position = unit.position
                vehicle_unit.heading = unit.position.heading.degrees
                vehicle_group.add_unit(vehicle_unit)
            self._register_theater_unit(unit, vehicle_group.units[-1])
        if vehicle_group is None:
            raise RuntimeError(f"Error creating VehicleGroup for {group_name}")
        return vehicle_group

    def create_ship_group(
        self,
        group_name: str,
        units: list[TheaterUnit],
        frequency: Optional[RadioFrequency] = None,
    ) -> ShipGroup:
        ship_group: Optional[ShipGroup] = None
        for unit in units:
            assert issubclass(unit.type, ShipType)
            if ship_group is None:
                ship_group = self.m.ship_group(
                    self.country,
                    group_name,
                    unit.type,
                    position=unit.position,
                    heading=unit.position.heading.degrees,
                )
                if frequency:
                    ship_group.set_frequency(frequency.hertz)
                ship_group.units[0].name = unit.unit_name
                self.set_alarm_state(ship_group)
            else:
                ship_unit = Ship(
                    self.m.next_unit_id(),
                    unit.unit_name,
                    unit.type,
                )
                if frequency:
                    ship_unit.set_frequency(frequency.hertz)
                ship_unit.position = unit.position
                ship_unit.heading = unit.position.heading.degrees
                ship_group.add_unit(ship_unit)
            self._register_theater_unit(unit, ship_group.units[-1])
        if ship_group is None:
            raise RuntimeError(f"Error creating ShipGroup for {group_name}")
        return ship_group

    def create_static_group(self, unit: TheaterUnit) -> None:
        if isinstance(unit, SceneryUnit):
            # Special handling for scenery objects:
            # Only create a trigger zone and no "real" dcs unit
            self.add_trigger_zone_for_scenery(unit)
            return

        static_group = self.m.static_group(
            country=self.country,
            name=unit.unit_name,
            _type=unit.type,
            position=unit.position,
            heading=unit.position.heading.degrees,
            dead=not unit.alive,
        )
        self._register_theater_unit(unit, static_group.units[0])

    @staticmethod
    def enable_eplrs(group: VehicleGroup, unit_type: Type[VehicleType]) -> None:
        if unit_type.eplrs:
            group.points[0].tasks.append(EPLRS(group.id))

    def set_alarm_state(self, group: MovingGroup[Any]) -> None:
        if self.game.settings.perf_red_alert_state:
            group.points[0].tasks.append(OptAlarmState(2))
        else:
            group.points[0].tasks.append(OptAlarmState(1))

    def _register_theater_unit(
        self,
        theater_unit: TheaterUnit,
        dcs_unit: Unit,
    ) -> None:
        self.unit_map.add_theater_unit_mapping(theater_unit, dcs_unit)

    def add_trigger_zone_for_scenery(self, scenery: SceneryUnit) -> None:
        # Align the trigger zones to the faction color on the DCS briefing/F10 map.
        color = (
            {1: 0.2, 2: 0.7, 3: 1, 4: 0.15}
            if scenery.ground_object.is_friendly(to_player=True)
            else {1: 1, 2: 0.2, 3: 0.2, 4: 0.15}
        )

        # Create the smallest valid size trigger zone (16 feet) so that risk of overlap
        # is minimized. As long as the triggerzone is over the scenery object, we're ok.
        smallest_valid_radius = feet(16).meters

        trigger_zone = self.m.triggers.add_triggerzone(
            scenery.zone.position,
            smallest_valid_radius,
            scenery.zone.hidden,
            scenery.zone.name,
            color,
            scenery.zone.properties,
        )
        # DCS only visually shows a scenery object is dead when
        # this trigger rule is applied.  Otherwise you can kill a
        # structure twice.
        if not scenery.alive:
            self.generate_destruction_trigger_rule(trigger_zone)
        else:
            self.generate_on_dead_trigger_rule(trigger_zone)

        self.unit_map.add_scenery(scenery, trigger_zone)

    def generate_destruction_trigger_rule(self, trigger_zone: TriggerZone) -> None:
        # Add destruction zone trigger
        t = TriggerStart(comment="Destruction")
        t.actions.append(
            SceneryDestructionZone(destruction_level=100, zone=trigger_zone.id)
        )
        self.m.triggerrules.triggers.append(t)

    def generate_on_dead_trigger_rule(self, trigger_zone: TriggerZone) -> None:
        # Add a TriggerRule with the MapObjectIsDead condition to recognize killed
        # map objects and add them to the state.json with a DoScript
        t = TriggerOnce(Event.NoEvent, f"MapObjectIsDead Trigger {trigger_zone.id}")
        t.add_condition(MapObjectIsDead(trigger_zone.id))
        script_string = String(
            f'killed_ground_units[#killed_ground_units + 1] = "{trigger_zone.name}"'
        )
        t.actions.append(DoScript(script_string))
        self.m.triggerrules.triggers.append(t)


class MissileSiteGenerator(GroundObjectGenerator):
    @property
    def culled(self) -> bool:
        # Don't cull missile sites - their range is long enough to make them easily
        # culled despite being a threat.
        return False

    def generate(self) -> None:
        super(MissileSiteGenerator, self).generate()
        # Note : Only the SCUD missiles group can fire (V1 site cannot fire in game right now)
        # TODO : Should be pre-planned ?
        # TODO : Add delay to task to spread fire task over mission duration ?
        for group in self.ground_object.groups:
            vg = self.m.find_group(group.group_name)
            if vg is not None:
                targets = self.possible_missile_targets()
                if targets:
                    target = random.choice(targets)
                    real_target = target.point_from_heading(
                        Heading.random().degrees, random.randint(0, 2500)
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

    def possible_missile_targets(self) -> List[Point]:
        """
        Find enemy control points in range
        :return: List of possible missile targets
        """
        targets: List[Point] = []
        for cp in self.game.theater.controlpoints:
            if cp.captured != self.ground_object.control_point.captured:
                distance = cp.position.distance_to_point(self.ground_object.position)
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
            vg = self.m.find_group(group.group_name)
            if vg is not None:
                for u in vg.units:
                    if u.type in vehicle_map:
                        if vehicle_map[u.type].threat_range > site_range:
                            site_range = vehicle_map[u.type].threat_range
        return site_range


class GenericCarrierGenerator(GroundObjectGenerator):
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

        # This can also be refactored as the general generation was updated
        atc = self.radio_registry.alloc_uhf()

        for g_id, group in enumerate(self.ground_object.groups):
            if not group.units:
                logging.warning(f"Found empty carrier group in {self.control_point}")
                continue

            ship_group = self.create_ship_group(group.group_name, group.units, atc)

            # Always steam into the wind, even if the carrier is being moved.
            # There are multiple unsimulated hours between turns, so we can
            # count those as the time the carrier uses to move and the mission
            # time as the recovery window.
            brc = self.steam_into_wind(ship_group)

            # Set Carrier Specific Options
            if g_id == 0:
                # Correct unit type for the carrier.
                # This is only used for the super carrier setting
                ship_group.units[0].type = self.get_carrier_type(group).id
                tacan = self.tacan_registry.alloc_for_band(
                    TacanBand.X, TacanUsage.TransmitReceive
                )
                tacan_callsign = self.tacan_callsign()
                icls = next(self.icls_alloc)
                self.activate_beacons(ship_group, tacan, tacan_callsign, icls)
                self.add_runway_data(
                    brc or Heading.from_degrees(0), atc, tacan, tacan_callsign, icls
                )

    def get_carrier_type(self, group: TheaterGroup) -> Type[ShipType]:
        carrier_type = group.units[0].type
        if issubclass(carrier_type, ShipType):
            return carrier_type
        raise RuntimeError(f"First unit of TGO {group.name} is no Ship")

    def steam_into_wind(self, group: ShipGroup) -> Optional[Heading]:
        wind = self.game.conditions.weather.wind.at_0m
        brc = Heading.from_degrees(wind.direction).opposite
        # Aim for 25kts over the deck.
        carrier_speed = knots(25) - mps(wind.speed)
        for attempt in range(5):
            point = group.points[0].position.point_from_heading(
                brc.degrees, 100000 - attempt * 20000
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
        brc: Heading,
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

    def get_carrier_type(self, group: TheaterGroup) -> Type[ShipType]:
        unit_type = super().get_carrier_type(group)
        if self.game.settings.supercarrier:
            unit_type = self.upgrade_to_supercarrier(unit_type, self.control_point.name)
        return unit_type

    @staticmethod
    def upgrade_to_supercarrier(unit: Type[ShipType], name: str) -> Type[ShipType]:
        if unit == Stennis:
            if name == "CVN-71 Theodore Roosevelt":
                return CVN_71
            elif name == "CVN-72 Abraham Lincoln":
                return CVN_72
            elif name == "CVN-73 George Washington":
                return CVN_73
            elif name == "CVN-75 Harry S. Truman":
                return CVN_75
            elif name == "Carrier Strike Group 8":
                return CVN_75
            else:
                return CVN_71
        elif unit == KUZNECOW:
            return CV_1143_5
        else:
            return unit

    def tacan_callsign(self) -> str:
        # TODO: Assign these properly.
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
        self.helipads: list[StaticGroup] = []

    def generate(self) -> None:
        # This gets called for every control point, so we don't want to add an empty group (causes DCS mission editor to crash)
        if len(self.cp.helipads) == 0:
            return

        # Note: Helipad are generated as neutral object in order not to interfer with
        # capture triggers
        neutral_country = self.m.country(self.game.neutral_country.name)
        country = self.m.country(self.game.coalition_for(self.cp.captured).country_name)
        name = self.cp.name + "_helipad"
        sg = unitgroup.StaticGroup(self.m.next_group_id(), name)
        sp = StaticPoint()
        sp.position = self.cp.position
        sg.add_point(sp)

        for i, helipad in enumerate(self.cp.helipads):
            # This is used as a trigger of the number of available pads when spawning flights
            self.helipads.append(sg)
            name_i = name + "_" + str(i)
            logging.info("Generating helipad static : " + name_i)
            pad = InvisibleFARP(unit_id=self.m.next_unit_id(), name=name_i)
            pad.position = Point(helipad.x, helipad.y)
            pad.heading = helipad.heading.degrees
            sg.add_unit(pad)
            # Generate a FARP Ammo and Fuel stack for each pad
            self.m.static_group(
                country=country,
                name=(name_i + "_fuel"),
                _type=Fortification.FARP_Fuel_Depot,
                position=pad.position.point_from_heading(helipad.heading.degrees, 35),
                heading=pad.heading,
            )
            self.m.static_group(
                country=country,
                name=(name_i + "_ammo"),
                _type=Fortification.FARP_Ammo_Dump_Coating,
                position=pad.position.point_from_heading(
                    helipad.heading.degrees, 35
                ).point_from_heading(helipad.heading.degrees + 90, 10),
                heading=pad.heading,
            )
            self.m.static_group(
                country=country,
                name=(name_i + "_ws"),
                _type=Fortification.Windsock,
                position=pad.position.point_from_heading(
                    helipad.heading.degrees + 45, 35
                ),
                heading=pad.heading,
            )
        neutral_country.add_static_group(sg)


class TgoGenerator:
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
        self.helipads: dict[ControlPoint, list[StaticGroup]] = defaultdict(list)

    def generate(self) -> None:
        for cp in self.game.theater.controlpoints:
            country = self.m.country(self.game.coalition_for(cp.captured).country_name)

            # Generate helipads
            helipad_gen = HelipadGenerator(
                self.m, cp, self.game, self.radio_registry, self.tacan_registry
            )
            helipad_gen.generate()
            self.helipads[cp] = helipad_gen.helipads

            for ground_object in cp.ground_objects:
                generator: GroundObjectGenerator
                if isinstance(ground_object, CarrierGroundObject):
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
                    generator = LhaGenerator(
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
                elif isinstance(ground_object, MissileSiteGroundObject):
                    generator = MissileSiteGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                else:
                    generator = GroundObjectGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                generator.generate()
