import logging
import os
from pathlib import Path
from typing import List, Optional, Set

from dcs import Mission
from dcs.action import DoScript, DoScriptFile
from dcs.coalition import Coalition
from dcs.countries import country_dict
from dcs.lua.parse import loads
from dcs.mapping import Point
from dcs.terrain.terrain import Terrain
from dcs.translation import String
from dcs.triggers import TriggerStart
from dcs.unittype import UnitType

from gen import Conflict, FlightType, VisualGenerator
from gen.aircraft import AIRCRAFT_DATA, AircraftConflictGenerator, FlightData
from gen.airfields import AIRFIELD_DATA
from gen.airsupportgen import AirSupport, AirSupportConflictGenerator
from gen.armor import GroundConflictGenerator, JtacInfo
from gen.beacons import load_beacons_for_terrain
from gen.briefinggen import BriefingGenerator
from gen.environmentgen import EnvironmentGenerator
from gen.forcedoptionsgen import ForcedOptionsGenerator
from gen.groundobjectsgen import GroundObjectsGenerator
from gen.kneeboard import KneeboardGenerator
from gen.radios import RadioFrequency, RadioRegistry
from gen.tacan import TacanRegistry
from gen.triggergen import TRIGGER_RADIUS_MEDIUM, TriggersGenerator
from plugin import LuaPluginManager
from theater import ControlPoint
from .. import db
from ..debriefing import Debriefing


class Operation:
    attackers_starting_position = None  # type: db.StartingPosition
    defenders_starting_position = None  # type: db.StartingPosition

    current_mission = None  # type: Mission
    regular_mission = None  # type: Mission
    quick_mission = None  # type: Mission
    conflict = None  # type: Conflict
    airgen = None  # type: AircraftConflictGenerator
    triggersgen = None  # type: TriggersGenerator
    airsupportgen = None  # type: AirSupportConflictGenerator
    visualgen = None  # type: VisualGenerator
    groundobjectgen = None  # type: GroundObjectsGenerator
    briefinggen = None  # type: BriefingGenerator
    forcedoptionsgen = None  # type: ForcedOptionsGenerator
    radio_registry: Optional[RadioRegistry] = None
    tacan_registry: Optional[TacanRegistry] = None

    environment_settings = None
    trigger_radius = TRIGGER_RADIUS_MEDIUM
    is_quick = None
    is_awacs_enabled = False
    ca_slots = 0

    def __init__(self,
                 game,
                 attacker_name: str,
                 defender_name: str,
                 from_cp: ControlPoint,
                 departure_cp: ControlPoint,
                 to_cp: ControlPoint):
        self.game = game
        self.attacker_name = attacker_name
        self.attacker_country = db.FACTIONS[attacker_name].country
        self.defender_name = defender_name
        self.defender_country = db.FACTIONS[defender_name].country
        print(self.defender_country, self.attacker_country)
        self.from_cp = from_cp
        self.departure_cp = departure_cp
        self.to_cp = to_cp
        self.is_quick = False
        self.plugin_scripts: List[str] = []

    def units_of(self, country_name: str) -> List[UnitType]:
        return []

    def is_successfull(self, debriefing: Debriefing) -> bool:
        return True

    @property
    def is_player_attack(self) -> bool:
        return self.from_cp.captured

    def initialize(self, mission: Mission, conflict: Conflict):
        self.current_mission = mission
        self.conflict = conflict
        self.briefinggen = BriefingGenerator(self.current_mission,
                                             self.conflict, self.game)

    def prepare(self, terrain: Terrain, is_quick: bool):
        with open("resources/default_options.lua", "r") as f:
            options_dict = loads(f.read())["options"]

        self.current_mission = Mission(terrain)

        print(self.game.player_country)
        print(country_dict[db.country_id_from_name(self.game.player_country)])
        print(country_dict[db.country_id_from_name(self.game.player_country)]())

        # Setup coalition :
        self.current_mission.coalition["blue"] = Coalition("blue")
        self.current_mission.coalition["red"] = Coalition("red")

        p_country = self.game.player_country
        e_country = self.game.enemy_country
        self.current_mission.coalition["blue"].add_country(country_dict[db.country_id_from_name(p_country)]())
        self.current_mission.coalition["red"].add_country(country_dict[db.country_id_from_name(e_country)]())

        print([c for c in self.current_mission.coalition["blue"].countries.keys()])
        print([c for c in self.current_mission.coalition["red"].countries.keys()])

        if is_quick:
            self.quick_mission = self.current_mission
        else:
            self.regular_mission = self.current_mission

        self.current_mission.options.load_from_dict(options_dict)
        self.is_quick = is_quick

        if is_quick:
            self.attackers_starting_position = None
            self.defenders_starting_position = None
        else:
            self.attackers_starting_position = self.departure_cp.at
            # TODO: Is this possible?
            if self.to_cp is not None:
                self.defenders_starting_position = self.to_cp.at
            else:
                self.defenders_starting_position = None

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
            fileref = self.current_mission.map_resource.add_resource_file(filename)
            trigger.add_action(DoScriptFile(fileref))
            self.current_mission.triggerrules.triggers.append(trigger)

    def generate(self):
        radio_registry = RadioRegistry()
        tacan_registry = TacanRegistry()

        # Dedup beacon/radio frequencies, since some maps have some frequencies
        # used multiple times.
        beacons = load_beacons_for_terrain(self.game.theater.terrain.name)
        unique_map_frequencies: Set[RadioFrequency] = set()
        for beacon in beacons:
            unique_map_frequencies.add(beacon.frequency)
            if beacon.is_tacan:
                if beacon.channel is None:
                    logging.error(
                        f"TACAN beacon has no channel: {beacon.callsign}")
                else:
                    tacan_registry.reserve(beacon.tacan_channel)

        for airfield, data in AIRFIELD_DATA.items():
            if data.theater == self.game.theater.terrain.name:
                unique_map_frequencies.add(data.atc.hf)
                unique_map_frequencies.add(data.atc.vhf_fm)
                unique_map_frequencies.add(data.atc.vhf_am)
                unique_map_frequencies.add(data.atc.uhf)
                # No need to reserve ILS or TACAN because those are in the
                # beacon list.

        for frequency in unique_map_frequencies:
            radio_registry.reserve(frequency)

        # Set mission time and weather conditions.
        EnvironmentGenerator(self.current_mission,
                             self.game.conditions).generate()

        # Generate ground object first

        groundobjectgen = GroundObjectsGenerator(
            self.current_mission,
            self.conflict,
            self.game,
            radio_registry,
            tacan_registry
        )
        groundobjectgen.generate()

        # Generate destroyed units
        for d in self.game.get_destroyed_units():
            try:
                utype = db.unit_type_from_name(d["type"])
            except KeyError:
                continue

            pos = Point(d["x"], d["z"])
            if utype is not None and not self.game.position_culled(pos) and self.game.settings.perf_destroyed_units:
                self.current_mission.static_group(
                    country=self.current_mission.country(self.game.player_country),
                    name="",
                    _type=utype,
                    hidden=True,
                    position=pos,
                    heading=d["orientation"],
                    dead=True,
                )

        # Air Support (Tanker & Awacs)
        airsupportgen = AirSupportConflictGenerator(
            self.current_mission, self.conflict, self.game, radio_registry,
            tacan_registry)
        airsupportgen.generate(self.is_awacs_enabled)

        # Generate Activity on the map
        airgen = AircraftConflictGenerator(
            self.current_mission, self.conflict, self.game.settings, self.game,
            radio_registry)

        airgen.generate_flights(
            self.current_mission.country(self.game.player_country),
            self.game.blue_ato,
            groundobjectgen.runways
        )
        airgen.generate_flights(
            self.current_mission.country(self.game.enemy_country),
            self.game.red_ato,
            groundobjectgen.runways
        )

        # Generate ground units on frontline everywhere
        jtacs: List[JtacInfo] = []
        for front_line in self.game.theater.conflicts(True):
            player_cp = front_line.control_point_a
            enemy_cp = front_line.control_point_b
            conflict = Conflict.frontline_cas_conflict(self.attacker_name, self.defender_name,
                                                       self.current_mission.country(self.attacker_country),
                                                       self.current_mission.country(self.defender_country),
                                                       player_cp, enemy_cp, self.game.theater)
            # Generate frontline ops
            player_gp = self.game.ground_planners[player_cp.id].units_per_cp[enemy_cp.id]
            enemy_gp = self.game.ground_planners[enemy_cp.id].units_per_cp[player_cp.id]
            groundConflictGen = GroundConflictGenerator(self.current_mission, conflict, self.game, player_gp, enemy_gp, player_cp.stances[enemy_cp.id])
            groundConflictGen.generate()
            jtacs.extend(groundConflictGen.jtacs)

        # Setup combined arms parameters
        self.current_mission.groundControl.pilot_can_control_vehicles = self.ca_slots > 0
        if self.game.player_country in [country.name for country in self.current_mission.coalition["blue"].countries.values()]:
            self.current_mission.groundControl.blue_tactical_commander = self.ca_slots
        else:
            self.current_mission.groundControl.red_tactical_commander = self.ca_slots

        # Triggers
        triggersgen = TriggersGenerator(self.current_mission, self.conflict,
                                        self.game)
        triggersgen.generate()

        # Options
        forcedoptionsgen = ForcedOptionsGenerator(self.current_mission,
                                                  self.conflict, self.game)
        forcedoptionsgen.generate()

        # Generate Visuals Smoke Effects
        visualgen = VisualGenerator(self.current_mission, self.conflict,
                                    self.game)
        if self.game.settings.perf_smoke_gen:
            visualgen.generate()

        luaData = {}
        luaData["AircraftCarriers"] = {}
        luaData["Tankers"] = {}
        luaData["AWACs"] = {}
        luaData["JTACs"] = {}
        luaData["TargetPoints"] = {}

        self.assign_channels_to_flights(airgen.flights,
                                        airsupportgen.air_support)

        kneeboard_generator = KneeboardGenerator(self.current_mission)
        for dynamic_runway in groundobjectgen.runways.values():
            self.briefinggen.add_dynamic_runway(dynamic_runway)

        for tanker in airsupportgen.air_support.tankers:
            self.briefinggen.add_tanker(tanker)
            kneeboard_generator.add_tanker(tanker)
            luaData["Tankers"][tanker.callsign] = { 
                "dcsGroupName": tanker.dcsGroupName,
                "callsign": tanker.callsign,
                "variant": tanker.variant,
                "radio": tanker.freq.mhz,
                "tacan": str(tanker.tacan.number) + tanker.tacan.band.name
            }

        if self.is_awacs_enabled:
            for awacs in airsupportgen.air_support.awacs:
                self.briefinggen.add_awacs(awacs)
                kneeboard_generator.add_awacs(awacs)
                luaData["AWACs"][awacs.callsign] = { 
                    "dcsGroupName": awacs.dcsGroupName,
                    "callsign": awacs.callsign,
                    "radio": awacs.freq.mhz
                }

        for jtac in jtacs:
            self.briefinggen.add_jtac(jtac)
            kneeboard_generator.add_jtac(jtac)
            luaData["JTACs"][jtac.callsign] = { 
                "dcsGroupName": jtac.dcsGroupName,
                "callsign": jtac.callsign,
                "zone": jtac.region,
                "dcsUnit": jtac.unit_name,
                "laserCode": jtac.code
            }

        for flight in airgen.flights:
            self.briefinggen.add_flight(flight)
            kneeboard_generator.add_flight(flight)
            if flight.friendly and flight.flight_type in [FlightType.ANTISHIP, FlightType.DEAD, FlightType.SEAD, FlightType.STRIKE]:
                flightType = flight.flight_type.name
                flightTarget = flight.package.target
                if flightTarget:
                    flightTargetName = None
                    flightTargetType = None
                    if hasattr(flightTarget, 'obj_name'):
                        flightTargetName = flightTarget.obj_name
                        flightTargetType = flightType + f" TGT ({flightTarget.category})"
                    elif hasattr(flightTarget, 'name'):
                        flightTargetName = flightTarget.name
                        flightTargetType = flightType + " TGT (Airbase)"
                    luaData["TargetPoints"][flightTargetName] = { 
                        "name": flightTargetName,
                        "type": flightTargetType,
                        "position": { "x": flightTarget.position.x, "y": flightTarget.position.y}
                    }
                

        self.briefinggen.generate()
        kneeboard_generator.generate()


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
            dcsGroupName= data["dcsGroupName"]
            callsign = data["callsign"]
            variant = data["variant"]
            tacan = data["tacan"]
            radio = data["radio"]
            lua += f"    {{dcsGroupName='{dcsGroupName}', callsign='{callsign}', variant='{variant}', tacan='{tacan}', radio='{radio}' }}, \n"
            #lua += f"    {{name='{dcsGroupName}', description='{callsign} ({variant})', information='Tacan:{tacan} Radio:{radio}' }}, \n"
        lua += "}"

        # Process the AWACSes
        lua += """

-- list the AWACs generated by Liberation
dcsLiberation.AWACs = {
"""
        for key in luaData["AWACs"]:
            data = luaData["AWACs"][key]
            dcsGroupName= data["dcsGroupName"]
            callsign = data["callsign"]
            radio = data["radio"]
            lua += f"    {{dcsGroupName='{dcsGroupName}', callsign='{callsign}', radio='{radio}' }}, \n"
            #lua += f"    {{name='{dcsGroupName}', description='{callsign} (AWACS)', information='Radio:{radio}' }}, \n"
        lua += "}"

        # Process the JTACs
        lua += """

-- list the JTACs generated by Liberation
dcsLiberation.JTACs = {
"""
        for key in luaData["JTACs"]:
            data = luaData["JTACs"][key]
            dcsGroupName= data["dcsGroupName"]
            callsign = data["callsign"]
            zone = data["zone"]
            laserCode = data["laserCode"]
            dcsUnit = data["dcsUnit"]
            lua += f"    {{dcsGroupName='{dcsGroupName}', callsign='{callsign}', zone='{zone}', laserCode='{laserCode}', dcsUnit='{dcsUnit}' }}, \n"
            #lua += f"    {{name='{dcsGroupName}', description='JTAC {callsign} ', information='Laser:{laserCode}', jtac={laserCode} }}, \n"
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
            #lua += f"    {{name='{pointType} {name}', point{{x={positionX}, z={positionY} }} }}, \n"
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
        self.current_mission.triggerrules.triggers.append(trigger)

        # Inject Plugins Lua Scripts and data
        for plugin in LuaPluginManager().getPlugins():
            plugin.injectScripts(self)
            plugin.injectConfiguration(self)

        self.assign_channels_to_flights(airgen.flights,
                                        airsupportgen.air_support)

        kneeboard_generator = KneeboardGenerator(self.current_mission)

        for dynamic_runway in groundobjectgen.runways.values():
            self.briefinggen.add_dynamic_runway(dynamic_runway)

        for tanker in airsupportgen.air_support.tankers:
            self.briefinggen.add_tanker(tanker)
            kneeboard_generator.add_tanker(tanker)

        if self.is_awacs_enabled:
            for awacs in airsupportgen.air_support.awacs:
                self.briefinggen.add_awacs(awacs)
                kneeboard_generator.add_awacs(awacs)

        for jtac in jtacs:
            self.briefinggen.add_jtac(jtac)
            kneeboard_generator.add_jtac(jtac)

        for flight in airgen.flights:
            self.briefinggen.add_flight(flight)
            kneeboard_generator.add_flight(flight)

        self.briefinggen.generate()
        kneeboard_generator.generate()

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
