from dcs.lua.parse import loads

from userdata.debriefing import *

from gen import *

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
    aagen = None  # type: AAConflictGenerator
    extra_aagen = None  # type: ExtraAAConflictGenerator
    shipgen = None  # type: ShipGenerator
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
        self.armorgen = ArmorConflictGenerator(mission, conflict)
        self.airgen = AircraftConflictGenerator(mission, conflict, self.game.settings)
        self.aagen = AAConflictGenerator(mission, conflict)
        self.shipgen = ShipGenerator(mission, conflict)
        self.airsupportgen = AirSupportConflictGenerator(mission, conflict, self.game)
        self.triggersgen = TriggersGenerator(mission, conflict, self.game)
        self.visualgen = VisualGenerator(mission, conflict, self.game)
        self.envgen = EnviromentGenerator(mission, conflict, self.game)
        self.forcedoptionsgen = ForcedOptionsGenerator(mission, conflict, self.game)
        self.groundobjectgen = GroundObjectsGenerator(mission, conflict, self.game)
        self.briefinggen = BriefingGenerator(mission, conflict, self.game)

        player_country = self.from_cp.captured and self.attacker_country or self.defender_country
        enemy_country = self.from_cp.captured and self.defender_country or self.attacker_country
        self.extra_aagen = ExtraAAConflictGenerator(mission, conflict, self.game, player_country, enemy_country)

    def prepare(self, terrain: Terrain, is_quick: bool):
        with open("resources/default_options.lua", "r") as f:
            options_dict = loads(f.read())["options"]

        dcs.Mission.aaa_vehicle_group = aaa.aaa_vehicle_group

        self.current_mission = dcs.Mission(terrain)

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

    def prepare_carriers(self, for_units: db.UnitsDict):
        if not self.departure_cp.is_global:
            return

        ship = self.shipgen.generate_carrier(for_units=[t for t, c in for_units.items() if c > 0],
                                             country=self.game.player_country,
                                             at=self.departure_cp.at)

        if not self.is_quick:
            if not self.to_cp.captured:
                self.attackers_starting_position = ship
            else:
                self.defenders_starting_position = ship

    def generate(self):

        # Generate ground object first
        self.groundobjectgen.generate()

        # air support
        self.airsupportgen.generate(self.is_awacs_enabled)

        for cp in self.game.theater.controlpoints:
            if not cp.captured:
                self.airgen.generate_patrol_group(cp, self.current_mission.country(self.game.enemy_country))
            else:
                self.airgen.generate_patrol_group(cp, self.current_mission.country(self.game.player_country))

        for i, tanker_type in enumerate(self.airsupportgen.generated_tankers):
            self.briefinggen.append_frequency("Tanker {} ({})".format(TANKER_CALLSIGNS[i], tanker_type), "{}X/{} MHz AM".format(97+i, 130+i))

        if self.is_awacs_enabled:
            self.briefinggen.append_frequency("AWACS", "133 MHz AM")

        # combined arms
        self.current_mission.groundControl.pilot_can_control_vehicles = self.ca_slots > 0
        if self.game.player_country in [country.name for country in self.current_mission.coalition["blue"].countries.values()]:
            self.current_mission.groundControl.blue_tactical_commander = self.ca_slots
        else:
            self.current_mission.groundControl.red_tactical_commander = self.ca_slots

        self.extra_aagen.generate()

        # triggers
        if self.game.is_player_attack(self.conflict.attackers_country):
            cp = self.conflict.from_cp
        else:
            cp = self.conflict.to_cp

        self.triggersgen.generate(player_cp=cp,
                                  is_quick=self.is_quick,
                                  activation_trigger_radius=self.trigger_radius,
                                  awacs_enabled=self.is_awacs_enabled)

        # env settings
        if self.environment_settings is None:
            self.environment_settings = self.envgen.generate()
        else:
            self.envgen.load(self.environment_settings)

        # options
        self.forcedoptionsgen.generate()

        # main frequencies
        self.briefinggen.append_frequency("Flight", "251 MHz AM")
        if self.departure_cp.is_global or self.conflict.to_cp.is_global:
            self.briefinggen.append_frequency("Carrier", "20X/ICLS CHAN1")

        # briefing
        self.briefinggen.generate()

        # visuals
        self.visualgen.generate()

