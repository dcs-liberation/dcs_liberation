from dcs.terrain import Terrain

from game import db
from gen.armor import *
from gen.aircraft import *
from gen.aaa import *
from gen.shipgen import *
from gen.settingsgen import *
from gen.awacsgen import *
from gen.visualgen import *
from gen.conflictgen import Conflict

from .operation import Operation


class GroundAttackOperation(Operation):
    strikegroup = None  # type: db.PlaneDict
    target = None  # type: db.ArmorDict

    def setup(self,
              target: db.ArmorDict,
              strikegroup: db.PlaneDict):
        self.strikegroup = strikegroup
        self.target = target

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(GroundAttackOperation, self).prepare(terrain, is_quick)

        conflict = Conflict.ground_attack_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_defense(self.strikegroup, self.defender_clients, self.defenders_starting_position)
        self.armorgen.generate(self.target, {})

        super(GroundAttackOperation, self).generate()
