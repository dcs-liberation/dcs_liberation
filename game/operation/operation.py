from __future__ import annotations
from game.theater.theatergroundobject import TheaterGroundObject

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, List, Optional, Set

from dcs import Mission
from dcs.action import DoScript, DoScriptFile
from dcs.coalition import Coalition
from dcs.countries import country_dict
from dcs.lua.parse import loads
from dcs.mapping import Point
from dcs.translation import String
from dcs.triggers import TriggerStart
from game.plugins import LuaPluginManager
from gen import Conflict, FlightType, VisualGenerator
from gen.aircraft import AIRCRAFT_DATA, AircraftConflictGenerator, FlightData
from gen.airfields import AIRFIELD_DATA
from gen.airsupportgen import AirSupport, AirSupportConflictGenerator
from gen.armor import GroundConflictGenerator, JtacInfo
from gen.beacons import load_beacons_for_terrain
from gen.briefinggen import BriefingGenerator, MissionInfoGenerator
from gen.environmentgen import EnvironmentGenerator
from gen.forcedoptionsgen import ForcedOptionsGenerator
from gen.groundobjectsgen import GroundObjectsGenerator
from gen.kneeboard import KneeboardGenerator
from gen.naming import namegen
from gen.radios import RadioFrequency, RadioRegistry
from gen.tacan import TacanRegistry
from gen.triggergen import TRIGGER_RADIUS_MEDIUM, TriggersGenerator

from .. import db
from ..theater import Airfield
from ..unitmap import UnitMap

if TYPE_CHECKING:
    from game import Game


class Operation:
    """Static class for managing the final Mission generation"""
    current_mission = None  # type: Mission
    airgen = None  # type: AircraftConflictGenerator
    triggersgen = None  # type: TriggersGenerator
    airsupportgen = None  # type: AirSupportConflictGenerator
    visualgen = None  # type: VisualGenerator
    groundobjectgen = None  # type: GroundObjectsGenerator
    briefinggen = None  # type: BriefingGenerator
    forcedoptionsgen = None  # type: ForcedOptionsGenerator
    radio_registry: Optional[RadioRegistry] = None
    tacan_registry: Optional[TacanRegistry] = None
    game = None  # type: Game
    environment_settings = None
    trigger_radius = TRIGGER_RADIUS_MEDIUM
    is_quick = None
    player_awacs_enabled = True
    #  TODO: #436 Generate Air Support for red
    enemy_awacs_enabled = True
    ca_slots = 1
    unit_map: UnitMap
    jtacs: List[JtacInfo] = []
    plugin_scripts: List[str] = []

    @classmethod
    def prepare(cls, game: Game):
        with open("resources/default_options.lua", "r") as f:
            options_dict = loads(f.read())["options"]
        cls._set_mission(Mission(game.theater.terrain))
        cls.game = game
        cls._setup_mission_coalitions()
        cls.current_mission.options.load_from_dict(options_dict)

    @classmethod
    def conflicts(cls) -> Iterable[Conflict]:
        assert cls.game
        for frontline in cls.game.theater.conflicts():
            yield Conflict(
                cls.game.theater,
                frontline.control_point_a,
                frontline.control_point_b,
                cls.game.player_name,
                cls.game.enemy_name,
                cls.game.player_country,
                cls.game.enemy_country,
                frontline.position
            )

    @classmethod
    def air_conflict(cls) -> Conflict:
        assert cls.game
        player_cp, enemy_cp = cls.game.theater.closest_opposing_control_points()
        mid_point = player_cp.position.point_from_heading(
            player_cp.position.heading_between_point(enemy_cp.position),
            player_cp.position.distance_to_point(enemy_cp.position) / 2
        )
        return Conflict(
            cls.game.theater,
            player_cp,
            enemy_cp,
            cls.game.player_name,
            cls.game.enemy_name,
            cls.game.player_country,
            cls.game.enemy_country,
            mid_point
        )

    @classmethod
    def _set_mission(cls, mission: Mission) -> None:
        cls.current_mission = mission

    @classmethod
    def _setup_mission_coalitions(cls):
        cls.current_mission.coalition["blue"] = Coalition("blue")
        cls.current_mission.coalition["red"] = Coalition("red")

        p_country = cls.game.player_country
        e_country = cls.game.enemy_country
        cls.current_mission.coalition["blue"].add_country(
            country_dict[db.country_id_from_name(p_country)]())
        cls.current_mission.coalition["red"].add_country(
            country_dict[db.country_id_from_name(e_country)]())

    @classmethod
    def inject_lua_trigger(cls, contents: str, comment: str) -> None:
        trigger = TriggerStart(comment=comment)
        trigger.add_action(DoScript(String(contents)))
        cls.current_mission.triggerrules.triggers.append(trigger)

    @classmethod
    def bypass_plugin_script(cls, mnemonic: str) -> None:
        cls.plugin_scripts.append(mnemonic)

    @classmethod
    def inject_plugin_script(cls, plugin_mnemonic: str, script: str,
                             script_mnemonic: str) -> None:
        if script_mnemonic in cls.plugin_scripts:
            logging.debug(
                f"Skipping already loaded {script} for {plugin_mnemonic}"
            )
        else:
            cls.plugin_scripts.append(script_mnemonic)

            plugin_path = Path("./resources/plugins", plugin_mnemonic)

            script_path = Path(plugin_path, script)
            if not script_path.exists():
                logging.error(
                    f"Cannot find {script_path} for plugin {plugin_mnemonic}"
                )
                return

            trigger = TriggerStart(comment=f"Load {script_mnemonic}")
            filename = script_path.resolve()
            fileref = cls.current_mission.map_resource.add_resource_file(
                filename)
            trigger.add_action(DoScriptFile(fileref))
            cls.current_mission.triggerrules.triggers.append(trigger)

    @classmethod
    def notify_info_generators(
        cls,
        groundobjectgen: GroundObjectsGenerator,
        airsupportgen: AirSupportConflictGenerator,
        jtacs: List[JtacInfo],
        airgen: AircraftConflictGenerator,
    ):
        """Generates subscribed MissionInfoGenerator objects (currently kneeboards and briefings)
        """
        gens: List[MissionInfoGenerator] = [
            KneeboardGenerator(cls.current_mission, cls.game),
            BriefingGenerator(cls.current_mission, cls.game)
        ]
        for gen in gens:
            for dynamic_runway in groundobjectgen.runways.values():
                gen.add_dynamic_runway(dynamic_runway)

            for tanker in airsupportgen.air_support.tankers:
                gen.add_tanker(tanker)

            if cls.player_awacs_enabled:
                for awacs in airsupportgen.air_support.awacs:
                    gen.add_awacs(awacs)

            for jtac in jtacs:
                gen.add_jtac(jtac)

            for flight in airgen.flights:
                gen.add_flight(flight)
            gen.generate()

    @classmethod
    def create_unit_map(cls) -> None:
        cls.unit_map = UnitMap()
        for control_point in cls.game.theater.controlpoints:
            if isinstance(control_point, Airfield):
                cls.unit_map.add_airfield(control_point)

    @classmethod
    def create_radio_registries(cls) -> None:
        unique_map_frequencies: Set[RadioFrequency] = set()
        cls._create_tacan_registry(unique_map_frequencies)
        cls._create_radio_registry(unique_map_frequencies)

        assert cls.radio_registry is not None
        for frequency in unique_map_frequencies:
            cls.radio_registry.reserve(frequency)

    @classmethod
    def assign_channels_to_flights(cls, flights: List[FlightData],
                                   air_support: AirSupport) -> None:
        """Assigns preset radio channels for client flights."""
        for flight in flights:
            if not flight.client_units:
                continue
            cls.assign_channels_to_flight(flight, air_support)

    @staticmethod
    def assign_channels_to_flight(flight: FlightData,
                                  air_support: AirSupport) -> None:
        """Assigns preset radio channels for a client flight."""
        airframe = flight.aircraft_type

        try:
            aircraft_data = AIRCRAFT_DATA[airframe.id]
        except KeyError:
            logging.warning(f"No aircraft data for {airframe.id}")
            return

        if aircraft_data.channel_allocator is not None:
            aircraft_data.channel_allocator.assign_channels_for_flight(
                flight, air_support
            )

    @classmethod
    def _create_tacan_registry(cls, unique_map_frequencies: Set[RadioFrequency]) -> None:
        """
        Dedup beacon/radio frequencies, since some maps have some frequencies
        used multiple times.
        """
        cls.tacan_registry = TacanRegistry()
        beacons = load_beacons_for_terrain(cls.game.theater.terrain.name)

        for beacon in beacons:
            unique_map_frequencies.add(beacon.frequency)
            if beacon.is_tacan:
                if beacon.channel is None:
                    logging.error(
                        f"TACAN beacon has no channel: {beacon.callsign}")
                else:
                    cls.tacan_registry.reserve(beacon.tacan_channel)

    @classmethod
    def _create_radio_registry(cls, unique_map_frequencies: Set[RadioFrequency]) -> None:
        cls.radio_registry = RadioRegistry()
        for data in AIRFIELD_DATA.values():
            if data.theater == cls.game.theater.terrain.name and data.atc:
                unique_map_frequencies.add(data.atc.hf)
                unique_map_frequencies.add(data.atc.vhf_fm)
                unique_map_frequencies.add(data.atc.vhf_am)
                unique_map_frequencies.add(data.atc.uhf)
                # No need to reserve ILS or TACAN because those are in the
                # beacon list.

    @classmethod
    def _generate_ground_units(cls):
        cls.groundobjectgen = GroundObjectsGenerator(
            cls.current_mission,
            cls.game,
            cls.radio_registry,
            cls.tacan_registry,
            cls.unit_map
        )
        cls.groundobjectgen.generate()

    @classmethod
    def _generate_destroyed_units(cls) -> None:
        """Add destroyed units to the Mission"""
        for d in cls.game.get_destroyed_units():
            try:
                utype = db.unit_type_from_name(d["type"])
            except KeyError:
                continue

            pos = Point(d["x"], d["z"])
            if utype is not None and not cls.game.position_culled(pos) and cls.game.settings.perf_destroyed_units:
                cls.current_mission.static_group(
                    country=cls.current_mission.country(
                        cls.game.player_country),
                    name="",
                    _type=utype,
                    hidden=True,
                    position=pos,
                    heading=d["orientation"],
                    dead=True,
                )

    @classmethod
    def generate(cls) -> UnitMap:
        """Build the final Mission to be exported"""
        cls.create_unit_map()
        cls.create_radio_registries()
        # Set mission time and weather conditions.
        EnvironmentGenerator(cls.current_mission,
                             cls.game.conditions).generate()
        cls._generate_ground_units()
        cls._generate_destroyed_units()
        cls._generate_air_units()
        cls.assign_channels_to_flights(cls.airgen.flights,
                                        cls.airsupportgen.air_support)
        cls._generate_ground_conflicts()

        # Triggers
        triggersgen = TriggersGenerator(cls.current_mission, cls.game)
        triggersgen.generate()

        # Setup combined arms parameters
        cls.current_mission.groundControl.pilot_can_control_vehicles = cls.ca_slots > 0
        if cls.game.player_country in [country.name for country in cls.current_mission.coalition["blue"].countries.values()]:
            cls.current_mission.groundControl.blue_tactical_commander = cls.ca_slots
        else:
            cls.current_mission.groundControl.red_tactical_commander = cls.ca_slots

        # Options
        forcedoptionsgen = ForcedOptionsGenerator(
            cls.current_mission, cls.game)
        forcedoptionsgen.generate()

        # Generate Visuals Smoke Effects
        visualgen = VisualGenerator(cls.current_mission, cls.game)
        if cls.game.settings.perf_smoke_gen:
            visualgen.generate()

        cls.generate_lua(cls.airgen, cls.airsupportgen, cls.jtacs)

        # Inject Plugins Lua Scripts and data
        cls.plugin_scripts.clear()
        for plugin in LuaPluginManager.plugins():
            if plugin.enabled:
                plugin.inject_scripts(cls)
                plugin.inject_configuration(cls)

        cls.assign_channels_to_flights(cls.airgen.flights,
                                        cls.airsupportgen.air_support)
        cls.notify_info_generators(
            cls.groundobjectgen,
            cls.airsupportgen,
            cls.jtacs,
            cls.airgen
        )
        cls.reset_naming_ids()
        return cls.unit_map

    @classmethod
    def _generate_air_units(cls) -> None:
        """Generate the air units for the Operation"""

        # Air Support (Tanker & Awacs)
        assert cls.radio_registry and cls.tacan_registry
        cls.airsupportgen = AirSupportConflictGenerator(
            cls.current_mission, cls.air_conflict(), cls.game, cls.radio_registry,
            cls.tacan_registry)
        cls.airsupportgen.generate()

        # Generate Aircraft Activity on the map
        cls.airgen = AircraftConflictGenerator(
            cls.current_mission, cls.game.settings, cls.game,
            cls.radio_registry, cls.unit_map)
        cls.airgen.clear_parking_slots()

        cls.airgen.generate_flights(
            cls.current_mission.country(cls.game.player_country),
            cls.game.blue_ato,
            cls.groundobjectgen.runways
        )
        cls.airgen.generate_flights(
            cls.current_mission.country(cls.game.enemy_country),
            cls.game.red_ato,
            cls.groundobjectgen.runways
        )
        cls.airgen.spawn_unused_aircraft(
            cls.current_mission.country(cls.game.player_country),
            cls.current_mission.country(cls.game.enemy_country))

    @classmethod
    def _generate_ground_conflicts(cls) -> None:
        """For each frontline in the Operation, generate the ground conflicts and JTACs"""
        for front_line in cls.game.theater.conflicts(True):
            player_cp = front_line.control_point_a
            enemy_cp = front_line.control_point_b
            conflict = Conflict.frontline_cas_conflict(
                cls.game.player_name,
                cls.game.enemy_name,
                cls.current_mission.country(cls.game.player_country),
                cls.current_mission.country(cls.game.enemy_country),
                player_cp,
                enemy_cp,
                cls.game.theater
            )
            # Generate frontline ops
            player_gp = cls.game.ground_planners[player_cp.id].units_per_cp[enemy_cp.id]
            enemy_gp = cls.game.ground_planners[enemy_cp.id].units_per_cp[player_cp.id]
            ground_conflict_gen = GroundConflictGenerator(
                cls.current_mission,
                conflict, cls.game,
                player_gp, enemy_gp,
                player_cp.stances[enemy_cp.id],
                cls.unit_map
            )
            ground_conflict_gen.generate()
            cls.jtacs.extend(ground_conflict_gen.jtacs)

    @classmethod
    def reset_naming_ids(cls):
        namegen.reset_numbers()

    @classmethod
    def generate_lua(cls, airgen: AircraftConflictGenerator,
                     airsupportgen: AirSupportConflictGenerator,
                     jtacs: List[JtacInfo]) -> None:
        #  TODO: Refactor this
        luaData = {
            "AircraftCarriers": {},
            "Tankers": {},
            "AWACs": {},
            "JTACs": {},
            "TargetPoints": {},
        }  # type: ignore

        for tanker in airsupportgen.air_support.tankers:
            luaData["Tankers"][tanker.callsign] = {
                "dcsGroupName": tanker.dcsGroupName,
                "callsign": tanker.callsign,
                "variant": tanker.variant,
                "radio": tanker.freq.mhz,
                "tacan": str(tanker.tacan.number) + tanker.tacan.band.name
            }

        if airsupportgen.air_support.awacs:
            for awacs in airsupportgen.air_support.awacs:
                luaData["AWACs"][awacs.callsign] = {
                    "dcsGroupName": awacs.dcsGroupName,
                    "callsign": awacs.callsign,
                    "radio": awacs.freq.mhz
                }

        for jtac in jtacs:
            luaData["JTACs"][jtac.callsign] = {
                "dcsGroupName": jtac.dcsGroupName,
                "callsign": jtac.callsign,
                "zone": jtac.region,
                "dcsUnit": jtac.unit_name,
                "laserCode": jtac.code
            }

        for flight in airgen.flights:
            if flight.friendly and flight.flight_type in [FlightType.ANTISHIP,
                                                          FlightType.DEAD,
                                                          FlightType.SEAD,
                                                          FlightType.STRIKE]:
                flightType = str(flight.flight_type)
                flightTarget = flight.package.target
                if flightTarget:
                    flightTargetName = None
                    flightTargetType = None
                    if isinstance(flightTarget, TheaterGroundObject):
                        flightTargetName = flightTarget.obj_name
                        flightTargetType = flightType + \
                            f" TGT ({flightTarget.category})"
                    elif hasattr(flightTarget, 'name'):
                        flightTargetName = flightTarget.name
                        flightTargetType = flightType + " TGT (Airbase)"
                    luaData["TargetPoints"][flightTargetName] = {
                        "name": flightTargetName,
                        "type": flightTargetType,
                        "position": {"x": flightTarget.position.x,
                                     "y": flightTarget.position.y}
                    }

        # set a LUA table with data from Liberation that we want to set
        # at the moment it contains Liberation's install path, and an overridable definition for the JTACAutoLase function
        # later, we'll add data about the units and points having been generated, in order to facilitate the configuration of the plugin lua scripts
        state_location = "[[" + os.path.abspath(".") + "]]"
        lua = """
        -- setting configuration table
        env.info("DCSLiberation|: setting configuration table")

        -- all data in this table is overridable.
        dcsLiberation = {}

        -- the base location for state.json; if non-existent, it'll be replaced with LIBERATION_EXPORT_DIR, TEMP, or DCS working directory
        dcsLiberation.installPath=""" + state_location + """

        """
        # Process the tankers
        lua += """

        -- list the tankers generated by Liberation
        dcsLiberation.Tankers = {
        """
        for key in luaData["Tankers"]:
            data = luaData["Tankers"][key]
            dcsGroupName = data["dcsGroupName"]
            callsign = data["callsign"]
            variant = data["variant"]
            tacan = data["tacan"]
            radio = data["radio"]
            lua += f"    {{dcsGroupName='{dcsGroupName}', callsign='{callsign}', variant='{variant}', tacan='{tacan}', radio='{radio}' }}, \n"
            # lua += f"    {{name='{dcsGroupName}', description='{callsign} ({variant})', information='Tacan:{tacan} Radio:{radio}' }}, \n"
        lua += "}"

        # Process the AWACSes
        lua += """

        -- list the AWACs generated by Liberation
        dcsLiberation.AWACs = {
        """
        for key in luaData["AWACs"]:
            data = luaData["AWACs"][key]
            dcsGroupName = data["dcsGroupName"]
            callsign = data["callsign"]
            radio = data["radio"]
            lua += f"    {{dcsGroupName='{dcsGroupName}', callsign='{callsign}', radio='{radio}' }}, \n"
            # lua += f"    {{name='{dcsGroupName}', description='{callsign} (AWACS)', information='Radio:{radio}' }}, \n"
        lua += "}"

        # Process the JTACs
        lua += """

        -- list the JTACs generated by Liberation
        dcsLiberation.JTACs = {
        """
        for key in luaData["JTACs"]:
            data = luaData["JTACs"][key]
            dcsGroupName = data["dcsGroupName"]
            callsign = data["callsign"]
            zone = data["zone"]
            laserCode = data["laserCode"]
            dcsUnit = data["dcsUnit"]
            lua += f"    {{dcsGroupName='{dcsGroupName}', callsign='{callsign}', zone='{zone}', laserCode='{laserCode}', dcsUnit='{dcsUnit}' }}, \n"
            # lua += f"    {{name='{dcsGroupName}', description='JTAC {callsign} ', information='Laser:{laserCode}', jtac={laserCode} }}, \n"
        lua += "}"

        # Process the Target Points
        lua += """

        -- list the target points generated by Liberation
        dcsLiberation.TargetPoints = {
        """
        for key in luaData["TargetPoints"]:
            data = luaData["TargetPoints"][key]
            name = data["name"]
            pointType = data["type"]
            positionX = data["position"]["x"]
            positionY = data["position"]["y"]
            lua += f"    {{name='{name}', pointType='{pointType}', positionX='{positionX}', positionY='{positionY}' }}, \n"
            # lua += f"    {{name='{pointType} {name}', point{{x={positionX}, z={positionY} }} }}, \n"
        lua += "}"

        lua += """

        -- list the airbases generated by Liberation
        -- dcsLiberation.Airbases = {}

        -- list the aircraft carriers generated by Liberation
        -- dcsLiberation.Carriers = {}

        -- later, we'll add more data to the table

        """

        trigger = TriggerStart(comment="Set DCS Liberation data")
        trigger.add_action(DoScript(String(lua)))
        Operation.current_mission.triggerrules.triggers.append(trigger)
