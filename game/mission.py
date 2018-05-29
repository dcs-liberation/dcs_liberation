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
                 from_cp: ControlPoint,
                 to_cp: ControlPoint,
                 cas: typing.Dict[PlaneType, int],
                 escort: typing.Dict[PlaneType, int],
                 attack: typing.Dict[Armor, int],
                 intercept: typing.Dict[PlaneType, int],
                 defense: typing.Dict[Armor, int],
                 aa: typing.Dict[AirDefence, int]):
            conflict = None
            if from_cp.captured:
                assert not to_cp.captured
                conflict = to_cp.conflict_attack(from_cp, US, THEM)
            else:
                assert not from_cp.captured
                conflict = to_cp.conflict_attack(from_cp, THEM, US)

            super(CaptureOperation, self).__init__(mission, conflict)
            self.from_cp = from_cp
            self.to_cp = to_cp
            self.cas = cas
            self.escort = escort
            self.intercept = intercept

            self.attack = attack
            self.defense = defense

            self.aa = aa

    @classmethod
    def player_defending(self, from_cp: ControlPoint, to_cp: ControlPoint, interceptors: typing.Dict[PlaneType, int]):
        cas = from_cp.base.scramble_cas(to_cp)
        escort = from_cp.base.scramble_sweep(to_cp)
        attackers = from_cp.base.assemble_cap(to_cp)

        return CaptureOperation(from_cp=from_cp,
                                to_cp=to_cp,
                                cas=cas,
                                escort=escort,
                                attack=attackers,
                                intercept=interceptors,
                                defense=to_cp.base.armor,
                                aa=to_cp.base.aa)

    @classmethod
    def player_attacking(self, from_cp: ControlPoint, to_cp: ControlPoint, cas: typing.Dict[PlaneType, int], escort: typing.Dict[PlaneType, int], armor: typing.Dict[Armor, int]):
        interceptors = to_cp.base.scramble_sweep()

        return CaptureOperation(from_cp=from_cp,
                                to_cp=to_cp,
                                cas=cas,
                                escort=escort,
                                attack=armor,
                                intercept=interceptors,
                                defense=to_cp.base.armor,
                                aa=to_cp.base.aa)

    @classmethod
    def playerless(self, mission: Mission, from_cp: ControlPoint, to_cp: ControlPoint):
        return CaptureOperation(mission=mission,
                                from_cp=from_cp,
                                to_cp=to_cp,
                                cas=from_cp.base.scramble_cas(to_cp),
                                escort=from_cp.base.scramble_sweep(to_cp),
                                attack=from_cp.base.assemble_cap(to_cp),
                                intercept=to_cp.base.scramble_interceptors(0.5),
                                defense=to_cp.base.assemble_defense(0.5),
                                aa=to_cp.base.aa)

    def generate(self):
        self.armorgen.generate(self.attack, self.defense)
        self.airgen.generate_cas(self.cas)
        self.airgen.generate_escort(self.escort)
        self.airgen.generate_interceptors(self.intercept)
        self.aagen.generate(self.aa)
