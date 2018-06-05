import typing

from globals import *
from userdata.debriefing_parser import *
from dcs.mission import *
from dcs.unitgroup import *
from dcs.vehicles import *
from theater.controlpoint import *
from theater.conflicttheater import *
from theater.base import *
from shop import *

from gen.armor import *
from gen.aircraft import *
from gen.aaa import *
from gen.conflictgen import *


class Operation:
    def __init__(self, mission: Mission, conflict: Conflict):
        self.mission = mission
        self.conflict = conflict
        self.armorgen = ArmorConflictGenerator(self.mission, self.conflict)
        self.airgen = AircraftConflictGenerator(self.mission, self.conflict)
        self.aagen = AAConflictGenerator(self.mission, self.conflict)

    def units_of(self, country_name: str) -> typing.Collection[UnitType]:
        return []

    def is_successfull(self, debriefing: Debriefing) -> bool:
        return True

    def generate(self):
        pass


class CaptureOperation(Operation):
    def __init__(self,
                 mission: Mission,
                 attacker: Country,
                 defender: Country,
                 attacker_clients: db.PlaneDict,
                 defender_clients: db.PlaneDict,
                 from_cp: ControlPoint,
                 to_cp: ControlPoint,
                 cas: db.PlaneDict,
                 escort: db.PlaneDict,
                 attack: db.ArmorDict,
                 intercept: db.PlaneDict,
                 defense: db.ArmorDict,
                 aa: db.AirDefenseDict):
            conflict = to_cp.conflict_attack(from_cp, attacker, defender)

            super(CaptureOperation, self).__init__(mission, conflict)
            self.from_cp = from_cp
            self.to_cp = to_cp
            self.attacker_clients = attacker_clients
            self.defender_clients = defender_clients
            self.cas = cas
            self.escort = escort
            self.intercept = intercept

            self.attack = attack
            self.defense = defense

            self.aa = aa

    def generate(self):
        self.armorgen.generate(self.attack, self.defense)
        self.airgen.generate_cas(self.cas, clients=self.attacker_clients)
        self.airgen.generate_cas_escort(self.escort, clients=self.attacker_clients)
        self.airgen.generate_defense(self.intercept, clients=self.defender_clients)
        self.aagen.generate(self.aa)


class InterceptOperation(Operation):
    def __init__(self,
                 mission: Mission,
                 attacker: Country,
                 defender: Country,
                 attacker_clients: db.PlaneDict,
                 defender_clients: db.PlaneDict,
                 destination: ControlPoint,
                 destination_port: Airport,
                 escort: db.PlaneDict,
                 transport: db.PlaneDict,
                 airdefense: db.AirDefenseDict,
                 interceptors: db.PlaneDict):
        conflict = Conflict.intercept_conflict(
            attacker=attacker,
            defender=defender,
            position=destination.position,
            heading=randint(0, 360),
            radials=ALL_RADIALS
        )

        super(InterceptOperation, self).__init__(mission, conflict)
        self.destination_port = destination_port
        self.attacker_clients = attacker_clients
        self.defender_clients = defender_clients
        self.escort = escort
        self.transport = transport
        self.airdefense = airdefense
        self.interceptors = interceptors

    def generate(self):
        self.airgen.generate_transport(self.transport, self.destination_port)
        self.airgen.generate_transport_escort(self.escort, clients=self.defender_clients)
        self.airgen.generate_interception(self.interceptors, clients=self.attacker_clients)
        self.aagen.generate(self.airdefense)


class GroundInterceptOperation(Operation):
    def __init__(self,
                 mission: Mission,
                 attacker: Country,
                 defender: Country,
                 attacker_clients: db.PlaneDict,
                 defender_clients: db.PlaneDict,
                 position: Point,
                 target: db.ArmorDict,
                 strikegroup: db.PlaneDict):
        conflict = Conflict.ground_intercept_conflict(
            attacker=attacker,
            defender=defender,
            position=position,
            heading=randint(0, 360),
            radials=ALL_RADIALS
        )

        super(GroundInterceptOperation, self).__init__(mission, conflict)
        self.attacker_clients = attacker_clients
        self.defender_clients = defender_clients
        self.strikegroup = strikegroup
        self.target = target

    def generate(self):
        self.airgen.generate_cas(self.strikegroup, clients=self.attacker_clients)
        self.armorgen.generate({}, self.target)

