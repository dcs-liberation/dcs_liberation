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

class GroundInterceptOperation(Operation):
    def setup(self,
              target: db.ArmorDict,
              strikegroup: db.PlaneDict):
        self.strikegroup = strikegroup
        self.target = target

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(GroundInterceptOperation, self).prepare(terrain, is_quick)
        conflict = Conflict.ground_intercept_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            heading=self.to_cp.position.heading_between_point(self.from_cp.position),
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_cas_strikegroup(self.strikegroup, clients=self.attacker_clients, at=self.attackers_starting_position)
        self.armorgen.generate({}, self.target)

        super(GroundInterceptOperation, self).generate()
