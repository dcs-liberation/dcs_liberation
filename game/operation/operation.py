from typing import Set

from gen import *
from gen.airfields import AIRFIELD_DATA
from gen.beacons import load_beacons_for_terrain
from gen.radios import RadioRegistry
from gen.tacan import TacanRegistry
from dcs.countries import country_dict
from dcs.lua.parse import loads
from dcs.terrain.terrain import Terrain
from userdata.debriefing import *


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
        self.radio_registry = RadioRegistry()
        self.tacan_registry = TacanRegistry()
        self.airgen = AircraftConflictGenerator(
            mission, conflict, self.game.settings, self.game,
            self.radio_registry)
        self.airsupportgen = AirSupportConflictGenerator(
            mission, conflict, self.game, self.radio_registry,
            self.tacan_registry)
        self.triggersgen = TriggersGenerator(mission, conflict, self.game)
        self.visualgen = VisualGenerator(mission, conflict, self.game)
        self.envgen = EnviromentGenerator(mission, conflict, self.game)
        self.forcedoptionsgen = ForcedOptionsGenerator(mission, conflict, self.game)
        self.groundobjectgen = GroundObjectsGenerator(
            mission,
            conflict,
            self.game,
            self.radio_registry,
            self.tacan_registry
        )
        self.briefinggen = BriefingGenerator(mission, conflict, self.game)

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
                    self.tacan_registry.reserve(beacon.tacan_channel)

        for airfield, data in AIRFIELD_DATA.items():
            if data.theater == self.game.theater.terrain.name:
                unique_map_frequencies.add(data.atc.hf)
                unique_map_frequencies.add(data.atc.vhf_fm)
                unique_map_frequencies.add(data.atc.vhf_am)
                unique_map_frequencies.add(data.atc.uhf)
                # No need to reserve ILS or TACAN because those are in the
                # beacon list.

        for frequency in unique_map_frequencies:
            self.radio_registry.reserve(frequency)

        # Generate meteo
        if self.environment_settings is None:
            self.environment_settings = self.envgen.generate()
        else:
            self.envgen.load(self.environment_settings)

        # Generate ground object first
        self.groundobjectgen.generate()

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
        self.airsupportgen.generate(self.is_awacs_enabled)

        # Generate Activity on the map
        for cp in self.game.theater.controlpoints:
            side = cp.captured
            if side:
                country = self.current_mission.country(self.game.player_country)
            else:
                country = self.current_mission.country(self.game.enemy_country)
            if cp.id in self.game.planners.keys():
                self.airgen.generate_flights(
                    cp,
                    country,
                    self.game.planners[cp.id],
                    self.groundobjectgen.runways
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
        if self.game.is_player_attack(self.conflict.attackers_country):
            cp = self.conflict.from_cp
        else:
            cp = self.conflict.to_cp
        self.triggersgen.generate()

        # Options
        self.forcedoptionsgen.generate()

        # Generate Visuals Smoke Effects
        if self.game.settings.perf_smoke_gen:
            self.visualgen.generate()

        # Inject Plugins Lua Scripts
        listOfPluginsScripts = []
        try:
            with open("./resources/scripts/plugins/__plugins.lst", "r") as a_file:
                for line in a_file:
                    name = line.strip()
                    if not name.startswith( '#' ):
                        trigger = TriggerStart(comment="Load " + name)
                        listOfPluginsScripts.append(name)
                        fileref = self.current_mission.map_resource.add_resource_file("./resources/scripts/plugins/" + name)
                        trigger.add_action(DoScriptFile(fileref))
                        self.current_mission.triggerrules.triggers.append(trigger)
        except Exception as e:
            print(e)

        # Inject Mist Script if not done already in the plugins
        if not "mist.lua" in listOfPluginsScripts and not "mist_4_3_74.lua" in listOfPluginsScripts: # don't load mist twice
            trigger = TriggerStart(comment="Load Mist Lua Framework")
            fileref = self.current_mission.map_resource.add_resource_file("./resources/scripts/mist_4_3_74.lua")
            trigger.add_action(DoScriptFile(fileref))
            self.current_mission.triggerrules.triggers.append(trigger)

        # Inject Liberation script
        load_dcs_libe = TriggerStart(comment="Load DCS Liberation Script")
        with open("./resources/scripts/dcs_liberation.lua") as f:
            script = f.read()
            json_location = "[["+os.path.abspath("resources\\scripts\\json.lua")+"]]"
            state_location = "[[" + os.path.abspath("state.json") + "]]"
            script = script.replace("{{json_file_abs_location}}", json_location)
            script = script.replace("{{debriefing_file_location}}", state_location)
            load_dcs_libe.add_action(DoScript(String(script)))
        self.current_mission.triggerrules.triggers.append(load_dcs_libe)

        # Load Ciribob's JTACAutoLase script if not done already in the plugins
        if not "JTACAutoLase.lua" in listOfPluginsScripts: # don't load JTACAutoLase twice
            load_autolase = TriggerStart(comment="Load JTAC script")
            with open("./resources/scripts/JTACAutoLase.lua") as f:

                script = f.read()
                script = script + "\n"

                smoke = "true"
                if hasattr(self.game.settings, "jtac_smoke_on"):
                    if not self.game.settings.jtac_smoke_on:
                        smoke = "false"

                for jtac in jtacs:
                    script += f"\nJTACAutoLase('{jtac.unit_name}', {jtac.code}, {smoke}, 'vehicle')\n"

                load_autolase.add_action(DoScript(String(script)))
            self.current_mission.triggerrules.triggers.append(load_autolase)

        self.assign_channels_to_flights()

        kneeboard_generator = KneeboardGenerator(self.current_mission)

        for dynamic_runway in self.groundobjectgen.runways.values():
            self.briefinggen.add_dynamic_runway(dynamic_runway)

        for tanker in self.airsupportgen.air_support.tankers:
            self.briefinggen.add_tanker(tanker)
            kneeboard_generator.add_tanker(tanker)

        if self.is_awacs_enabled:
            for awacs in self.airsupportgen.air_support.awacs:
                self.briefinggen.add_awacs(awacs)
                kneeboard_generator.add_awacs(awacs)

        for jtac in jtacs:
            self.briefinggen.add_jtac(jtac)
            kneeboard_generator.add_jtac(jtac)

        for flight in self.airgen.flights:
            self.briefinggen.add_flight(flight)
            kneeboard_generator.add_flight(flight)

        self.briefinggen.generate()
        kneeboard_generator.generate()

    def assign_channels_to_flights(self) -> None:
        """Assigns preset radio channels for client flights."""
        for flight in self.airgen.flights:
            if not flight.client_units:
                continue
            self.assign_channels_to_flight(flight)

    def assign_channels_to_flight(self, flight: FlightData) -> None:
        """Assigns preset radio channels for a client flight."""
        airframe = flight.aircraft_type

        try:
            aircraft_data = AIRCRAFT_DATA[airframe.id]
        except KeyError:
            logging.warning(f"No aircraft data for {airframe.id}")
            return

        aircraft_data.channel_allocator.assign_channels_for_flight(
            flight, self.airsupportgen.air_support)
