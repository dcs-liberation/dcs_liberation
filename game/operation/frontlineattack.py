from itertools import zip_longest

from dcs.terrain import Terrain

from game import db
from gen.armor import *
from gen.aircraft import *
from gen.aaa import *
from gen.shipgen import *
from gen.triggergen import *
from gen.awacsgen import *
from gen.visualgen import *
from gen.conflictgen import Conflict

from .operation import Operation


MAX_DISTANCE_BETWEEN_GROUPS = 12000


class FrontlineAttackOperation(Operation):
    attackers = None  # type: db.ArmorDict
    strikegroup = None  # type: db.PlaneDict
    target = None  # type: db.ArmorDict

    def setup(self,
              target: db.ArmorDict,
              attackers: db.ArmorDict,
              strikegroup: db.PlaneDict):
        self.strikegroup = strikegroup
        self.target = target
        self.attackers = attackers

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(FrontlineAttackOperation, self).prepare(terrain, is_quick)
        if self.defender_name == self.game.player:
            self.attackers_starting_position = None
            self.defenders_starting_position = None

        conflict = Conflict.frontline_cas_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        self.armorgen.generate_vec(self.attackers, self.target)
        self.airgen.generate_cas_strikegroup(self.strikegroup, clients=self.attacker_clients, at=self.attackers_starting_position)
        super(FrontlineAttackOperation, self).generate()
