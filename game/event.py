import typing
import random
import math

import dcs

from theater.controlpoint import *
from userdata.debriefing_parser import *
from game.operation import *

DIFFICULTY_LOG_BASE = 1.5


class Event:
    silent = False
    operation = None  # type: Operation
    difficulty = 1  # type: int
    BONUS_BASE = 0

    def __init__(self, attacker_name: str, defender_name: str, from_cp: ControlPoint, to_cp: ControlPoint):
        self.mission = dcs.mission.Mission()
        self.attacker = self.mission.country(attacker_name)
        self.defender = self.mission.country(defender_name)
        self.to_cp = to_cp
        self.from_cp = from_cp

    def bonus(self) -> int:
        return math.ceil(math.log(self.difficulty, DIFFICULTY_LOG_BASE) * self.BONUS_BASE)

    def is_successfull(self, debriefing: Debriefing) -> bool:
        return self.operation.is_successfull(debriefing)

    def commit(self, debriefing: Debriefing):
        for country, losses in debriefing.destroyed_units.items():
            cp = None  # type: ControlPoint
            if country == self.attacker.name:
                cp = self.from_cp
            else:
                cp = self.to_cp

            cp.base.commit_losses(losses)

    def skip(self):
        pass


class GroundInterceptEvent(Event):
    BONUS_BASE = 3
    TARGET_AMOUNT_FACTOR = 3
    TARGET_VARIETY = 3

    def __str__(self):
        return "Ground intercept at {} ({})".format(self.to_cp, "*" * self.difficulty)

    def commit(self, debriefing: Debriefing):
        super(GroundInterceptEvent, self).commit(debriefing)

        if self.from_cp.captured:
            if self.is_successfull(debriefing):
                self.to_cp.base.affect_strength(-0.1)
            else:
                self.to_cp.base.affect_strength(+0.1)
        else:
            assert False

    def skip(self):
        if not self.to_cp.captured:
            self.to_cp.base.affect_strength(+0.1)
        else:
            pass

    def player_attacking(self, position: Point, strikegroup: typing.Dict[PlaneType, int]):
        suitable_unittypes = db.find_unittype(CAP, self.defender.name)
        random.shuffle(suitable_unittypes)
        unittypes = suitable_unittypes[:self.TARGET_VARIETY]
        typecount = max(math.floor(self.difficulty * self.TARGET_AMOUNT_FACTOR), 1)
        targets = {unittype: typecount for unittype in unittypes}

        self.operation = GroundInterceptOperation(mission=self.mission,
                                                  attacker=self.attacker,
                                                  defender=self.defender,
                                                  position=position,
                                                  target=targets,
                                                  strikegroup=strikegroup)


class InterceptEvent(Event):
    ESCORT_AMOUNT_FACTOR = 2
    BONUS_BASE = 5

    def __str__(self):
        return "Intercept at {} ({})".format(self.to_cp, "*" * self.difficulty)

    def commit(self, debriefing: Debriefing):
        super(InterceptEvent, self).commit(debriefing)
        if self.is_successfull(debriefing):
            self.to_cp.base.affect_strength(0.1 * self.from_cp.captured and -1 or 1)
        else:
            self.to_cp.base.affect_strength(0.1 * self.from_cp.captured and 1 or -1)

    def skip(self):
        if self.to_cp.captured:
            self.to_cp.base.affect_strength(-0.2)

    def player_attacking(self, interceptors: typing.Dict[PlaneType, int]):
        escort = self.to_cp.base.scramble_sweep(self.to_cp)
        transport_unit = random.choice(db.find_unittype(Transport, self.defender.name))
        assert transport_unit is not None

        self.operation = InterceptOperation(mission=self.mission,
                                            attacker=self.attacker,
                                            defender=self.defender,
                                            destination=self.to_cp,
                                            destination_port=self.to_cp.airport,
                                            escort=escort,
                                            transport={transport_unit: 1},
                                            interceptors=interceptors)

    def player_defending(self, escort: typing.Dict[PlaneType, int]):
        interceptors = self.from_cp.base.scramble_interceptors_count(self.difficulty * self.ESCORT_AMOUNT_FACTOR)
        transport_unit = random.choice(db.find_unittype(Transport, self.defender.name))
        assert transport_unit is not None

        self.operation = InterceptOperation(mission=self.mission,
                                            attacker=self.attacker,
                                            defender=self.defender,
                                            destination=self.to_cp,
                                            destination_port=self.to_cp.airport,
                                            escort=escort,
                                            transport={transport_unit: 1},
                                            interceptors=interceptors)


class CaptureEvent(Event):
    silent = True
    BONUS_BASE = 7

    def __str__(self):
        return "Capture {} ({})".format(self.to_cp, "*" * self.difficulty)

    def commit(self, debriefing: Debriefing):
        super(CaptureEvent, self).commit(debriefing)
        if self.is_successfull(debriefing):
            if self.from_cp.captured:
                self.to_cp.captured = True
        else:
            if not self.from_cp.captured:
                self.to_cp.captured = False
            self.to_cp.base.affect_strength(+0.5)

    def skip(self):
        if self.to_cp.captured:
            self.to_cp.captured = False

    def player_defending(self, interceptors: typing.Dict[PlaneType, int]):
        cas = self.from_cp.base.scramble_cas(self.to_cp)
        escort = self.from_cp.base.scramble_sweep(self.to_cp)
        attackers = self.from_cp.base.assemble_cap(self.to_cp)

        self.operation = CaptureOperation(mission=self.mission,
                                          attacker=self.attacker,
                                          defender=self.defender,
                                          from_cp=self.from_cp,
                                          to_cp=self.to_cp,
                                          cas=cas,
                                          escort=escort,
                                          attack=attackers,
                                          intercept=interceptors,
                                          defense=self.to_cp.base.armor,
                                          aa=self.to_cp.base.aa)

    def player_attacking(self, cas: typing.Dict[PlaneType, int], escort: typing.Dict[PlaneType, int], armor: typing.Dict[Armor, int]):
        interceptors = self.to_cp.base.scramble_sweep(for_target=self.to_cp)

        self.operation = CaptureOperation(mission=self.mission,
                                          attacker=self.attacker,
                                          defender=self.defender,
                                          from_cp=self.from_cp,
                                          to_cp=self.to_cp,
                                          cas=cas,
                                          escort=escort,
                                          attack=armor,
                                          intercept=interceptors,
                                          defense=self.to_cp.base.armor,
                                          aa=self.to_cp.base.aa)