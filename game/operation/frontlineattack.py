from dcs.terrain.terrain import Terrain

from gen.conflictgen import Conflict
from .operation import Operation
from .. import db

MAX_DISTANCE_BETWEEN_GROUPS = 12000


class FrontlineAttackOperation(Operation):
    interceptors = None  # type: db.AssignedUnitsDict
    escort = None  # type: db.AssignedUnitsDict
    strikegroup = None  # type: db.AssignedUnitsDict

    attackers = None  # type: db.ArmorDict
    defenders = None  # type: db.ArmorDict

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(FrontlineAttackOperation, self).prepare(terrain, is_quick)
        if self.defender_name == self.game.player_name:
            self.attackers_starting_position = None
            self.defenders_starting_position = None

        conflict = Conflict.frontline_cas_conflict(
            attacker_name=self.attacker_name,
            defender_name=self.defender_name,
            attacker=self.current_mission.country(self.attacker_country),
            defender=self.current_mission.country(self.defender_country),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.current_mission,
                        conflict=conflict)

    def generate(self):
        super(FrontlineAttackOperation, self).generate()
