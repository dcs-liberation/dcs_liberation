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
    strikegroup = None  # type: db.PlaneDict
    interceptors = None  # type: db.PlaneDict
    target = None  # type: db.ArmorDict

    def setup(self,
              target: db.ArmorDict,
              strikegroup: db.PlaneDict,
              interceptors: db.PlaneDict):
        self.strikegroup = strikegroup
        self.interceptors = interceptors
        self.target = target

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(GroundInterceptOperation, self).prepare(terrain, is_quick)
        if self.defender_name == self.game.player:
            self.attackers_starting_position = None
            self.defenders_starting_position = None

        conflict = Conflict.ground_intercept_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            heading=self.to_cp.position.heading_between_point(self.from_cp.position),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_cas_strikegroup(self.strikegroup, clients=self.attacker_clients, at=self.attackers_starting_position)

        if self.interceptors:
            self.airgen.generate_defense(self.interceptors, clients=self.defender_clients, at=self.defenders_starting_position)

        self.armorgen.generate({}, self.target)
        super(GroundInterceptOperation, self).generate()
