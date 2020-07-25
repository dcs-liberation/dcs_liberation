from dcs.countries import country_dict
from dcs.lua.parse import loads
from dcs.terrain import Terrain

from gen import *
from userdata.debriefing import *

TANKER_CALLSIGNS = ["Texaco", "Arco", "Shell"]


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
        self.airgen = AircraftConflictGenerator(mission, conflict, self.game.settings, self.game)
        self.airsupportgen = AirSupportConflictGenerator(mission, conflict, self.game)
        self.triggersgen = TriggersGenerator(mission, conflict, self.game)
        self.visualgen = VisualGenerator(mission, conflict, self.game)
        self.envgen = EnviromentGenerator(mission, conflict, self.game)
        self.forcedoptionsgen = ForcedOptionsGenerator(mission, conflict, self.game)
        self.groundobjectgen = GroundObjectsGenerator(mission, conflict, self.game)
        self.briefinggen = BriefingGenerator(mission, conflict, self.game)

        player_country = self.from_cp.captured and self.attacker_country or self.defender_country
        enemy_country = self.from_cp.captured and self.defender_country or self.attacker_country

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
        if self.game.player_country and self.game.player_country in db.BLUEFOR_FACTIONS:
            self.current_mission.coalition["blue"].add_country(country_dict[db.country_id_from_name(self.game.player_country)]())
            self.current_mission.coalition["red"].add_country(country_dict[db.country_id_from_name(self.game.enemy_country)]())
        else:
            self.current_mission.coalition["blue"].add_country(country_dict[db.country_id_from_name(self.game.enemy_country)]())
            self.current_mission.coalition["red"].add_country(country_dict[db.country_id_from_name(self.game.player_country)]())
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

        # Generate meteo
        if self.environment_settings is None:
            self.environment_settings = self.envgen.generate()
        else:
            self.envgen.load(self.environment_settings)

        # Generate ground object first
        self.groundobjectgen.generate()

        # Generate destroyed units
        for d in self.game.get_destroyed_units():
            utype = db.unit_type_from_name(d["type"])
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
                self.airgen.generate_flights(cp, country, self.game.planners[cp.id])

        # Generate ground units on frontline everywhere
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

        # Setup combined arms parameters
        self.current_mission.groundControl.pilot_can_control_vehicles = self.ca_slots > 0
        if self.game.player_country in [country.name for country in self.current_mission.coalition["blue"].countries.values()]:
            self.current_mission.groundControl.blue_tactical_commander = self.ca_slots
        else:
            self.current_mission.groundControl.red_tactical_commander = self.ca_slots

        # triggers
        if self.game.is_player_attack(self.conflict.attackers_country):
            cp = self.conflict.from_cp
        else:
            cp = self.conflict.to_cp
        self.triggersgen.generate()

        # options
        self.forcedoptionsgen.generate()

        # Generate Visuals Smoke Effects
        if self.game.settings.perf_smoke_gen:
            self.visualgen.generate()

        # Inject Lua Scripts
        load_mist = TriggerStart(comment="Load Mist Lua Framework")
        with open("./resources/scripts/mist_4_3_74.lua") as f:
            load_mist.add_action(DoScript(String(f.read())))
        self.current_mission.triggerrules.triggers.append(load_mist)

        load_dcs_libe = TriggerStart(comment="Load DCS Liberation Script")
        with open("./resources/scripts/dcs_liberation.lua") as f:
            script = f.read()
            json_location = "[["+os.path.abspath("resources\\scripts\\json.lua")+"]]"
            state_location = "[[" + os.path.abspath("state.json") + "]]"
            script = script.replace("{{json_file_abs_location}}", json_location)
            script = script.replace("{{debriefing_file_location}}", state_location)
            load_dcs_libe.add_action(DoScript(String(script)))
        self.current_mission.triggerrules.triggers.append(load_dcs_libe)

        # Briefing Generation
        for i, tanker_type in enumerate(self.airsupportgen.generated_tankers):
            self.briefinggen.append_frequency("Tanker {} ({})".format(TANKER_CALLSIGNS[i], tanker_type), "{}X/{} MHz AM".format(97+i, 130+i))

        if self.is_awacs_enabled:
            self.briefinggen.append_frequency("AWACS", "133 MHz AM")

        self.briefinggen.append_frequency("Flight", "251 MHz AM")

        # Generate the briefing
        self.briefinggen.generate()



