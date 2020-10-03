from typing import Set

from gen import *
from gen.airfields import AIRFIELD_DATA
from gen.beacons import load_beacons_for_terrain
from gen.radios import RadioRegistry
from gen.tacan import TacanRegistry
from dcs.countries import country_dict
from dcs.lua.parse import loads
from dcs.terrain.terrain import Terrain
from ..debriefing import Debriefing


class Operation:
    attackers_starting_position = None  # type: db.StartingPosition
    defenders_starting_position = None  # type: db.StartingPosition

    current_mission = None  # type: dcs.Mission
    regular_mission = None  # type: dcs.Mission
    quick_mission = None  # type: dcs.Mission
    conflict = None  # type: Conflict
    armorgen = None  # type: ArmorConflictGenerator
    airgen = None  # type: AircraftConflictGenerator
    triggersgen = None  # type: TriggersGenerator
    airsupportgen = None  # type: AirSupportConflictGenerator
    visualgen = None  # type: VisualGenerator
    envgen = None  # type: EnvironmentGenerator
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
                 to_cp: ControlPoint = None):
        self.game = game
        self.attacker_name = attacker_name
        self.attacker_country = db.FACTIONS[attacker_name]["country"]
        self.defender_name = defender_name
        self.defender_country = db.FACTIONS[defender_name]["country"]
        print(self.defender_country, self.attacker_country)
        self.from_cp = from_cp
        self.departure_cp = departure_cp
        self.to_cp = to_cp
        self.is_quick = False

    def units_of(self, country_name: str) -> typing.Collection[UnitType]:
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

        self.current_mission = dcs.Mission(terrain)

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
            self.defenders_starting_position = self.to_cp.at

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

        # Generate meteo
        envgen = EnviromentGenerator(self.current_mission, self.conflict,
                                     self.game)
        if self.environment_settings is None:
            self.environment_settings = envgen.generate()
        else:
            envgen.load(self.environment_settings)

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
        for player_cp, enemy_cp in self.game.theater.conflicts(True):
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

        # Inject Plugins Lua Scripts
        listOfPluginsScripts = []
        plugin_file_path = Path("./resources/scripts/plugins/__plugins.lst")
        if plugin_file_path.exists():
            for line in plugin_file_path.read_text().splitlines():
                name = line.strip()
                if not name.startswith( '#' ):
                    trigger = TriggerStart(comment="Load " + name)
                    listOfPluginsScripts.append(name)
                    fileref = self.current_mission.map_resource.add_resource_file("./resources/scripts/plugins/" + name)
                    trigger.add_action(DoScriptFile(fileref))
                    self.current_mission.triggerrules.triggers.append(trigger)
        else:
            logging.info(
                f"Not loading plugins, {plugin_file_path} does not exist")

        # Inject Mist Script if not done already in the plugins
        if not "mist.lua" in listOfPluginsScripts and not "mist_4_3_74.lua" in listOfPluginsScripts: # don't load the script twice
            trigger = TriggerStart(comment="Load Mist Lua framework")
            fileref = self.current_mission.map_resource.add_resource_file("./resources/scripts/mist_4_3_74.lua")
            trigger.add_action(DoScriptFile(fileref))
            self.current_mission.triggerrules.triggers.append(trigger)

        # Inject JSON library if not done already in the plugins
        if not "json.lua" in listOfPluginsScripts : # don't load the script twice
            trigger = TriggerStart(comment="Load JSON Lua library")
            fileref = self.current_mission.map_resource.add_resource_file("./resources/scripts/json.lua")
            trigger.add_action(DoScriptFile(fileref))
            self.current_mission.triggerrules.triggers.append(trigger)

        # Inject Ciribob's JTACAutoLase if not done already in the plugins
        if not "JTACAutoLase.lua" in listOfPluginsScripts : # don't load the script twice
            trigger = TriggerStart(comment="Load JTACAutoLase.lua script")
            fileref = self.current_mission.map_resource.add_resource_file("./resources/scripts/JTACAutoLase.lua")
            trigger.add_action(DoScriptFile(fileref))
            self.current_mission.triggerrules.triggers.append(trigger)

        # set a LUA table with data from Liberation that we want to set
        # at the moment it contains Liberation's install path, and an overridable definition for the JTACAutoLase function
        # later, we'll add data about the units and points having been generated, in order to facilitate the configuration of the plugin lua scripts
        state_location = "[[" + os.path.abspath("state.json") + "]]"
        lua = """
        -- setting configuration table
        env.info("DCSLiberation|: setting configuration table")
        
        -- all data in this table is overridable.
        dcsLiberation = {}
        
        -- the base location for state.json; if non-existent, it'll be replaced with LIBERATION_EXPORT_DIR, TEMP, or DCS working directory
        dcsLiberation.installPath=""" + state_location + """
        
        -- you can override dcsLiberation.JTACAutoLase to make it use your own function ; it will be called with these parameters : ({jtac.unit_name}, {jtac.code}, {smoke}, 'vehicle') for all JTACs
        if ctld then
            dcsLiberation.JTACAutoLase=ctld.JTACAutoLase
        elseif JTACAutoLase then
            dcsLiberation.JTACAutoLase=JTACAutoLase
        end
        
        -- later, we'll add more data to the table
        --dcsLiberation.POIs = {}
        --dcsLiberation.BASEs = {}
        --dcsLiberation.JTACs = {}
        """

        trigger = TriggerStart(comment="Set DCS Liberation data")
        trigger.add_action(DoScript(String(lua)))
        self.current_mission.triggerrules.triggers.append(trigger)

        # Inject DCS-Liberation script if not done already in the plugins
        if not "dcs_liberation.lua" in listOfPluginsScripts : # don't load the script twice
            trigger = TriggerStart(comment="Load DCS Liberation script")
            fileref = self.current_mission.map_resource.add_resource_file("./resources/scripts/dcs_liberation.lua")
            trigger.add_action(DoScriptFile(fileref))
            self.current_mission.triggerrules.triggers.append(trigger)

        # add a configuration for JTACAutoLase and start lasing for all JTACs
        smoke = "true"
        if hasattr(self.game.settings, "jtac_smoke_on"):
            if not self.game.settings.jtac_smoke_on:
                smoke = "false"

        lua = """
        -- setting and starting JTACs
        env.info("DCSLiberation|: setting and starting JTACs")
        """

        for jtac in jtacs:
            lua += f"if dcsLiberation.JTACAutoLase then dcsLiberation.JTACAutoLase('{jtac.unit_name}', {jtac.code}, {smoke}, 'vehicle') end\n"

        trigger = TriggerStart(comment="Start JTACs")
        trigger.add_action(DoScript(String(lua)))
        self.current_mission.triggerrules.triggers.append(trigger)

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

        aircraft_data.channel_allocator.assign_channels_for_flight(
            flight, air_support
        )
