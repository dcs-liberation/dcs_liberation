from dcs.terrain import Terrain

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
    awacsgen = None  # type: AWACSConflictGenerator
    visualgen = None  # type: VisualGenerator
    envgen = None  # type: EnvironmentGenerator

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

    def initialize(self, mission: Mission, conflict: Conflict):
        self.mission = mission
        self.conflict = conflict

        self.armorgen = ArmorConflictGenerator(mission, conflict)
        self.airgen = AircraftConflictGenerator(mission, conflict, self.game.settings)
        self.aagen = AAConflictGenerator(mission, conflict)
        self.shipgen = ShipGenerator(mission, conflict)
        self.awacsgen = AWACSConflictGenerator(mission, conflict, self.game)
        self.triggersgen = TriggersGenerator(mission, conflict, self.game)
        self.visualgen = VisualGenerator(mission, conflict, self.game)
        self.envgen = EnviromentGenerator(mission, conflict, self.game)

        player_name = self.from_cp.captured and self.attacker_name or self.defender_name
        enemy_name = self.from_cp.captured and self.defender_name or self.attacker_name
        self.extra_aagen = ExtraAAConflictGenerator(mission, conflict, self.game, player_name, enemy_name)

    def prepare(self, terrain: Terrain, is_quick: bool):
        self.mission = dcs.Mission(terrain)
        self.is_quick = is_quick

        if is_quick:
            self.attackers_starting_position = None
            self.defenders_starting_position = None
        else:
            self.attackers_starting_position = self.from_cp.at
            self.defenders_starting_position = self.to_cp.at

    def generate(self):
        self.visualgen.generate()

        if self.is_awacs_enabled:
            self.awacsgen.generate()

        self.extra_aagen.generate()
        self.triggersgen.generate(self.is_quick, self.trigger_radius)

        if self.environment_settings is None:
            self.environment_settings = self.envgen.generate()
        else:
            self.envgen.load(self.environment_settings)

        for global_cp in self.game.theater.controlpoints:
            if not global_cp.is_global:
                continue

            ship = self.shipgen.generate_carrier(type=db.find_unittype(Carriage, self.game.player)[0],
                                                 country=self.game.player,
                                                 at=global_cp.at)

            if global_cp == self.from_cp and not self.is_quick:
                self.attackers_starting_position = ship

    def units_of(self, country_name: str) -> typing.Collection[UnitType]:
        return []

    def is_successfull(self, debriefing: Debriefing) -> bool:
        return True
