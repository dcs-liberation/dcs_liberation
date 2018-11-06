import math
import random

from dcs.task import *

from game import *
from game.event import *
from game.event.frontlineattack import FrontlineAttackEvent

from .event import *
from game.operation.convoystrike import ConvoyStrikeOperation

TRANSPORT_COUNT = 4, 6
DEFENDERS_AMOUNT_FACTOR = 4


class ConvoyStrikeEvent(Event):
    SUCCESS_FACTOR = 0.6
    STRENGTH_INFLUENCE = 0.25

    targets = None  # type: db.ArmorDict

    @property
    def threat_description(self):
        return ""

    @property
    def tasks(self):
        return [CAS]

    @property
    def global_cp_available(self) -> bool:
        return True

    def flight_name(self, for_task: typing.Type[Task]) -> str:
        if for_task == CAS:
            return "Strike flight"

    def __str__(self):
        return "Convoy Strike"

    def skip(self):
        self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def commit(self, debriefing: Debriefing):
        super(ConvoyStrikeEvent, self).commit(debriefing)

        if self.from_cp.captured:
            if self.is_successfull(debriefing):
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
        else:
            if self.is_successfull(debriefing):
                self.from_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def is_successfull(self, debriefing: Debriefing):
        killed_units = sum([v for k, v in debriefing.destroyed_units[self.defender_name].items() if db.unit_task(k) in [PinpointStrike, Reconnaissance]])
        all_units = sum(self.targets.values())
        attackers_success = (float(killed_units) / (all_units + 0.01)) > self.SUCCESS_FACTOR
        if self.from_cp.captured:
            return attackers_success
        else:
            return not attackers_success

    def player_attacking(self, flights: db.TaskForceDict):
        assert CAS in flights and len(flights) == 1, "Invalid flights"

        convoy_unittype = db.find_unittype(Reconnaissance, self.defender_name)[0]
        defense_unittype = db.find_unittype(PinpointStrike, self.defender_name)[0]

        defenders_count = int(math.ceil(self.from_cp.base.strength * self.from_cp.importance * DEFENDERS_AMOUNT_FACTOR))
        self.targets = {convoy_unittype: random.randrange(*TRANSPORT_COUNT),
                        defense_unittype: defenders_count, }

        op = ConvoyStrikeOperation(game=self.game,
                                   attacker_name=self.attacker_name,
                                   defender_name=self.defender_name,
                                   from_cp=self.from_cp,
                                   departure_cp=self.departure_cp,
                                   to_cp=self.to_cp)
        op.setup(target=self.targets,
                 strikegroup=flights[CAS])

        self.operation = op
