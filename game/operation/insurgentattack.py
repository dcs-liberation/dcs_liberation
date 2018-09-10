from game.db import assigned_units_split

from .operation import *


class InsurgentAttackOperation(Operation):
    strikegroup = None  # type: db.AssignedUnitsDict
    target = None  # type: db.ArmorDict

    def setup(self,
              target: db.ArmorDict,
              strikegroup: db.AssignedUnitsDict):
        self.strikegroup = strikegroup
        self.target = target

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(InsurgentAttackOperation, self).prepare(terrain, is_quick)

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
        self.airgen.generate_defense(*assigned_units_split(self.strikegroup), at=self.defenders_starting_position)
        self.armorgen.generate(self.target, {})

        self.briefinggen.title = "Destroy insurgents"
        self.briefinggen.description = "Destroy vehicles of insurgents in close proximity of the friendly base. Be advised that your flight will not attack anything until you explicitly tell them so by comms menu."

        super(InsurgentAttackOperation, self).generate()
