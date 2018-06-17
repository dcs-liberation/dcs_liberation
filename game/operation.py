from userdata.debriefing import *
from theater.conflicttheater import *
from theater.base import *

from gen.armor import *
from gen.aircraft import *
from gen.aaa import *
from gen.shipgen import *
from gen.conflictgen import *
from gen.settingsgen import *
from gen.awacsgen import *
from gen.visualgen import *


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
    envgen = None  # type: SettingsGenerator
    awacsgen = None  # type: AWACSConflictGenerator
    visualgen = None  # type: VisualGenerator

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
        self.airgen = AircraftConflictGenerator(mission, conflict)
        self.aagen = AAConflictGenerator(mission, conflict)
        self.shipgen = ShipGenerator(mission, conflict)
        self.awacsgen = AWACSConflictGenerator(mission, conflict, self.game)
        self.envgen = SettingsGenerator(mission, conflict, self.game)
        self.visualgen = VisualGenerator(mission, conflict, self.game)

        player_name = self.from_cp.captured and self.attacker_name or self.defender_name
        enemy_name = self.from_cp.captured and self.defender_name or self.attacker_name
        self.extra_aagen = ExtraAAConflictGenerator(mission, conflict, self.game, player_name, enemy_name)

    def prepare(self, terrain: dcs.terrain.Terrain, is_quick: bool):
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
        self.envgen.generate(self.is_quick)

        for global_cp in self.game.theater.controlpoints:
            if not global_cp.is_global:
                continue

            ship = self.shipgen.generate(type=db.find_unittype(Carriage, self.game.player)[0],
                                         country=self.game.player,
                                         at=global_cp.at)

            if global_cp == self.from_cp and not self.is_quick:
                self.attackers_starting_position = ship

    def units_of(self, country_name: str) -> typing.Collection[UnitType]:
        return []

    def is_successfull(self, debriefing: Debriefing) -> bool:
        return True


class CaptureOperation(Operation):
    cas = None  # type: db.PlaneDict
    escort = None  # type: db.PlaneDict
    intercept = None  # type: db.PlaneDict
    attack = None  # type: db.ArmorDict
    defense = None  # type: db.ArmorDict
    aa = None  # type: db.AirDefenseDict

    def setup(self,
              cas: db.PlaneDict,
              escort: db.PlaneDict,
              attack: db.ArmorDict,
              intercept: db.PlaneDict,
              defense: db.ArmorDict,
              aa: db.AirDefenseDict):
        self.cas = cas
        self.escort = escort
        self.intercept = intercept
        self.attack = attack
        self.defense = defense
        self.aa = aa

    def prepare(self, terrain: dcs.terrain.Terrain, is_quick: bool):
        super(CaptureOperation, self).prepare(terrain, is_quick)

        self.defenders_starting_position = None
        if self.game.player == self.defender_name:
            self.attackers_starting_position = None

        self.initialize(mission=self.mission,
                        conflict=self.to_cp.conflict_attack(self.from_cp,
                                                            self.mission.country(self.attacker_name),
                                                            self.mission.country(self.defender_name)))

    def generate(self):
        self.armorgen.generate(self.attack, self.defense)
        self.aagen.generate(self.aa)

        self.airgen.generate_defense(self.intercept, clients=self.defender_clients, at=self.defenders_starting_position)

        self.airgen.generate_cas(self.cas, clients=self.attacker_clients, at=self.attackers_starting_position)
        self.airgen.generate_cas_escort(self.escort, clients=self.attacker_clients, at=self.attackers_starting_position)

        self.visualgen.generate_target_smokes(self.to_cp)
        super(CaptureOperation, self).generate()


class InterceptOperation(Operation):
    escort = None  # type: db.PlaneDict
    transport = None  # type: db.PlaneDict
    interceptors = None  # type: db.PlaneDict
    airdefense = None  # type: db.AirDefenseDict

    def setup(self,
              escort: db.PlaneDict,
              transport: db.PlaneDict,
              airdefense: db.AirDefenseDict,
              interceptors: db.PlaneDict):
        self.escort = escort
        self.transport = transport
        self.airdefense = airdefense
        self.interceptors = interceptors

    def prepare(self, terrain: dcs.terrain.Terrain, is_quick: bool):
        super(InterceptOperation, self).prepare(terrain, is_quick)
        self.defenders_starting_position = None
        if self.defender_name == self.game.player:
            self.attackers_starting_position = None

        conflict = Conflict.intercept_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_transport(self.transport, self.to_cp.at)
        self.airgen.generate_transport_escort(self.escort, clients=self.defender_clients)

        if self.from_cp.is_global:
            super(InterceptOperation, self).generate()
            self.airgen.generate_interception(self.interceptors, clients=self.attacker_clients, at=self.attackers_starting_position)
        else:
            self.airgen.generate_interception(self.interceptors, clients=self.attacker_clients, at=self.attackers_starting_position)
            super(InterceptOperation, self).generate()


class GroundInterceptOperation(Operation):
    def setup(self,
              target: db.ArmorDict,
              strikegroup: db.PlaneDict):
        self.strikegroup = strikegroup
        self.target = target

    def prepare(self, terrain: dcs.terrain.Terrain, is_quick: bool):
        super(GroundInterceptOperation, self).prepare(terrain, is_quick)
        conflict = Conflict.ground_intercept_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            heading=self.to_cp.position.heading_between_point(self.from_cp.position),
            cp=self.to_cp
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_cas(self.strikegroup, clients=self.attacker_clients, at=self.attackers_starting_position)
        self.armorgen.generate({}, self.target)

        super(GroundInterceptOperation, self).generate()
