import typing

from globals import *
from dcs.mission import *
from dcs.unitgroup import *
from dcs.vehicles import *
from theater.controlpoint import *
from theater.base import *

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

class CaptureOperation(Operation):
    def __init__(self,
                 mission: Mission,
                 attacker: Country,
                 defender: Country,
                 from_cp: ControlPoint,
                 to_cp: ControlPoint,
                 cas: typing.Dict[PlaneType, int],
                 escort: typing.Dict[PlaneType, int],
                 attack: typing.Dict[Armor, int],
                 intercept: typing.Dict[PlaneType, int],
                 defense: typing.Dict[Armor, int],
                 aa: typing.Dict[AirDefence, int]):
            conflict = to_cp.conflict_attack(from_cp, attacker, defender)

            super(CaptureOperation, self).__init__(mission, conflict)
            self.from_cp = from_cp
            self.to_cp = to_cp
            self.cas = cas
            self.escort = escort
            self.intercept = intercept

            self.attack = attack
            self.defense = defense

            self.aa = aa

    def generate(self):
        self.armorgen.generate(self.attack, self.defense)
        self.airgen.generate_cas(self.cas)
        self.airgen.generate_cas_escort(self.escort)
        self.airgen.generate_defense(self.intercept)
        self.aagen.generate(self.aa)

class InterceptOperation(Operation):
    def __init__(self,
                 mission: Mission,
                 attacker: Country,
                 defender: Country,
                 destination: ControlPoint,
                 destination_port: Airport,
                 escort: typing.Dict[PlaneType, int],
                 transport: typing.Dict[PlaneType, int],
                 interceptors: typing.Dict[PlaneType, int]):
        conflict = Conflict.intercept_conflict(
            attacker=attacker,
            defender=defender,
            position=destination.position,
            heading=0
        )

        super(InterceptOperation, self).__init__(mission, conflict)
        self.destination_port = destination_port
        self.escort = escort
        self.transport = transport
        self.interceptors = interceptors

    def generate(self):
        self.airgen.generate_transport(self.transport, self.destination_port)
        self.airgen.generate_transport_escort(self.escort)
        self.airgen.generate_interception(self.interceptors)
