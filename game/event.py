import typing

import dcs

from theater.controlpoint import *
from .mission import *

class Event:
    silent = False
    operation = None # type: Operation

    def failure(self):
        pass

    def success(self):
        pass

class InterceptEvent(Event):
    pass

class CaptureEvent(Event):
    silent = True

    def __init__(self, from_cp: ControlPoint, to_cp: ControlPoint):
        pass

    def player_defending(self, from_cp: ControlPoint, to_cp: ControlPoint, interceptors: typing.Dict[PlaneType, int]):
        assert not self.operation

        cas = from_cp.base.scramble_cas(to_cp)
        escort = from_cp.base.scramble_sweep(to_cp)
        attackers = from_cp.base.assemble_cap(to_cp)

        self.operation = CaptureOperation(from_cp=from_cp,
                                          to_cp=to_cp,
                                          cas=cas,
                                          escort=escort,
                                          attack=attackers,
                                          intercept=interceptors,
                                          defense=to_cp.base.armor,
                                          aa=to_cp.base.aa)

    def player_attacking(self, from_cp: ControlPoint, to_cp: ControlPoint, cas: typing.Dict[PlaneType, int], escort: typing.Dict[PlaneType, int], armor: typing.Dict[Armor, int]):
        assert not self.operation

        interceptors = to_cp.base.scramble_sweep()

        self.operation = CaptureOperation(from_cp=from_cp,
                                          to_cp=to_cp,
                                          cas=cas,
                                          escort=escort,
                                          attack=armor,
                                          intercept=interceptors,
                                          defense=to_cp.base.armor,
                                          aa=to_cp.base.aa)