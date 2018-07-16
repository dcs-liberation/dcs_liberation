from itertools import zip_longest

from dcs.terrain import Terrain

from game import db
from gen.armor import *
from gen.aircraft import *
from gen.aaa import *
from gen.shipgen import *
from gen.triggergen import *
from gen.airsupportgen import *
from gen.visualgen import *
from gen.conflictgen import Conflict

from .operation import Operation


MAX_DISTANCE_BETWEEN_GROUPS = 12000


class FrontlinePatrolOperation(Operation):
    cas = None  # type: db.PlaneDict
    escort = None  # type: db.PlaneDict
    interceptors = None  # type: db.PlaneDict

    def setup(self, cas: db.PlaneDict, escort: db.PlaneDict, interceptors: db.PlaneDict):
        self.cas = cas
        self.escort = escort
        self.interceptors = interceptors

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(FrontlinePatrolOperation, self).prepare(terrain, is_quick)
        self.defenders_starting_position = None

        conflict = Conflict.frontline_cap_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_defenders_cas(self.cas, {}, self.defenders_starting_position)
        self.airgen.generate_defenders_escort(self.escort, {}, self.defenders_starting_position)
        self.airgen.generate_patrol(self.interceptors, self.defender_clients, self.attackers_starting_position)

        # todo: generate armor

        super(FrontlinePatrolOperation, self).generate()
