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
from dcs.unittype import UnitType
from game.plugins import LuaPluginManager
from game.theater import ControlPoint
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
from gen.radios import RadioFrequency, RadioRegistry
from gen.tacan import TacanRegistry
from gen.triggergen import TRIGGER_RADIUS_MEDIUM, TriggersGenerator

from .. import db
from ..debriefing import Debriefing

if TYPE_CHECKING:
    from game import Game


class Operation:
    attackers_starting_position = None  # type: db.StartingPosition
    defenders_starting_position = None  # type: db.StartingPosition

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
    is_awacs_enabled = False
    ca_slots = 0

    def __init__(self,
                 departure_cp: ControlPoint,
                 ):
        self.departure_cp = departure_cp
        self.plugin_scripts: List[str] = []
        self.jtacs: List[JtacInfo] = []

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

    def units_of(self, country_name: str) -> List[UnitType]:
        return []

    def is_successfull(self, debriefing: Debriefing) -> bool:
        return True

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

    def inject_lua_trigger(self, contents: str, comment: str) -> None:
        trigger = TriggerStart(comment=comment)
        trigger.add_action(DoScript(String(contents)))
        self.current_mission.triggerrules.triggers.append(trigger)

    def bypass_plugin_script(self, mnemonic: str) -> None:
        self.plugin_scripts.append(mnemonic)

    def inject_plugin_script(self, plugin_mnemonic: str, script: str,
                             script_mnemonic: str) -> None:
        if script_mnemonic in self.plugin_scripts:
            logging.debug(
                f"Skipping already loaded {script} for {plugin_mnemonic}"
            )
        else:
            self.plugin_scripts.append(script_mnemonic)

            plugin_path = Path("./resources/plugins", plugin_mnemonic)

            script_path = Path(plugin_path, script)
            if not script_path.exists():
                logging.error(
                    f"Cannot find {script_path} for plugin {plugin_mnemonic}"
                )
                return

            trigger = TriggerStart(comment=f"Load {script_mnemonic}")
            filename = script_path.resolve()
            fileref = self.current_mission.map_resource.add_resource_file(
                filename)
            trigger.add_action(DoScriptFile(fileref))
            self.current_mission.triggerrules.triggers.append(trigger)

    def notify_info_generators(
        self,
        groundobjectgen: GroundObjectsGenerator,
        airsupportgen: AirSupportConflictGenerator,
        jtacs: List[JtacInfo],
        airgen: AircraftConflictGenerator,
    ):
        """Generates subscribed MissionInfoGenerator objects (currently kneeboards and briefings)
        """
        gens: List[MissionInfoGenerator] = [
            KneeboardGenerator(self.current_mission, self.game),
            BriefingGenerator(self.current_mission, self.game)
        ]
        for gen in gens:
            for dynamic_runway in groundobjectgen.runways.values():
                gen.add_dynamic_runway(dynamic_runway)

            for tanker in airsupportgen.air_support.tankers:
                gen.add_tanker(tanker)

            if self.is_awacs_enabled:
                for awacs in airsupportgen.air_support.awacs:
                    gen.add_awacs(awacs)

            for jtac in jtacs:
                gen.add_jtac(jtac)

            for flight in airgen.flights:
                gen.add_flight(flight)
            gen.generate()

    @classmethod
    def create_radio_registries(cls) -> None:
        unique_map_frequencies = set()  # type: Set[RadioFrequency]
        cls._create_tacan_registry(unique_map_frequencies)
        cls._create_radio_registry(unique_map_frequencies)

    def assign_channels_to_flights(self, flights: List[FlightData],
                                   air_support: AirSupport) -> None:
        """Assigns preset radio channels for client flights."""
        for flight in flights:
            if not flight.client_units:
                continue
            self.assign_channels_to_flight(flight, air_support)

    def assign_channels_to_flight(self, flight: FlightData,
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
            if data.theater == cls.game.theater.terrain.name:
                if data.atc:
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
            cls.tacan_registry
        )
        cls.groundobjectgen.generate()

    def _generate_destroyed_units(self) -> None:
        """Add destroyed units to the Mission"""
        for d in self.game.get_destroyed_units():
            try:
                utype = db.unit_type_from_name(d["type"])
            except KeyError:
                continue

            pos = Point(d["x"], d["z"])
            if utype is not None and not self.game.position_culled(pos) and self.game.settings.perf_destroyed_units:
                self.current_mission.static_group(
                    country=self.current_mission.country(
                        self.game.player_country),
                    name="",
                    _type=utype,
                    hidden=True,
                    position=pos,
                    heading=d["orientation"],
                    dead=True,
                )

    def generate(self):
        """Build the final Mission to be exported"""
        self.create_radio_registries()
        # Set mission time and weather conditions.
        EnvironmentGenerator(self.current_mission,
                             self.game.conditions).generate()
        self._generate_ground_units()
        self._generate_destroyed_units()
        self._generate_air_units()
        self.assign_channels_to_flights(self.airgen.flights,
                                        self.airsupportgen.air_support)
        self._generate_ground_conflicts()

        #  TODO: This is silly, once Bulls position is defined without Conflict this should be removed.
        default_conflict = [i for i in self.conflicts()][0]
        # Triggers
        triggersgen = TriggersGenerator(self.current_mission, default_conflict,
                                        self.game)
        triggersgen.generate()

        # Setup combined arms parameters
        self.current_mission.groundControl.pilot_can_control_vehicles = self.ca_slots > 0
        if self.game.player_country in [country.name for country in self.current_mission.coalition["blue"].countries.values()]:
            self.current_mission.groundControl.blue_tactical_commander = self.ca_slots
        else:
            self.current_mission.groundControl.red_tactical_commander = self.ca_slots

        # Options
        forcedoptionsgen = ForcedOptionsGenerator(
            self.current_mission, self.game)
        forcedoptionsgen.generate()

        # Generate Visuals Smoke Effects
        visualgen = VisualGenerator(self.current_mission, self.game)
        if self.game.settings.perf_smoke_gen:
            visualgen.generate()

        self.generate_lua(self.airgen, self.airsupportgen, self.jtacs)

        # Inject Plugins Lua Scripts and data
        for plugin in LuaPluginManager.plugins():
            if plugin.enabled:
                plugin.inject_scripts(self)
                plugin.inject_configuration(self)

        self.assign_channels_to_flights(self.airgen.flights,
                                        self.airsupportgen.air_support)
        self.notify_info_generators(
            self.groundobjectgen,
            self.airsupportgen,
            self.jtacs,
            self.airgen
        )

    @classmethod
    def _generate_air_units(cls) -> None:
        """Generate the air units for the Operation"""
        #  TODO: this is silly, once AirSupportConflictGenerator doesn't require Conflict this can be removed.
        default_conflict = [i for i in cls.conflicts()][0]

        # Air Support (Tanker & Awacs)
        assert cls.radio_registry and cls.tacan_registry
        cls.airsupportgen = AirSupportConflictGenerator(
            cls.current_mission, default_conflict, cls.game, cls.radio_registry,
            cls.tacan_registry)
        cls.airsupportgen.generate(cls.is_awacs_enabled)

        # Generate Aircraft Activity on the map
        cls.airgen = AircraftConflictGenerator(
            cls.current_mission, cls.game.settings, cls.game,
            cls.radio_registry)

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

    def _generate_ground_conflicts(self) -> None:
        """For each frontline in the Operation, generate the ground conflicts and JTACs"""
        for front_line in self.game.theater.conflicts(True):
            player_cp = front_line.control_point_a
            enemy_cp = front_line.control_point_b
            conflict = Conflict.frontline_cas_conflict(
                self.game.player_name,
                self.game.enemy_name,
                self.current_mission.country(self.game.player_country),
                self.current_mission.country(self.game.enemy_country),
                player_cp,
                enemy_cp,
                self.game.theater
            )
            # Generate frontline ops
            player_gp = self.game.ground_planners[player_cp.id].units_per_cp[enemy_cp.id]
            enemy_gp = self.game.ground_planners[enemy_cp.id].units_per_cp[player_cp.id]
            ground_conflict_gen = GroundConflictGenerator(
                self.current_mission,
                conflict, self.game,
                player_gp, enemy_gp,
                player_cp.stances[enemy_cp.id]
            )
            ground_conflict_gen.generate()
            self.jtacs.extend(ground_conflict_gen.jtacs)

    def generate_lua(self, airgen: AircraftConflictGenerator,
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

        if self.is_awacs_enabled:
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
                flightType = flight.flight_type.name
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
