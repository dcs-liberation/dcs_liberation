from dcs.terrain import Terrain
from dcs.lua.parse import loads

from userdata.debriefing import *

from theater import *
from gen import *


class Operation:
    attackers_starting_position = None  # type: db.StartingPosition
    defenders_starting_position = None  # type: db.StartingPosition
    mission = None  # type: dcs.Mission
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

    environment_settings = None
    trigger_radius = TRIGGER_RADIUS_MEDIUM
    is_quick = None
    is_awacs_enabled = False

    def __init__(self,
                 game,
                 attacker_name: str,
                 defender_name: str,
                 attacker_clients: db.PlaneDict,
                 defender_clients: db.PlaneDict,
                 from_cp: ControlPoint,
                 to_cp: ControlPoint = None):
        self.game = game
        self.attacker_name = attacker_name
        self.defender_name = defender_name
        self.attacker_clients = attacker_clients
        self.defender_clients = defender_clients
        self.from_cp = from_cp
        self.to_cp = to_cp
        self.is_quick = False

    def units_of(self, country_name: str) -> typing.Collection[UnitType]:
        return []

    def is_successfull(self, debriefing: Debriefing) -> bool:
        return True

    def initialize(self, mission: Mission, conflict: Conflict):
        self.mission = mission
        self.conflict = conflict

        self.armorgen = ArmorConflictGenerator(mission, conflict)
        self.airgen = AircraftConflictGenerator(mission, conflict, self.game.settings)
        self.aagen = AAConflictGenerator(mission, conflict)
        self.shipgen = ShipGenerator(mission, conflict)
        self.airsupportgen = AirSupportConflictGenerator(mission, conflict, self.game)
        self.triggersgen = TriggersGenerator(mission, conflict, self.game)
        self.visualgen = VisualGenerator(mission, conflict, self.game)
        self.envgen = EnviromentGenerator(mission, conflict, self.game)
        self.groundobjectgen = GroundObjectsGenerator(mission, conflict, self.game)
        self.briefinggen = BriefingGenerator(mission, conflict, self.game)

        player_name = self.from_cp.captured and self.attacker_name or self.defender_name
        enemy_name = self.from_cp.captured and self.defender_name or self.attacker_name
        self.extra_aagen = ExtraAAConflictGenerator(mission, conflict, self.game, player_name, enemy_name)

    def prepare(self, terrain: Terrain, is_quick: bool):
        with open("resources/default_options.lua", "r") as f:
            options_dict = loads(f.read())["options"]

        self.mission = dcs.Mission(terrain)
        self.mission.options.load_from_dict(options_dict)
        self.is_quick = is_quick

        if is_quick:
            self.attackers_starting_position = None
            self.defenders_starting_position = None
        else:
            self.attackers_starting_position = self.from_cp.at
            self.defenders_starting_position = self.to_cp.at

    def generate(self):
        self.visualgen.generate()

        # air support
        self.airsupportgen.generate(self.is_awacs_enabled)
        self.briefinggen.append_frequency("Tanker", "10X/240 MHz FM")
        if self.is_awacs_enabled:
            self.briefinggen.append_frequency("AWACS", "244 MHz FM")

        # ground infrastructure
        self.groundobjectgen.generate()
        self.extra_aagen.generate()

        # triggers
        if self.game.is_player_attack(self.conflict.attackers_side):
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

        # main frequencies
        self.briefinggen.append_frequency("Flight", "251 MHz FM")
        if self.conflict.from_cp.is_global or self.conflict.to_cp.is_global:
            self.briefinggen.append_frequency("Carrier", "20X/ICLS CHAN1")

        # briefing
        self.briefinggen.generate()
