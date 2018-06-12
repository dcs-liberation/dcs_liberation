from userdata.debriefing_parser import *
from theater.conflicttheater import *
from theater.base import *

from gen.armor import *
from gen.aircraft import *
from gen.aaa import *
from gen.shipgen import *
from gen.conflictgen import *


class Operation:
    starting_position = None  # type: db.StartingPosition
    mission = None  # type: dcs.Mission
    conflict = None  # type: Conflict
    armorgen = None  # type: ArmorConflictGenerator
    airgen = None  # type: AircraftConflictGenerator
    aagen = None  # type: AAConflictGenerator
    shipgen = None  # type: ShipGenerator

    def __init__(self,
                 attacker_name: str,
                 defender_name: str,
                 attacker_clients: db.PlaneDict,
                 defender_clients: db.PlaneDict,
                 from_cp: ControlPoint,
                 to_cp: ControlPoint = None):
        self.attacker_name = attacker_name
        self.defender_name = defender_name
        self.attacker_clients = attacker_clients
        self.defender_clients = defender_clients
        self.from_cp = from_cp
        self.to_cp = to_cp

    def initialize(self, mission: Mission, conflict: Conflict):
        self.mission = mission
        self.conflict = conflict

        self.armorgen = ArmorConflictGenerator(mission, conflict)
        self.airgen = AircraftConflictGenerator(mission, conflict)
        self.aagen = AAConflictGenerator(mission, conflict)
        self.shipgen = ShipGenerator(mission, conflict)

    def prepare(self, is_quick: bool):
        self.starting_position = is_quick and self.from_cp.at or None

    def generate(self):
        pass

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

    def prepare(self, is_quick: bool):
        super(CaptureOperation, self).prepare(is_quick)
        mission = dcs.Mission()

        self.initialize(mission=mission,
                        conflict=self.to_cp.conflict_attack(self.from_cp,
                                                            mission.country(self.attacker_name),
                                                            mission.country(self.defender_name)))

    def generate(self):
        self.armorgen.generate(self.attack, self.defense)
        self.aagen.generate(self.aa)
        self.airgen.generate_defense(self.intercept, clients=self.defender_clients)

        self.airgen.generate_cas(self.cas, clients=self.attacker_clients, at=self.starting_position)
        self.airgen.generate_cas_escort(self.escort, clients=self.attacker_clients, at=self.starting_position)


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

    def prepare(self, is_quick: bool):
        super(InterceptOperation, self).prepare(is_quick)
        mission = dcs.Mission()
        conflict = Conflict.intercept_conflict(
            attacker=mission.country(self.attacker_name),
            defender=mission.country(self.defender_name),
            position=self.from_cp.position,
            heading=randint(0, 360),
            radials=ALL_RADIALS
        )

        self.initialize(mission=mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_transport(self.transport, self.to_cp.at)
        self.airgen.generate_transport_escort(self.escort, clients=self.defender_clients)
        self.aagen.generate(self.airdefense)

        if self.from_cp.is_global:
            self.airgen.generate_interception(self.interceptors, clients=self.attacker_clients, at=self.shipgen.generate(self.from_cp.at))
        else:
            self.airgen.generate_interception(self.interceptors, clients=self.attacker_clients, at=self.starting_position)


class GroundInterceptOperation(Operation):
    def setup(self,
              position: Point,
              target: db.ArmorDict,
              strikegroup: db.PlaneDict):
        self.position = position
        self.strikegroup = strikegroup
        self.target = target

    def prepare(self, is_quick: bool):
        super(GroundInterceptOperation, self).prepare(is_quick)
        mission = dcs.Mission()
        conflict = Conflict.ground_intercept_conflict(
            attacker=mission.country(self.defender_name),
            defender=mission.country(self.defender_name),
            position=self.position,
            heading=randint(0, 360),
            radials=ALL_RADIALS
        )

        super(GroundInterceptOperation, self).__init__(mission, conflict)

    def generate(self):
        self.airgen.generate_cas(self.strikegroup, clients=self.attacker_clients, at=self.starting_position)
        self.armorgen.generate({}, self.target)
